import jwt
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from main import models
from main.schemas.dashboard import GetCountsResponse, GetOnlinesResponse
from main.schemas.common import PostResponse
from main.library.common import common


class DashboardController:

    def get_count(
        self,
        db: Session,
        payload: dict,
    ):
        filters = [
            models.Router.deleted_at == None
        ]
        total_business_owners = 0
        if payload.get("owner_user_id"):
            filters.append(models.Router.owner_user_id == payload.get("owner_user_id"))
            total_business_owners = 1
        

        data = db.query(models.Router).filter(*filters)
        total_routers = data.count()
        # total_data_usage = sum((r.data_usage or 0) for r in data)
        total_subscribers = sum((r.subscribers_count or 0) for r in data)

        
        owners = db.query(models.User).filter(*[
            models.User.deleted_at == None,
            models.User.user_type == "business_owner"
        ])
        total_business_owners = owners.count()

        return GetCountsResponse(
            status="ok",
            status_code=200,
            total_business_owners=total_business_owners,
            total_routers=total_routers,
            total_subscribers=total_subscribers
            # total_data_usage=total_data_usage,
        ).__dict__


    def get_online(
        self,
        db: Session
    ):

        data = (
            db.query(models.Dashboard)
            .filter(models.Dashboard.type=="online-dashboard")
            .one_or_none()
        )
        if not data:
            return PostResponse(
                status="error",
                status_code=400,
                message="Dashboard entry not found"
            ).__dict__

        return GetOnlinesResponse(
            status="ok",
            status_code=200,
            total_online_subscriber=data.total_online_subscriber,
            total_online_router=data.total_online_router,
            total_data_usage=data.total_data_usage
        ).__dict__


    def update_realtime_data(
        self,
        db: Session,
        payload: dict
    ):

        data = (
            db.query(models.Dashboard)
            .filter(models.Dashboard.type=="online-dashboard")
            .one_or_none()
        )
        if not data:
            return PostResponse(
                status="error",
                status_code=400,
                message="Dashboard entry not found"
            ).__dict__
        
        data.total_online_subscriber = payload["total_online_subscriber"]
        data.total_online_router = payload["total_online_router"]
        data.total_data_usage = payload["total_data_usage"]
        data.last_updated_at = common.get_timestamp(1)

        db.commit()
        db.refresh(data)        

        return PostResponse(
            status="ok",
            status_code=200,
            message="Dashboard data successfully updated",
            data=jsonable_encoder(data)
        ).__dict__

    