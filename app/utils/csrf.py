import random
import string
from google.appengine.api import memcache


def get_csrf():
    random_csrf = ''.join(random.choice(string.ascii_uppercase) for i in range(12))

    # add csrf to memcache for 1 hour
    memcache.add(key=random_csrf, value=True, time=3600)

    return random_csrf