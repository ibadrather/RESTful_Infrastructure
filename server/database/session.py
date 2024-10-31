from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseSession:
    """Manages database connections and provides session instances.

    Attributes:
        engine (Engine): SQLAlchemy engine connected to the database.
        SessionLocal (sessionmaker): Factory for creating new SQLAlchemy sessions.

    Methods:
        get_session: Provides a new session instance with resource management.
    """

    def __init__(self, connection_string: str):
        """Initializes DatabaseSession with a database connection string.

        Args:
            connection_string (str): The database URI for connecting to the database.
        """
        self.engine = create_engine(connection_string)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self):
        """Creates and provides a new session instance.

        Yields:
            Session: A new SQLAlchemy session instance.
        """
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()
