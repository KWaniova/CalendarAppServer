# def map_event_to_event_model(instance: Event) -> EventModel:
#     return EventModel(
#         id=instance.id,
#         title=instance.title,
#         description=instance.description,
#         type=instance.type.value,
#         start_date=instance.date_range.start_date,
#         end_date=instance.date_range.end_date,
#         user_id=instance.user_id
#     )


# def map_event_model_to_event(instance: EventModel) -> Event:
#     return Event(
#         id=instance.id,
#         title=instance.title,
#         description=instance.description,
#         type=instance.type,
#         date_range=DateRange(start_date=instance.start_date,
#                              end_date=instance.end_date),
#         user_id=instance.user_id
#     )
