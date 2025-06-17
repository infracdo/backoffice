import jwt
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from main import models
from main.library.common import common
from main.schemas.common import PostResponse, GetResponse, GetResponseWithDataUsage
from main.core.config import Settings

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
        with_data_usage: bool
    ):
        limit = payload.get("limit",9999999)
        page = payload.get("page",1)
        filters = [
            models.Router.deleted_at == None
        ]
        if payload.get("id"):
            filters.append(models.Router.router_id == payload.get("id"))

        # get total rows count
        data = db.query(models.Router).filter(*filters)
        total_rows = data.count()
        # get total data usage
        total_data_usage = 0
        if with_data_usage:
            total_data_usage = sum((r.data_usage or 0) for r in data)

        limit = int(limit) if limit else 0
        page = int(page) if page else 0
        offset = (page - 1) * limit if limit and page else None

        routers = (
            db.query(
                models.Router
            )
            .filter(*filters)
            .order_by(models.Router.updated_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        if with_data_usage:
            return GetResponseWithDataUsage(
                status="ok",
                status_code=200,
                data=jsonable_encoder(routers),
                total_rows=total_rows,
                total_data_usage=total_data_usage
            ).__dict__
        else:
            return GetResponse(
                status="ok",
                status_code=200,
                data=jsonable_encoder(routers),
                total_rows=total_rows
            ).__dict__
            
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