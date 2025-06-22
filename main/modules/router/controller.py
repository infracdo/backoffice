import jwt
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String
from main import models
from main.library.common import common
from main.schemas.common import PostResponse, GetResponse, GetResponseWithDataUsage
from main.core.config import Settings
from typing import Optional

settings = Settings()

class RouterController:

    def create_router(
        self,
        db: Session,
        current_user: dict,
        payload: dict
    ):

        existing_serial = (
            db.query(models.Router)
            .filter(models.Router.serial_no == payload["serial_no"]).first()
        )
        if existing_serial:
            return PostResponse(
                status="error",
                status_code=400,
                message="Serial No. already registered"
            ).__dict__

        time_now = common.get_timestamp(1)
        new_router = models.Router(
            serial_no=payload["serial_no"],
            router_model=payload["router_model"],
            router_version=payload["router_version"],
            long=payload["long"],
            lat=payload["lat"],
            owner_user_id=current_user.get("user_id"),
            router_id=common.uuid_generator(),
            created_at=time_now,
            updated_at=time_now
        )
        db.add(new_router)
        db.commit()
        db.refresh(new_router)

        return PostResponse(
            status="ok",
            status_code=200,
            message="Router created successfully",
            data={
                "router": jsonable_encoder(new_router)
            }
        ).__dict__
        
    
    def update_router(
        self,
        db: Session,
        payload: dict
    ):

        router = (
            db.query(models.Router)
            .filter_by(router_id=payload["router_id"])
            .one_or_none()
        )
        if not router:
            return PostResponse(
                status="error",
                status_code=400,
                message="Router not found"
            ).__dict__
        

        router_data = jsonable_encoder(router)
        if isinstance(payload, dict):
            update_data = payload
        else:
            update_data = payload.dict(exclude_unset=True)
        update_data["updated_at"] = common.get_timestamp(1)
        for field in router_data:
            if field in update_data:
                setattr(router, field, update_data[field])

        db.commit()
        db.refresh(router)

        return PostResponse(
            status="ok",
            status_code=200,
            message="Router successfully updated",
            data={
                "router": jsonable_encoder(router)
            }
        ).__dict__

    
    def router_list(
        self,
        db: Session,
        payload: dict,
        with_total_data_usage: bool,
        with_total_subscribers: bool,
        search: Optional[str] = None
    ):
        limit = payload.get("limit",9999999)
        page = payload.get("page",1)
        filters = [
            models.Router.deleted_at == None
        ]
        if payload.get("id"):
            filters.append(models.Router.router_id == payload.get("id"))
        if search: 
            filters.append(
                or_(
                    models.Router.serial_no.ilike(f"%{search}%"),
                    models.Router.router_model.ilike(f"%{search}%"),
                    models.Router.router_version.ilike(f"%{search}%"),
                    cast(models.Router.data_usage, String).ilike(search),
                    cast(models.Router.subscribers_count, String).ilike(search),
                    models.User.name.ilike(f"%{search}%"),
                )
            )
        # get total rows count
        data = db.query(models.Router).filter(*filters)
        total_rows = data.count()
        # get total data usage
        total_data_usage = 0
        if with_total_data_usage:
            total_data_usage = sum((r.data_usage or 0) for r in data)
         # get total data usage
        total_subscribers = 0
        if with_total_subscribers:
            total_subscribers = sum((r.subscribers_count or 0) for r in data)

        limit = int(limit) if limit else 0
        page = int(page) if page else 0
        offset = (page - 1) * limit if limit and page else None

        results = (
            db.query(models.Router, models.User.name.label("business_owner_name"))
            .join(models.User, models.Router.owner_user_id == models.User.user_id)
            .filter(*filters)
            .order_by(models.Router.updated_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        routers = []
        for router, business_owner_name in results:
            router_dict = router.__dict__.copy()
            router_dict["business_owner_name"] = business_owner_name
            router_dict.pop("_sa_instance_state", None)
            routers.append(router_dict)

        ret = GetResponse(
                status="ok",
                status_code=200,
                data=jsonable_encoder(routers),
                total_rows=total_rows
            ).__dict__
        

        if with_total_data_usage:
            ret["total_data_usage"] = total_data_usage
        if with_total_subscribers:
            ret["total_subscribers"] = total_subscribers
        
        return ret
            
    
    def download_router_list(
        self,
        db: Session,
        filename: str,
        file_type: str,
        search: Optional[str] = None
    ):
        filters = [
            models.Router.deleted_at == None
        ]
        if search: 
            filters.append(
                or_(
                    models.Router.serial_no.ilike(f"%{search}%"),
                    models.Router.router_model.ilike(f"%{search}%"),
                    models.Router.router_version.ilike(f"%{search}%"),
                    cast(models.Router.data_usage, String).ilike(search),
                    cast(models.Router.subscribers_count, String).ilike(search),
                    models.User.name.ilike(f"%{search}%"),
                )
            )
        results = (
            db.query(models.Router, models.User.name.label("business_owner_name"))
            .join(models.User, models.Router.owner_user_id == models.User.user_id)
            .filter(*filters)
            .order_by(models.Router.updated_at.desc())
            .all()
        )

        routers = []
        for router, business_owner_name in results:
            router_dict = router.__dict__.copy()
            router_dict["business_owner_name"] = business_owner_name
            router_dict.pop("_sa_instance_state", None)
            routers.append(router_dict)

        keys = (
            "created_at",
            "updated_at",
            "business_owner_name",
            "serial_no",
            "router_model",
            "router_version",
            "data_usage",
            "subscribers_count",
            "long",
            "lat",
            "is_enabled"
        )
        headers = (
            "Date Created",
            "Date Updated",
            "Business Owner",
            "Serial No",
            "Router Model",
            "Router Version",
            "Data Usage",
            "Subscribers Count",
            "Longitude",
            "Latitude",
            "Enabled"
        )

        raw_data = {
            "header": keys,
            "headers": headers,
            "rows": jsonable_encoder(routers)
        }
        data = common.format_excel(rawData=raw_data)
        return common.get_media_return(
            file_name=filename,
            file_type=file_type,
            data=data,
        )
    
    def delete_router(
        self,
        db: Session,
        id: str
    ):

        router = (
            db.query(models.Router)
            .filter_by(router_id=id)
            .one_or_none()
        )
        if not router:
            return PostResponse(
                status="error",
                status_code=400,
                message="Router not found"
            ).__dict__
    
        router.deleted_at= common.get_timestamp(1)
        db.commit()

        return PostResponse(
            status="ok",
            status_code=200,
            message="Router successfully deleted"
        ).__dict__