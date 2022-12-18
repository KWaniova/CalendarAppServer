/*


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
  users(auth:"965ba223204c11a081fe2b611079d6dc") {
    email
    id
    firstName
    lastName
    createdAt
  }
}
mutation MakeConnection {
  addConnection(auth: "965ba223204c11a081fe2b611079d6dc", targetUserId: "42c1fd9f-5494-4b90-8d21-dbb845258794")
}

mutation ConnectionActions {
  connectionAction(
    action: ACCEPT
    auth: "a6f854ca08ecc945fbb9465cf0adb2cc"
    connectionId: "0e2b0c15-2afc-4a6b-9fcb-54cc23da4fac"
  )
}


query MyConnections {
  myConnections(auth: "965ba223204c11a081fe2b611079d6dc") {
    connectionRequests {
      connectionStatus
      firstName
      id
      lastName
    }
    connectionRequestsSent {
      connectionStatus
      firstName
      id
      lastName
    }
    connections {
      connectionStatus
      firstName
      id
    }
  }
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

mutation AddEvent {
  createPublicEvent(
    auth: "965ba223204c11a081fe2b611079d6dc"
    event: {title: "Some event", description: "description", startDate: "2022-12-16T14:48:00", endDate: "2022-12-13T22:48:00"}
  )
}


query myEvents {
  myEvents(auth: "965ba223204c11a081fe2b611079d6dc", fromDate: "2022-12-01T14:48:00", toDate: "2022-12-26T14:48:00"){
    title
    description
    type
    startDate
    endDate
  }
}

    

*/
