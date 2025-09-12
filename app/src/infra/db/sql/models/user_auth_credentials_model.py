from app.src.infra.mixins.update_from_schema import UpdateFromSchemaMixin
from app.src.infra.db.sql.database import Base
from sqlalchemy import Column, Integer, Text, DateTime
import uuid

class UserAuthCredentialsModel(UpdateFromSchemaMixin, Base):
    __tablename__ = "user_auth_credentials"

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True, index=True)
    device_id = Column(Text, nullable=False, default=lambda: uuid.uuid4().hex)
    email = Column(Text, nullable=False)
    access_token = Column(Text, nullable=False)
    access_expiry = Column(DateTime, nullable=False)
    refresh_token = Column(Text, nullable=False)
    refresh_expiry = Column(DateTime, nullable=False)
    token_type = Column(Text, nullable=False)
