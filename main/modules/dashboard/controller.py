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
        totals = self.get_table_counts(db, id=payload.get("owner_user_id"))

        return GetCountsResponse(
            status="ok",
            status_code=200,
            total_business_owners=totals.get("total_business_owners"),
            total_routers=totals.get("total_routers"),
            total_subscribers=totals.get("total_subscribers")
        ).__dict__


    def get_online(
        self,
        db: Session
    ):

        data = jsonable_encoder(self.get_online_dashboard(db))
        if not data:
            return PostResponse(
                status="error",
                status_code=400,
                message="Dashboard entry not found"
            ).__dict__

        return GetOnlinesResponse(
            status="ok",
            status_code=200,
            total_online_subscriber=data.get("total_online_subscriber",0),
            total_online_router=data.get("total_online_router",0),
            total_data_usage=data.get("total_data_usage",0)
        ).__dict__


    def get_data(
        self,
        db: Session
    ):
        online = jsonable_encoder(self.get_online_dashboard(db))
        count = self.get_table_counts(db)

        return PostResponse(
            status="ok",
            status_code=200,
            data={
                "total_business_owners" : count.get("total_business_owners"),
                "total_routers": count.get("total_routers"),
                "total_subscribers": count.get("total_subscribers"),
                "total_online_subscriber": online.get("total_online_subscriber",0),
                "total_online_router": online.get("total_online_router",0),
                "total_data_usage": online.get("total_data_usage",0)
            }
        ).__dict__

    
    def update_realtime_data(
        self,
        db: Session,
        payload: dict
    ):

        data = (
            db.query(models.Dashboard)
            .filter(models.Dashboard.type=="online-dashboard")
            .first()
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

    
    def get_online_dashboard(self, db):
        return (
            db.query(models.Dashboard)
            .filter(models.Dashboard.type=="online-dashboard")
            .first()
        )

    
    def get_table_counts(self,db,id=None):
        
        filters = [
            models.Router.deleted_at == None
        ]
        total_business_owners = 0
        if id:
            filters.append(models.Router.owner_user_id == id)
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

        return {
            "total_business_owners": total_business_owners,
            "total_routers": total_routers,
            "total_subscribers": total_subscribers
        }