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