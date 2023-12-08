from sqlalchemy.orm import Session


class BaseDbService:

    def __init__(self, session: Session) -> None:
        self.session = session
