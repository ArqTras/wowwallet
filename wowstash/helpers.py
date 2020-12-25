from wowstash.library.elasticsearch import send_es
from wowstash.library.mattermost import post_webhook


def capture_event(event_type, user_obj):
    send_es({'type': event_type, 'user': user_obj.email})
    post_webhook(f'`{event_type}` from user {user_obj.id}')
