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

# Login:

```
mutation LoginMutations {
  login(email: "sam@email.com", password: "Sam123") {
    message
    data {
      token
    }
    status
  }
  logBEn: login(email: "ben@email.com", password: "Ben123") {
    message
    data {
      token
    }
    status
  }
}

mutation MyMutation2 {
  logout(auth: "bbbe3881594cbfde6723981d8d43a18b") {
    data
    message
    status
  }
}
```

====================

# Get data

```
query GetUsers {
  users(auth: "") {
    email
    id
    password
    firstName
    lastName
    createdAt
  }
}

mutation CreateSam {
  createUser(
    email: "sam@email.com"
    firstName: "Samatha"
    lastName: "Smith"
    password: "Sam123"
  ) {
    status
  }
}

mutation CreateBen {
  createUser(
    email: "ben@email.com"
    firstName: "Ben"
    lastName: "Smith"
    password: "Ben123"
  ) {
    status
  }
}

query Me {
  me(auth: "9079cf9a6551489d52869141f50ac45e") {
    firstName
  }
}


```
