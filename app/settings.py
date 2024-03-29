"""
    App settings file
"""
import os

ADMINS = [
    "matej.ramuta@gmail.com",
    "besal.ziga@gmail.com",
    "miha.fabjan@gmail.com"
]


def is_local():
    env = str(os.environ["SERVER_NAME"])
    if env.startswith("localhost"):
        return True
    else:
        return False