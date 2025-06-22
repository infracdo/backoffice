from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from main import models
from main.library.common import common
from main.library.mailer import mailer
from main.schemas.common import PostResponse
from main.core.config import Settings

settings = Settings()

class AuthController:

    def sign_in(
        self,
        db: Session,
        credentials: dict
    ):
        user = (
            db.query(models.User)
            .filter(
                 models.User.deleted_at == None,
                 models.User.email == credentials["email"]).first()
        )
        if not user:
             return PostResponse(
                status="error",
                status_code=401,
                message="Invalid email or password."
            ).__dict__
        verified = common.verify_password(
            password=credentials["password"], 
            hashed_password=user.password
        )
        if not verified:
            return PostResponse(
                status="error",
                status_code=401,
                message="Invalid email or password."
            ).__dict__

        if not user.is_active:
            return PostResponse(
                status="error",
                status_code=403,
                message="Access denied. Account is currently deactivated",
            ).__dict__

        time_now = common.get_timestamp(1)
        token = common.generate_jwt(jsonable_encoder(user))

        user.last_login = time_now
        db.commit()
        db.refresh(user)

        return PostResponse(
            status="ok",
            status_code=200,
            message="Login successful",
            data={
                "user": jsonable_encoder(user),
                "token": token
            }
        ).__dict__
        
    
    def forgot_password(
        self,
        db: Session,
        email: str
    ):

        time_now = common.get_timestamp(1)
        if settings.MANDRILL_API and settings.MANDRILL_NAME \
            and settings.MANDRILL_EMAIL:
            mailer.set_api_key(
                api_key=settings.MANDRILL_API, 
                from_name=settings.MANDRILL_NAME, 
                from_email=settings.MANDRILL_EMAIL,
            )

        user = (
            db.query(models.User)
            .filter(
                 models.User.deleted_at == None,
                 models.User.email == email).first()
        )
        if not user:
            return PostResponse(
                status="error",
                status_code=401,
                message="User not found",
            ).__dict__

        tmp_password = common.generate_temporary_password()
        new_password = common.generate_hashed_password(
            password_str=tmp_password
        )
        user.password = new_password
        user.updated_at = time_now

        # EMAIL NEW TEMPORARY PASSWORD
        subject = "Password Reset"
        msg = f"""
            Hi {user.name}!\n\nYour new temporary password is: {tmp_password}\n\nThank You\n\n{settings.MANDRILL_NAME}
        """
        mailer.send_mail(
            to_email=email,
            subject=subject,
            message=msg
        )

        # UPDATE
        db.commit()

        return PostResponse(
            status="ok", 
            status_code=200,
            message="If an account with that email exists, a temporary password has been sent."
        ).__dict__
        
    
    def change_password(
        self,
        db: Session,
        current_user: dict,
        payload: dict
    ):

        user = (
            db.query(models.User)
            .filter(
                models.User.deleted_at == None,
                models.User.user_id == current_user["user_id"]
            )
        )
        if not user:
            return PostResponse(
                status="error",
                status_code=401,
                message="User not found",
            ).__dict__

        if not (common.verify_password(
            password=payload["old_password"], hashed_password=user.password
        )):
            return PostResponse(
                status="error", 
                status_code=401,
                message="Incorrect password."
            ).__dict__

        user.password = common.generate_hashed_password(
            password_str=payload["new_password"]
        )
        db.commit()
        
        return PostResponse(
            status="ok", 
            status_code=200,
            message="Password changed successfully"
        ).__dict__
