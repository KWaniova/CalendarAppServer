Source: https://strawberry.rocks/docs

System requirments to launch this app - python environment (python v3.8.x, conda or pip...)

To generate python virtual environment:

```
python -m venv virtualenv
source virtualenv/bin/activate
pip install cryptography
pip install sqlalchemy 'fastapi[all]' 'uvicorn[standard]'
pip install 'strawberry-graphql[debug-server]'

```

=================================
Serever build with Strawberry, SQLAchemy, SQLLite database

In requirements.txt are dependencies that we need in our project

To generate requirements and store in file:

```
pip freeze > file.txt
```

To start server:

```
uvicorn main:app --reload
```
