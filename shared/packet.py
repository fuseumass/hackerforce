import os
from django.conf import settings
import requests

def get_packet_file_path():
    return os.path.join(settings.PROJECT_ROOT, 'static', settings.SPONSORSHIP_PACKET_FILE) if settings.SPONSORSHIP_PACKET_FILE else None

def fetch_packet():
    if settings.SPONSORSHIP_PACKET_FILE and settings.SPONSORSHIP_PACKET_URL:
        if not os.path.exists(get_packet_file_path()):
            r = requests.get(settings.SPONSORSHIP_PACKET_URL, stream=True)
            if r.status_code == 200:
                with open(get_packet_file_path(), 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
