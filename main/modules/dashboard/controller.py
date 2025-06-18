import jwt
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from main import models
from main.schemas.dashboard import GetTotalsResponse
from main.core.config import Settings

settings = Settings()

class DashboardController:

    def get_totals(
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
        total_data_usage = sum((r.data_usage or 0) for r in data)
        total_subscribers = sum((r.subscribers_count or 0) for r in data)

        
        owners = db.query(models.User).filter(*[
            models.User.deleted_at == None,
            models.User.user_type == "business_owner"
        ])
        total_business_owners = owners.count()

        return GetTotalsResponse(
            status="ok",
            status_code=200,
            total_business_owners=total_business_owners,
            total_routers=total_routers,
            total_subscribers=total_subscribers,
            total_data_usage=total_data_usage,
        ).__dict__
