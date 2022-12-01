Source: https://strawberry.rocks/docs

// to launch
python -m venv virtualenv
source virtualenv/bin/activate
pip install 'strawberry-graphql[debug-server]'

strawberry server schema

### exp_1

Enum type - (in strawberry)

```
query{
  books{
  __typename
    title,
    type
  }
}

{
  # books{
  #   type
  #   title
  #   id
  # }
  bookByType(type: FANTASY) {
    title
  }
}
```

### exp_2

```
query {
 books {
    title
    author {
      name
    }
  }

  authors {
    name
  }
}
```

### exp_3

```
{
  books {
    title
    id
  }
  authors {
    name
    id
  }
}

mutation{
  addBook(inputBook:{
    title: "Harry Potter and the Goblet of Fire",
    authorId: 1
  })
}

query MyQuery {
  authors {
    id
    name
    books {
      title
    }
  }
  books{
    title
  }
}
```

### exp_5

```
query{
  greet
  # greet(name: null)
  # greet(name: "Alfons")
}
```
