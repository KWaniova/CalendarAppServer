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

```

mutation CreateSam {
  createUser( user:{
    firstName: "Samatha",
    email: "sam@email.com",
    lastName: "Smith",
    password: "Sam123"
  }
  ) {
    status
  }
}

mutation CreateBen {
  createUser(
    user:{
      email: "ben@email.com"
    firstName: "Ben"
    lastName: "Smith"
    password: "Ben123"
    }
  ) {
    status
  }
}

mutation CreateBob {
  createUser(
    user:{
      email: "bobemail.com"
    firstName: "Bob"
    lastName: "Smith"
    password: "Bob123"
    }
  ) {
    status
  }
}
mutation CreateMike {
  createUser(
    user:{
      email: "mike@email.com"
    firstName: "Mike"
    lastName: "Smith"
    password: "Mike"
    }
  ) {
    status
  }
}



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
  logBob: login(email: "bobemail.com", password: "Bob123") {
    message
    data {
      token
    }
    status
  }
  logMike: login(email: "mike@email.com", password: "Mike") {
    message
    data {
      token
    }
    status
  }
}

mutation Logout {
  logout(auth: "673af1d53cdbee08e940cb4850c18d64") {
    data
    message
    status
  }
}

query Me {
  me(auth: "965ba223204c11a081fe2b611079d6dc") {
    firstName
    id


  }
}

query GetUsers {
  users(auth:"c845f79f8bf93c09d24e6ee6d1af0613") {
    email
    id
    firstName
    lastName
    createdAt
  }
}




mutation MakeConnection {
  addConnection(auth: "1a88b4b3423bb176735cbaeec22e6fa1", targetUserId: "1491580a-9261-43cc-8f04-6c9bd73c6668")
}

mutation ConnectionActions {
  connectionAction(
    action: ACCEPT
    auth: "c845f79f8bf93c09d24e6ee6d1af0613"
    connectionId: "8ec83485-2ed1-488d-ba8a-b260d3e534d1"
  )
}

query Connections {
  connectionsList(
    auth: "c34f3d2bac7a41db564c1ab511819436"
    userId: "1491580a-9261-43cc-8f04-6c9bd73c6668"
  ) {
    connections {
      connectionStatus
      firstName
      lastName
      id

    }
    connectionRequests{
      connectionStatus
      firstName
      lastName
      id

    }
     connectionRequestsSent{
      connectionStatus
      firstName
      lastName
      id

    }
  }
}
```
