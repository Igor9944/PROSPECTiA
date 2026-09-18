from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr

class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = None  # type: ignore

Base = declarative_base(cls=Base)
