# Will not claer session data after signup, making one-stop shopping easier

from django.contrib.sessions.backends.db import SessionStore as DbSessionStore

class SessionStore(DbSessionStore):
    def cycle_key(self):
        pass