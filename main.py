from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from keys import CDB_PASS
from shortuuid import uuid
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction

tags_metadata = [
  {
    "name": "Documentation",
    "description": "The route for this page"
  },
  {
    "name": "General Sports Operations",
    "description": "Operations on the set of all sports listed"
  },
  {
    "name": "Specific Sports Operations",
    "description": "Operations on specific database entries"
  }
]

app = FastAPI(
  title="FastApi + CockroachDB Example Project",
  description="An api to use as future reference - Created by Julien Bertazzo Lambert",
  version="0.1.0",
  openapi_tags=tags_metadata
)
Base = declarative_base()

# Database Model
class Sports(Base):
  __tablename__ = 'sports'
  id = Column(String(100), primary_key=True)
  name = Column(String(100), nullable=False)
  description = Column(String(500), nullable=False)

  def __repr__(self):
    return f"{self.name}: {self.description}"

# Pydantic model (for req bodies)
class SportsCreate(BaseModel):
  name: str
  description: str

engine = create_engine(
  f"cockroachdb://julien:{CDB_PASS}@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=certs/cc-ca.crt&options=--cluster=good-bat-867",
  echo=True
)
Base.metadata.create_all(engine)
sessionmaker = sessionmaker(engine)

@app.get('/', tags=['Documentation'])
def root():
  return RedirectResponse('/docs', 301)

@app.get('/sports', tags=['General Sports Operations'])
def get_sports():
  def callback(session):
    return str(session.query(Sports).all())
  sport = run_transaction(sessionmaker, callback)
  return {"sports": sport}

@app.post('/sports', tags=['General Sports Operations'])
def post_sport(sport: SportsCreate):
  def callback(session, sport):
    new_sport = Sports(id=uuid(), name=sport.name, description=sport.description)
    session.add(new_sport)
    return {"id": new_sport.id, "name": new_sport.name, "description": new_sport.description}
  return run_transaction(sessionmaker, lambda s: callback(s, sport))

@app.get('/sports/{sport_id}', tags=['Specific Sports Operations'])
def get_sport(sport_id: str):
  def callback(session, sport_id):
    found = session.query(Sports).filter_by(id=sport_id).first()
    if found:
      return {"id": found.id, "name": found.name, "description": found.description}
    else:
      raise HTTPException(status_code=404, detail="Sport not found")
  return run_transaction(sessionmaker, lambda s: callback(s, sport_id))

@app.patch('/sports/{sport_id}', tags=['Specific Sports Operations'])
def patch_sport(sport_id: str, sport: SportsCreate):
  def callback(session, sport_id, sport):
    found = session.query(Sports).filter_by(id=sport_id).update({"name": sport.name, "description": sport.description})
    if not found:
      raise HTTPException(status_code=404, detail="Sport not found")
    return {"message": "Successfully updated"}
  return run_transaction(sessionmaker, lambda s: callback(s, sport_id, sport))

@app.delete('/sports/{sport_id}', tags=['Specific Sports Operations'])
def delete_sport(sport_id: str):
  def callback(session, sport_id):
    found = session.query(Sports).filter_by(id=sport_id).delete()
    if not found:
      raise HTTPException(status_code=404, detail="Sport not found")
    return {"message": "Successfully deleted"}
  return run_transaction(sessionmaker, lambda s: callback(s, sport_id))