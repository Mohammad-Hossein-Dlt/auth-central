from repo.interface.Iauth import IAuthRepo
from fastapi import Request, Response
from sqlalchemy.orm import Session
from domain.schemas.auth.auth_credentials import AuthCredentials
from infra.db.sql.models.user_auth_credentials_model import UserAuthCredentialsModel

class AuthSQLRepo(IAuthRepo):
    
    def __init__(
        self,
        request: Request,
        response: Response,
        db: Session,
    ):
        
        self.request = request
        self.response = response   
        self.db = db
        
    def save_user_auth_credentials(
        self,
        credentials: AuthCredentials,
    ) -> AuthCredentials:
                
        existing_credentials = self.get_user_auth_credentials()
                
        if existing_credentials:
            record = self.db.merge(UserAuthCredentialsModel(**existing_credentials.model_dump()))
            record.update_from_schema(credentials)
        else:
            record = UserAuthCredentialsModel(**credentials.model_dump(exclude_unset=True))
            self.db.add(record)

        self.db.commit()

        self.request.session["device_id"] = record.device_id
                
        return AuthCredentials.model_validate(record, from_attributes=True)

    def get_user_auth_credentials(
        self,
    ) -> AuthCredentials | None:
        
        device_id = self.request.session.get("device_id")
                
        existing_credentials = self.db.query(
            UserAuthCredentialsModel
        ).where(
            UserAuthCredentialsModel.device_id == device_id,
        ).first()
                
        if not existing_credentials:
            return None
                
        return AuthCredentials.model_validate(existing_credentials, from_attributes=True)
    