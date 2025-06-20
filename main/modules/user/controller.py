import random
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from main import models
from main.library.common import common
from main.schemas.common import PostResponse, GetResponse
from typing import Optional

class UserController:

    def user_types(
        self,
        db: Session,
        payload: dict
    ):
        limit = payload.get("limit",9999999)
        page = payload.get("page",1)

        filters = [
            models.UserRole.deleted_at == None
        ]
        if payload.get("id"):
            filters.append(models.UserRole.type == payload.get("id"))

        # get total rows count
        data = db.query(models.UserRole).filter(*filters)
        total_rows = data.count()

        limit = int(limit) if limit else 0
        page = int(page) if page else 0
        offset = (page - 1) * limit if limit and page else None

        roles = (
            db.query(
                models.UserRole
            )
            .filter(*filters)
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
    

    def subscriber_tiers(
        self,
        db: Session,
        payload: dict
    ):
        filters = [
            models.Tier.deleted_at == None
        ]
        limit = payload.get("limit",9999999)
        page = payload.get("page",1)
        if payload.get("id"):
            filters.append(models.Tier.tier_id == payload.get("id"))

        # get total rows count
        data = db.query(models.Tier).filter(*filters)
        total_rows = data.count()

        limit = int(limit) if limit else 0
        page = int(page) if page else 0
        offset = (page - 1) * limit if limit and page else None

        tiers = (
            db.query(
                models.Tier
            )
            .filter(*filters)
            .order_by(models.Tier.updated_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        return GetResponse(
            status="ok",
            status_code=200,
            data=jsonable_encoder(tiers),
            total_rows=total_rows
        ).__dict__
    
    
    def create_subscriber_tier(
        self,
        db: Session,
        payload: dict
    ):

        time_now = common.get_timestamp(1)
        new_tier = models.Tier(
            name=payload["name"],
            description=payload["description"],
            data_limit=payload["data_limit"],
            tier_id=common.small_letter_no_space(payload["name"]),
            created_at=time_now,
            updated_at=time_now
        )
        db.add(new_tier)
        db.commit()
        db.refresh(new_tier)

        return PostResponse(
            status="ok",
            status_code=200,
            message="Tier created successfully",
            data={
                "tier": jsonable_encoder(new_tier)
            }
        ).__dict__


    def update_subscriber_tier(
        self,
        db: Session,
        payload: dict
    ):

        tier = (
            db.query(models.Tier)
            .filter_by(tier_id=payload["tier_id"])
            .one_or_none()
        )
        if not tier:
            return PostResponse(
                status="error",
                status_code=400,
                message="Tier not found"
            ).__dict__
        

        tier_data = jsonable_encoder(tier)
        if isinstance(payload, dict):
            update_data = payload
        else:
            update_data = payload.dict(exclude_unset=True)
        update_data["updated_at"] = common.get_timestamp(1)
        for field in tier_data:
            if field in update_data:
                setattr(tier, field, update_data[field])
        
        db.commit()
        db.refresh(tier)

        return PostResponse(
            status="ok",
            status_code=200,
            message="Tier successfully updated",
            data={
                "tier": jsonable_encoder(tier)
            }
        ).__dict__


    def delete_subscriber_tier(
        self,
        db: Session,
        id: str
    ):

        if id == "tier1":
            return PostResponse(
                status="error",
                status_code=400,
                message="Tier cannot be deleted"
            ).__dict__

        tier = (
            db.query(models.Tier)
            .filter_by(tier_id=id)
            .one_or_none()
        )
        if not tier:
            return PostResponse(
                status="error",
                status_code=400,
                message="Tier not found"
            ).__dict__
    
        tier.deleted_at= common.get_timestamp(1)
        db.commit()

        return PostResponse(
            status="ok",
            status_code=200,
            message="Tier successfully deleted"
        ).__dict__
   
   
    def create_user(
        self,
        db: Session,
        payload: dict
    ):

        is_subscriber = payload["user_type"] == "subscriber"
        new_subscriber_tier = None
        data_limit = None
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

        roles = db.query(models.UserRole).all()
        role_names = [r.type for r in roles]

        if not (payload["user_type"] in role_names):
            return PostResponse(
                status="error",
                status_code=400,
                message="Invalid user_type"
            ).__dict__

        if is_subscriber:
            tier_data = (
                db.query(models.Tier)
                .filter(models.Tier.is_default_tier == True).first()
            )
            data_limit = tier_data.data_limit if tier_data else 51200
            new_subscriber_tier = tier_data.tier_id if tier_data else None


        time_now = common.get_timestamp(1)
        new_user = models.User(
            name=payload["name"],
            email=payload["email"],
            mobile_no=payload["mobile_no"],
            user_type=payload["user_type"],
            device_id=payload.get("device_id"),
            data_limit=data_limit,
            tier=new_subscriber_tier if is_subscriber else None,
            is_active=payload.get("is_active", True),
            password=common.generate_hashed_password(
                password_str=payload["password"]
            ),
            user_id=common.uuid_generator(),
            last_login=time_now if payload.get("will_return_token") else None,
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

        if payload.get("will_return_token"):
            token = common.generate_jwt(jsonable_encoder(new_user))
            data["access_token"] = token
            message = "Signup successful"

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
        payload: dict,
        user_types: Optional[str] = None
    ):
        filters = [
            models.User.deleted_at == None
        ]
        if user_types:
            user_type_list = [t.strip() for t in user_types.split(",") if t.strip()]
            if user_type_list:
                filters.append(models.User.user_type.in_(user_type_list))
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