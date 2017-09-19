
class Session(object):
    """Base class for FIX sessions."""
    pass


class ClientSession(Session):
    """An outbound client session."""

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
        self.recv_queue = []
        return

    def connect(self):
        """Connect to peer socket."""

        if self.socket:
            raise RuntimeError()
        return

    def disconnect(self):
        """Disconnect from peer socket."""
        if not self.socket:
            raise RuntimeError()
        return

    def send(self):
        """Send a message to the peer entity."""
        if not self.socket:
            raise RuntimeError()
        return

    def received_count(self):
        """Get the number of unread messages received."""
        return len(self.recv_queue)

    def recv(self):
        """Get a received message."""

        if not self.recv_queue:
            return None

        return



class ServerSession(Session):
    """An advertised server endpoint."""
    pass


class AcceptedSession(Session):
    """A live session, accepted via a server session."""
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

