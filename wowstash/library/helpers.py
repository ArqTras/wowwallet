from wowstash.models import Event
from wowstash.factory import db


def capture_event(user_id, event_type):
    event = Event(
        user=user_id,
        type=event_type
    )
    db.session.add(event)
    db.session.commit()
    return
