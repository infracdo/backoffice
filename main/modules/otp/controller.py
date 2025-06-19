from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from main import models
from main.library.common import common
from main.schemas.common import OTPResponse, PostResponse, GetResponse
from main.core.config import Settings
# from twilio.rest import Client
import requests
from urllib.parse import urlencode


settings = Settings()
# account_sid = settings.TWILIO_ACCOUNT_SID
# auth_token = settings.TWILIO_AUTH_TOKEN
# twilio_number = settings.TWILIO_PHONE_NUMBER
# client = Client(account_sid, auth_token)

class OtpController:

    def send_otp(
        self,
        db: Session,
        payload: dict
    ):

        clean_num = common.normalize_ph_number(payload["mobile_no"])
        if not clean_num:
            return PostResponse(
                status="error",
                status_code=400,
                message="Invalid Philippine number format.",
            ).__dict__

        otp = common.generate_mobile_otp() 
        message_body = f"Your Zeep OTP code is: {otp}"

        try:

            # result = self.send_twilio_sms(payload["mobile_no"], message_body)
            # result = self.send_semaphore_sms(payload["mobile_no"], message_body)
            ref_id  = common.generate_otp() # sample ref
            time_now = common.get_timestamp(1)
            new_otp = models.MobileOtp(
                otp=otp,
                mobile_no=payload["mobile_no"],
                device_id=payload["device_id"],
                otp_id=common.uuid_generator(),
                ref_id = ref_id,
                created_at=time_now
            )
            db.add(new_otp)
            db.commit()
            db.refresh(new_otp)

            return OTPResponse(
                status="ok",
                status_code=200,
                otp=otp            
            ).__dict__

        except Exception as e:
            return PostResponse(
                status="error",
                status_code=500,
                message="Sending OTP failed.",
                detail=str(e)
            ).__dict__

        
    
    def sent_otp_list(
        self,
        db: Session,
        payload: dict
    ):
        limit = payload.get("limit",9999999)
        page = payload.get("page",1)

        filters = []
        if payload.get("id"):
            filters.append(models.MobileOtp.otp_id == payload.get("id"))

        # get total rows count
        data = db.query(models.MobileOtp).filter(*filters)
        total_rows = data.count()

        limit = int(limit) if limit else 0
        page = int(page) if page else 0
        offset = (page - 1) * limit if limit and page else None

        otps = (
            db.query(
                models.MobileOtp
            )
            .filter(*filters)
            .limit(limit)
            .offset(offset)
            .all()
        )

        return GetResponse(
            status="ok",
            status_code=200,
            data=jsonable_encoder(otps),
            total_rows=total_rows
        )


    # def send_semaphore_sms(self, to: str, message: str):
    #     url = "https://api.semaphore.co/api/v4/messages"
    #     data = {
    #         "apikey": settings.SEMAPHORE_API_KEY,
    #         "number": to,
    #         "message": message,
    #         "sendername": "frencys"
    #     }
    #     response = requests.post(url, data=data)
    #     print("S E M A  -   R E S", response)
    #     if response.status_code != 200:
    #         raise Exception(f"Semaphore Error: {response.text}")
    #     return response.json()


    # def send_twilio_sms(self, to: str, message: str):
    #     message = client.messages.create(
    #             body=message,
    #             from_=twilio_number,
    #             to=to
    #         )
    #     print("T W I L I O  -   R E S", message)
    #     return message