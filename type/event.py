import strawberry


@strawberry.input
class EventInput:
    title: str
    description: str
    start_date: str
    end_date: str


# TODO: validate (start<end date, user id)
