Source: https://strawberry.rocks/docs

// to launch
python -m venv virtualenv
source virtualenv/bin/activate
pip install cryptography
pip install sqlalchemy 'fastapi[all]' 'uvicorn[standard]'
pip install 'strawberry-graphql[debug-server]'

<!-- strawberry server schema -->

=================================
Serever build with FastAPI, Strawberry, SQLAchemy, SQLLite database

In requirements.txt are dependencies that we need in our project

To generate requirements and store in file:

```
pip freeze > file.txt
```

To start server:

```
uvicorn main:app --reload
```
