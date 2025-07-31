import asyncio
import httpx
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String
from main import models
from main.library.common import common
from main.schemas.common import PostResponse, GetResponse
from main.core.config import settings
from typing import Optional


class PromoController:

    def create_promo(
        self,
        db: Session,
        payload: dict
    ):
        if payload["title"]:
            existing_promo = (
                db.query(models.Promo)
                .filter(
                    models.Promo.deleted_at == None,
                    models.Promo.title == payload["title"]
                ).first()
            )
            if existing_promo:
                return PostResponse(
                    status="error",
                    status_code=400,
                    message="Promo title already exist"
                ).__dict__


        time_now = common.get_timestamp(1)
        new_promo = models.Promo(
            image_url=payload["image_url"],
            link_url=payload["link_url"],
            title=payload["title"],
            type=payload["type"],
            description=payload.get("description"),
            is_show=payload["is_show"],
            promo_id=common.uuid_generator(),
            created_at=time_now,
            updated_at=time_now
        )

        db.add(new_promo)
        db.commit()
        db.refresh(new_promo)


        return PostResponse(
            status="ok",
            status_code=200,
            message="Promo created successfully",
            data={
                "promo": jsonable_encoder(new_promo)
            }
        ).__dict__
        
    
    def update_promo(
        self,
        db: Session,
        payload: dict
    ):

        promo = (
            db.query(models.Promo)
            .filter_by(promo_id=payload["promo_id"])
            .one_or_none()
        )
        if not promo:
            return PostResponse(
                status="error",
                status_code=400,
                message="Promo not found"
            ).__dict__
        

        promo_data = jsonable_encoder(promo)
        if isinstance(payload, dict):
            update_data = payload
        else:
            update_data = payload.dict(exclude_unset=True)
        update_data["updated_at"] = common.get_timestamp(1)
        for field in promo_data:
            if field in update_data:
                setattr(promo, field, update_data[field])

        db.commit()
        db.refresh(promo)

        return PostResponse(
            status="ok",
            status_code=200,
            message="Promo successfully updated",
            data={
                "promo": jsonable_encoder(promo)
            }
        ).__dict__

    
    def promo_list(
        self,
        db: Session,
        payload: dict,
        type: Optional[str] = None,
        is_all: Optional[bool] = False,
        search: Optional[str] = None,
    ):
        limit = payload.get("limit",9999999)
        page = payload.get("page",1)
        filters = [
            models.Promo.deleted_at == None
        ]
        if payload.get("id"):
            filters.append(models.Promo.promo_id == payload.get("id"))
        if is_all == False:
            filters.append(models.Promo.is_show == True)
        if type:
            filters.append(models.Promo.type == type)
        if search: 
            filters.append(
                or_(
                    models.Promo.type.ilike(f"%{search}%"),
                    models.Promo.title.ilike(f"%{search}%"),
                    models.Promo.description.ilike(f"%{search}%"),
                    models.Promo.image_url.ilike(f"%{search}%")
                )
            )
        # get total rows count
        data = db.query(models.Promo).filter(*filters)
        total_rows = data.count()
       
        limit = int(limit) if limit else 0
        page = int(page) if page else 0
        offset = (page - 1) * limit if limit and page else None

        promos = (
            db.query(
                models.Promo
            )
            .filter(*filters)
            .order_by(models.Promo.updated_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )

        ret = GetResponse(
                status="ok",
                status_code=200,
                data=jsonable_encoder(promos),
                total_rows=total_rows
            ).__dict__
        
        
        return ret
            
    
    def download_promo_list(
        self,
        db: Session,
        filename: str,
        file_type: str,
        type: Optional[str] = None,
        is_all: Optional[bool] = False,
        search: Optional[str] = None
    ):
        filters = [
            models.Promo.deleted_at == None
        ]
        if is_all == False:
            filters.append(models.Promo.is_show == True)
        if type:
            filters.append(models.Promo.type == type)
        if search: 
            filters.append(
                or_(
                    models.Promo.type.ilike(f"%{search}%"),
                    models.Promo.title.ilike(f"%{search}%"),
                    models.Promo.description.ilike(f"%{search}%"),
                    models.Promo.image_url.ilike(f"%{search}%")
                )
            )
        promos = (
            db.query(
                models.Promo
            )
            .filter(*filters)
            .order_by(models.Promo.updated_at.desc())
            .all()
        )

        keys = (
            "created_at",
            "updated_at",
            "type",
            "title",
            "description",
            "image_url",
            "link_url",
            "is_show"
        )
        headers = (
            "Date Created",
            "Date Updated",
            "Type",
            "Promo Title",
            "Description",
            "Image URL",
            "link URL",
            "Show"
        )

        print("promos", promos)

        raw_data = {
            "header": keys,
            "headers": headers,
            "rows": jsonable_encoder(promos)
        }
        data = common.format_excel(rawData=raw_data)
        return common.get_media_return(
            file_name=filename,
            file_type=file_type,
            data=data,
        )
    
    def delete_promo(
        self,
        db: Session,
        id: str
    ):

        promo = (
            db.query(models.Promo)
            .filter_by(promo_id=id)
            .one_or_none()
        )
        if not promo:
            return PostResponse(
                status="error",
                status_code=400,
                message="Promo not found"
            ).__dict__
    
        promo.deleted_at= common.get_timestamp(1)
        db.commit()

        return PostResponse(
            status="ok",
            status_code=200,
            message="Promo successfully deleted"
        ).__dict__