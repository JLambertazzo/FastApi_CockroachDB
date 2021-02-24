from fastapi import FastAPI
from keys import CDB_PASS
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from cockroachdb.sqlalchemy import run_transaction
app = FastAPI()
Base = declarative_base()

class Sports(Base):
  __tablename__ = 'sports'
  id = Column(Integer, primary_key=True)
  name = Column(String(100), nullable=False)
  description = Column(String(500), nullable=False)

  def __repr__(self):
    return f"{self.name}: {self.description}"

engine = create_engine(
  f"cockroachdb://julien:{CDB_PASS}@free-tier.gcp-us-central1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=certs/cc-ca.crt&options=--cluster=good-bat-867",
  echo=True
)
Base.metadata.create_all(engine)
sessionmaker = sessionmaker(engine)

@app.get('/sports')
def get_sports():
  def callback(session):
    return str(session.query(Sports).all())
  sport = run_transaction(sessionmaker, callback)
  return {"sports": sport}

@app.post('/sports')
def post_sport():
  def callback(session):
    sport = Sports(id=3, name='basketball', description='basketball')
    session.add(sport)
  run_transaction(sessionmaker, callback)
  return {"message": "success"}