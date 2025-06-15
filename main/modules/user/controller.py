from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from main import models
from main.library.common import common
from main.schemas.common import PostResponse, GetResponse
from main.core.config import Settings

settings = Settings()

class UserController:

    def user_types(
        self,
        db: Session,
        payload: dict
    ):
        limit = payload.get("limit",9999999)
        page = payload.get("page",1)

        # get total rows count
        data = db.query(models.UserRole)
        total_rows = data.count()

        limit = int(limit) if limit else 0
        page = int(page) if page else 0
        offset = (page - 1) * limit if limit and page else None

        roles = (
            db.query(
                models.UserRole
            )
            .limit(limit)
            .offset(offset)
            .all()
        )

        return GetResponse(
            status="ok",
            status_code=200,
            data=jsonable_encoder(roles),
            total_rows=total_rows
        )
    

    def create_user(
        self,
        db: Session,
        payload: dict
    ):

        existing_email = (
            db.query(models.User)
            .filter(models.User.email == payload["email"]).first()
        )
        if existing_email:
            return PostResponse(
                status="error",
                status_code=400,
                message="Email already registered"
            ).__dict__
        existing_mobile = (
            db.query(models.User)
            .filter(models.User.mobile_no == payload["mobile_no"]).first()
        )
        if existing_mobile:
            return PostResponse(
                status="error",
                status_code=400,
                message="Mobile number already registered"
            ).__dict__

        time_now = common.get_timestamp(1)
        new_user = models.User(
            name=payload["name"],
            email=payload["email"],
            mobile_no=payload["mobile_no"],
            user_type=payload["user_type"],
            is_active=payload["is_active"],
            password=common.generate_hashed_password(
                password_str=payload["password"]
            ),
            user_id=common.uuid_generator(),
            last_login=time_now if payload["will_return_token"] else None,
            created_at=time_now,
            updated_at=time_now
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        data = {
            "user": jsonable_encoder(new_user)
        }
        message = "User created successfully"

        if payload["will_return_token"]:
            token = common.generate_jwt(jsonable_encoder(new_user))
            data["access_token"] = token
            message = "Login successful"

        return PostResponse(
            status="ok",
            status_code=200,
            message=message,
            data=data
        ).__dict__
        
    
    def update_user(
        self,
        db: Session,
        payload: dict
    ):

        user = (
            db.query(models.User)
            .filter_by(user_id=payload["user_id"])
            .one_or_none()
        )
        if not user:
            return PostResponse(
                status="error",
                status_code=400,
                message="User not found"
            ).__dict__
        

        user_data = jsonable_encoder(user)
        if isinstance(payload, dict):
            update_data = payload
        else:
            update_data = payload.dict(exclude_unset=True)
        update_data["updated_at"] = common.get_timestamp(1)
        for field in user_data:
            if field in update_data:
                setattr(user, field, update_data[field])
        
        db.commit()
        db.refresh(user)

        return PostResponse(
            status="ok",
            status_code=200,
            message="User successfully updated",
            data={
                "user": jsonable_encoder(user)
            }
        ).__dict__

    
    def user_list(
        self,
        db: Session,
        payload: dict
    ):
        filters = [
            models.User.deleted_at == None
        ]
        limit = payload.get("limit",9999999)
        page = payload.get("page",1)
        if payload.get("id"):
            filters.append(models.User.user_id == payload.get("id"))

        # get total rows count
        data = db.query(models.User).filter(*filters)
        total_rows = data.count()

        limit = int(limit) if limit else 0
        page = int(page) if page else 0
        offset = (page - 1) * limit if limit and page else None

        users = (
            db.query(
                models.User
            )
            .filter(*filters)
            .order_by(models.User.updated_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        return GetResponse(
            status="ok",
            status_code=200,
            data=jsonable_encoder(users),
            total_rows=total_rows
        ).__dict__


    def delete_user(
        self,
        db: Session,
        id: str
    ):

        user = (
            db.query(models.User)
            .filter_by(user_id=id)
            .one_or_none()
        )
        if not user:
            return PostResponse(
                status="error",
                status_code=400,
                message="User not found"
            ).__dict__
    
        user.deleted_at= common.get_timestamp(1)
        db.commit()

        return PostResponse(
            status="ok",
            status_code=200,
            message="User successfully deleted"
        ).__dict__