import random
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String
from main import models
from main.library.common import common
from main.schemas.common import PostResponse, GetResponse
from typing import Optional
from collections import defaultdict

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
        payload: dict,
        search: Optional[str] = None
    ):
        filters = [
            models.Tier.deleted_at == None
        ]
        limit = payload.get("limit",9999999)
        page = payload.get("page",1)
        if payload.get("id"):
            filters.append(models.Tier.tier_id == payload.get("id"))

        if search: 
            filters.append(
                or_(
                    models.Tier.name.ilike(f"%{search}%"),
                    models.Tier.description.ilike(f"%{search}%"),
                    cast(models.Tier.data_limit, String).ilike(search),
                )
            )

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
    
    
    def download_tier_list(
        self,
        db: Session,
        filename: str,
        file_type: str,
        search: Optional[str] = None
    ):
        filters = [
            models.Tier.deleted_at == None
        ]
        
        if search: 
            filters.append(
                or_(
                    models.Tier.name.ilike(f"%{search}%"),
                    models.Tier.description.ilike(f"%{search}%"),
                    cast(models.Tier.data_limit, String).ilike(search),
                )
            )

        tiers = (
            db.query(
                models.Tier
            )
            .filter(*filters)
            .order_by(models.Tier.updated_at.desc())
            .all()
        )


        keys = (
            "created_at",
            "updated_at",
            "name",
            "description",
            "data_limit",
            "is_default_tier"
        )
        headers = (
            "Date Created",
            "Date Updated",
            "Tier Name",
            "Description",
            "Data Limit",
            "Default"
        )

        raw_data = {
            "header": keys,
            "headers": headers,
            "rows": jsonable_encoder(tiers)
        }
        data = common.format_excel(rawData=raw_data)
        return common.get_media_return(
            file_name=filename,
            file_type=file_type,
            data=data,
        )
    
    
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
            .filter(
                models.User.deleted_at == None,
                models.User.email == payload["email"]
            ).first()
        )
        if existing_email:
            return PostResponse(
                status="error",
                status_code=400,
                message="Email already registered"
            ).__dict__
        existing_mobile = (
            db.query(models.User)
            .filter(
                models.User.deleted_at == None,
                models.User.mobile_no == payload["mobile_no"]
            ).first()
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
        user_types: Optional[str] = None,
        search: Optional[str] = None,
    ):
        filters = [
            models.User.deleted_at == None
        ]
        if user_types:
            user_type_list = [t.strip() for t in user_types.split(",") if t.strip()]
            if user_type_list:
                filters.append(models.User.user_type.in_(user_type_list))

        if search: 
            if user_types == "admin,support":
                filters.append(
                    or_(
                        models.User.name.ilike(f"%{search}%"),
                        models.User.email.ilike(f"%{search}%"),
                        models.User.mobile_no.ilike(f"%{search}%"),
                        models.User.user_type.ilike(f"%{search}%"),
                        cast(models.User.created_at, String).ilike(search),
                    )
                )
            elif user_types == "business_owner":
                filters.append(
                    or_(
                        models.User.name.ilike(f"%{search}%"),
                        models.User.email.ilike(f"%{search}%"),
                        models.User.mobile_no.ilike(f"%{search}%"),
                        cast(models.User.created_at, String).ilike(search),
                    )
                )
            else :
                filters.append(
                    or_(
                        models.User.name.ilike(f"%{search}%"),
                        models.User.email.ilike(f"%{search}%"),
                        models.User.mobile_no.ilike(f"%{search}%"),
                        models.User.device_id.ilike(f"%{search}%"),
                        cast(models.User.data_limit, String).ilike(search),
                        cast(models.User.data_usage, String).ilike(search),
                        models.User.tier.ilike(f"%{search}%"),
                        cast(models.User.created_at, String).ilike(search),
                    )
                )

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

        if user_types == "business_owner":
            user_ids = [user.user_id for user in users]

            routers = (
                db.query(
                    models.Router
                )
                .filter(
                    models.Router.deleted_at == None,
                    models.Router.owner_user_id.in_(user_ids))
                .order_by(models.Router.updated_at.desc())
                .all()
            )

            router_map = defaultdict(list)
            for router in routers:
                router_map[router.owner_user_id].append(router)

            # Attach routers to each user
            for user in users:
                user_routers = router_map.get(user.user_id, [])
                user.routers = user_routers
                user.total_routers = len(user_routers)
                user.total_data_usage = sum(router.data_usage or 0 for router in user_routers)
                user.total_subscribers = sum(router.subscribers_count or 0 for router in user_routers)


        return GetResponse(
            status="ok",
            status_code=200,
            data=jsonable_encoder(users) if users else [],
            total_rows=total_rows
        ).__dict__


    def download_user_list(
        self,
        db: Session,
        filename: str,
        file_type: str,
        user_id: Optional[str] = None,
        user_types: Optional[str] = None,
        search: Optional[str] = None
    ):
        filters = [
            models.User.deleted_at == None
        ]
        if user_id:
            filters.append(models.User.user_id == user_id)
        if user_types:
            user_type_list = [t.strip() for t in user_types.split(",") if t.strip()]
            if user_type_list:
                filters.append(models.User.user_type.in_(user_type_list))
        if search: 
            if user_types == "admin,support":
                filters.append(
                    or_(
                        models.User.name.ilike(f"%{search}%"),
                        models.User.email.ilike(f"%{search}%"),
                        models.User.mobile_no.ilike(f"%{search}%"),
                        models.User.user_type.ilike(f"%{search}%"),
                        cast(models.User.created_at, String).ilike(search),
                    )
                )
            elif user_types == "business_owner":
                filters.append(
                    or_(
                        models.User.name.ilike(f"%{search}%"),
                        models.User.email.ilike(f"%{search}%"),
                        models.User.mobile_no.ilike(f"%{search}%"),
                        cast(models.User.created_at, String).ilike(search),
                    )
                )
            else :
                filters.append(
                    or_(
                        models.User.name.ilike(f"%{search}%"),
                        models.User.email.ilike(f"%{search}%"),
                        models.User.mobile_no.ilike(f"%{search}%"),
                        models.User.device_id.ilike(f"%{search}%"),
                        cast(models.User.data_limit, String).ilike(search),
                        cast(models.User.data_usage, String).ilike(search),
                        models.User.tier.ilike(f"%{search}%"),
                        cast(models.User.created_at, String).ilike(search),
                    )
                )

        users = (
            db.query(
                models.User
            )
            .filter(*filters)
            .order_by(models.User.updated_at.desc())
            .all()
        )

        if user_types == "business_owner":
            user_ids = [user.user_id for user in users]

            routers = (
                db.query(
                    models.Router
                )
                .filter(
                    models.Router.deleted_at == None,
                    models.Router.owner_user_id.in_(user_ids))
                .order_by(models.Router.updated_at.desc())
                .all()
            )

            router_map = defaultdict(list)
            for router in routers:
                router_map[router.owner_user_id].append(router)

            # Attach routers to each user
            for user in users:
                user_routers = router_map.get(user.user_id, [])
                user.total_routers = len(user_routers)
                user.total_data_usage = sum(router.data_usage or 0 for router in user_routers)
                user.total_subscribers = sum(router.subscribers_count or 0 for router in user_routers)


        keys = (
            "created_at",
            "updated_at",
            "name",
            "email",
            "mobile_no",
            "is_active",
            "user_type",
        )
        headers = (
            "Date Created",
            "Date Updated",
            "Full Name",
            "Email Address",
            "Mobile No",
            "Active",
            "Type"
        )

        if user_types == "subscriber":
            keys += ("device_id","data_limit","data_usage","tier")
            headers += ("Device ID","Data Limit","Data Usage","Tier")
        
        if user_types == "business_owner":
            keys += ("total_routers","total_data_usage","total_subscribers")
            headers += ("Total Routers","Total Data Usage", "Total Subscribers")

        raw_data = {
            "header": keys,
            "headers": headers,
            "rows": jsonable_encoder(users)
        }
        data = common.format_excel(rawData=raw_data)
        return common.get_media_return(
            file_name=filename,
            file_type=file_type,
            data=data,
        )

    
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



    def check_by_mobile(
        self,
        db: Session,
        mobile_no: str
    ):

        user = (
            db.query(models.User)
            .filter(
                models.User.deleted_at == None,
                models.User.mobile_no == mobile_no
            )
            .one_or_none()
        )
        if not user:
            return PostResponse(
                status="error",
                status_code=400,
                message="User not found"
            ).__dict__

        else:
            return PostResponse(
                status="ok",
                status_code=200,
                message="User  found",
                data=jsonable_encoder(user)
            ).__dict__