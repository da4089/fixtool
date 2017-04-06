
class Session(object):
    pass

class ClientSession(Session):

    def __init__(self):
        """Constructor."""
        self.host = ''
        self.port = 0
        self.socket = None
        self.sender_comp_id = None
        self.target_comp_id = None
        self.username = ''
        self.password = ''
        self.do_auto_heartbeat = True
        self.history = None
        self.message_validator = None
        self.workflow_validator = None
        return

    def connect(self):
        """Connect to peer socket."""
        return

    def disconnect(self):
        """Disconnect from peer socket."""
        return

    def send(self):
        """Send a message to the peer entity."""
        return

    def received_count(self):
        """Get the number of unread messages received."""
        return 0

    def recv(self):
        """Get a received message."""
        return



class ServerSession(Session):
    pass

class AcceptedSession(Session):
    pass


class SessionSet(object):
    """This is basically the model for the session list."""
    pass


class SessionHistory(object):
    """This is basically the model for the session history panel."""
    pass


class SessionSetPersistor(object):
    """An interface offered by things that can save a session set."""
    pass

class SessionSetSqlitePersistor(SessionSetPersistor):
    """An implementation of session set persistence using Sqlite3."""
    pass


class Dispatcher(object):
    """Dispatch message handlers for events from GUI / API."""
    pass

