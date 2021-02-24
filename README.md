# FastApi_CockroachDB
A reference project to try out the use of FastApi and CockroachDB cloud together.

## Set Up
Use the following steps to set up a project like this one:
1. Ensure you have python3, pip3 installed
  * Try `pip --version` and `pip3 --version` and continue with whichever works.
2. Install virtualenv
  ```bash
  $ pip3 install virtualenv
  ```
3. Create a virtual environment locally
  ```bash
  $ virtualenv env
  ```
4. Activate the virtual environment
  * On Windows:
  ```bash
  > env\Scripts\activate
  ```
  * On Linux:
  ```bash
  $ source env/bin/activate
  ```
5. Install dependencies
  ```bash
  $ pip3 install sqlalchemy sqlalchemy-cockroachdb psycopg2-binary shortuuid fastapi uvicorn[standard] 
  ```
6. Create a main.py folder and set up a basic fastapi app
7. Run the web server
  ```bash
  uvicorn main:app --reload
  ```
---
## Using CockroachDB
Follow these steps to get up and running with CockroachDB.
1. Create a CockroachDB cloud cluster and save the connection string
  * It will look like: `postgres://...:...@...`
2. Create a declarative base for your models
  ```python
  Base = declarative_base()
  ```
3. Create your models
  ```python
  class Sports(Base):
  __tablename__ = 'sports'
  id = Column(String(100), primary_key=True)
  name = Column(String(100), nullable=False)
  description = Column(String(500), nullable=False)

  def __repr__(self):
    return f"{self.name}: {self.description}"
  ```
4. Create the database engine, create all tables and the session factory
  ```python
  engine = create_engine(
  "cockroachdb://user:pass@host",
  echo=True
  )
  Base.metadata.create_all(engine)
  sessionmaker = sessionmaker(engine)
  ```
  * Note that the first argument to create_engineis your connection string with `postgres` switched for `cockroachdb`
5. Perform database operations inside run_transaction callbacks
  * run_transaction helps with code encapsulation, see more [here](https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb-sqlalchemy.html#use-the-run_transaction-function)
  * your callback function should take a session variable followed by any other variables you need
  ```python
  def callback(session, sport_id: str):
    found = session.query(Sports).filter_by(id=sport_id).first()
    if found:
      return {
        "id": found.id,
        "name": found.name, "description": found.description
      }
    else:
      # ... raise 404
  ```
6. Call the run_transaction function with your session factory and your callback.
  ```python
  run_transaction(sessionmaker, lambda s: callback(s, sport_id))
  ```
---
## Using FastApi
1. Create the Documentation metadata
  ```python
    tags_metadata = [
      {
        "name": "tag name",
        "description": "tag info"
      },
      ...
    ]
  ```
2. Create the FastApi app
  ```python
    app = FastApi(
      title="title",
      description="description",
      version="v...",
      openapi_tags=tags_metadata
    )
  ```
3. Create pydantic models for api operations where users send data (such as creating a new object)
  * note these models only have the data you need to be given, I don't include the id here since we generate it.
  ```python
    class SportsCreate(BaseModel):
      name: str,
      description: str
  ```
4. Add your routes!
  ```python
    @app.get('/sports', tags=['tag name'])
    def get_sports():
      # get and return all sports...

    @app.patch('/sports', tags=['tag name'])
    def patch_sports(sport_id: str, sport: SportsCreate):
      # Find sport by id and update
  ```