from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from main import models
from main.library.common import common
from main.schemas.common import PostResponse, GetResponse
from main.core.config import Settings

settings = Settings()

class SubscriberController:

    def create_subscriber(
        self,
        db: Session,
        current_user: dict,
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

        time_now = common.get_timestamp(1)
        new_subscriber = models.Subscriber(
            router_id=payload["router_id"],
            subscriber_id=common.uuid_generator(),
            user_id=current_user.get("user_id"),
            created_at=time_now,
            updated_at=time_now
        )
        db.add(new_subscriber)
        router.subscribers_count += 1

        db.commit()
        db.refresh(new_subscriber)
        subscriber = jsonable_encoder(new_subscriber)
        db.commit()

        return PostResponse(
            status="ok",
            status_code=200,
            message="Subscriber created successfully",
            data={
                "subscriber": subscriber
            }
        ).__dict__
        
    
    def update_subscriber(
        self,
        db: Session,
        payload: dict
    ):

        subscriber = (
            db.query(models.Subscriber)
            .filter_by(subscriber_id=payload["subscriber_id"])
            .one_or_none()
        )
        if not subscriber:
            return PostResponse(
                status="error",
                status_code=400,
                message="Subscriber not found"
            ).__dict__
        

        subscriber_data = jsonable_encoder(subscriber)
        if isinstance(payload, dict):
            update_data = payload
        else:
            update_data = payload.dict(exclude_unset=True)
        update_data["updated_at"] = common.get_timestamp(1)
        for field in subscriber_data:
            if field in update_data:
                setattr(subscriber, field, update_data[field])

        db.commit()
        db.refresh(subscriber)

        return PostResponse(
            status="ok",
            status_code=200,
            message="Subscriber successfully updated",
            data={
                "subscriber": jsonable_encoder(subscriber)
            }
        ).__dict__

    
    def subscriber_list(
        self,
        db: Session,
        payload: dict
    ):
        limit = payload.get("limit",9999999)
        page = payload.get("page",1)
        filters = [
            models.Subscriber.deleted_at == None
        ]
        if payload.get("id"):
            filters.append(models.Subscriber.subscriber_id == payload.get("id"))

        # get total rows count
        data = db.query(models.Subscriber).filter(*filters)
        total_rows = data.count()

        limit = int(limit) if limit else 0
        page = int(page) if page else 0
        offset = (page - 1) * limit if limit and page else None

        subscribers = (
            db.query(
                models.Subscriber
            )
            .filter(*filters)
            .order_by(models.Subscriber.updated_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        return GetResponse(
            status="ok",
            status_code=200,
            data=jsonable_encoder(subscribers),
            total_rows=total_rows
        ).__dict__

    
    def subscriber_list_by_router_ownerself(
        db: Session,
        payload: dict
    ):
        filters = [
            models.Subscriber.deleted_at == None,
            models.Router.owner_user_id == payload["owner_user_id"],
        ]
        
        # get total rows count
        data = (
            db.query(models.Subscriber)
            .join(models.Router, models.Subscriber.router_id==models.Router.router_id)
            .filter(*filters)
        )
        total_rows = data.count()

        limit = int(limit) if limit else 0
        page = int(page) if page else 0
        offset = (page - 1) * limit if limit and page else None

        subscribers = (
            db.query(
                models.Subscriber
            )
            .join(models.Router, models.Subscriber.router_id==models.Router.router_id)
            .filter(*filters)
            .order_by(models.Subscriber.updated_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        return GetResponse(
            status="ok",
            status_code=200,
            data=jsonable_encoder(subscribers),
            total_rows=total_rows
        ).__dict__


    def delete_subscriber(
        self,
        db: Session,
        id: str
    ):

        subscriber = (
            db.query(models.Subscriber)
            .filter_by(subscriber_id=id)
            .one_or_none()
        )
        if not subscriber:
            return PostResponse(
                status="error",
                status_code=400,
                message="Subscriber not found"
            ).__dict__
    
        subscriber.deleted_at= common.get_timestamp(1)
        db.commit()

        return PostResponse(
            status="ok",
            status_code=200,
            message="Subscriber successfully deleted"
        ).__dict__