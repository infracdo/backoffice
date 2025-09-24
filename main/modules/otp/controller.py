from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String
from main import models
from main.library.common import common
from main.library.macrodroidInterface import macrodroid_interface
from main.schemas.common import OTPResponse, PostResponse, GetResponse
from typing import Optional
import asyncio
from acs_zeep_client import ACSZeepClient


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
            result = self.send_sms(
                macrodroid_interface, clean_num, message_body
            )
            print("result ", result)
        except Exception as e:
            print("SEND OTP: FAILED:", e)
            return PostResponse(
                status="error",
                status_code=500,
                message="Sending OTP failed",
                details=str(e)
            ).__dict__
        
     



        ref_id  = common.generate_ref_id() # sample ref
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

        # register subscriber if device_id is less than 32 chars        
        if len(payload["device_id"]) < 32:
            asyncio.create_task(self.register_subscriber(
                username=payload["mobile_no"],
                password=payload["device_id"],
                email=payload["email"],
                fullName=payload["name"]
            ))

        return OTPResponse(
            status="ok",
            status_code=200,
            otp=otp            
        ).__dict__
            

        
    
    def sent_otp_list(
        self,
        db: Session,
        payload: dict,
        search: Optional[str] = None
    ):
        limit = payload.get("limit",9999999)
        page = payload.get("page",1)

        filters = []
        if payload.get("id"):
            filters.append(models.MobileOtp.otp_id == payload.get("id"))
        
        if search: 
            filters.append(
                or_(
                    models.MobileOtp.otp.ilike(f"%{search}%"),
                    models.MobileOtp.mobile_no.ilike(f"%{search}%"),
                    models.MobileOtp.device_id.ilike(f"%{search}%"),
                    models.MobileOtp.ref_id.ilike(f"%{search}%"),
                    cast(models.MobileOtp.created_at, String).ilike(search)
                )
            )

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

    def download_otp_list(
        self,
        db: Session,
        filename: str,
        file_type: str,
        search: Optional[str] = None
    ):
    
        filters = []
 
        if search: 
            filters.append(
                or_(
                    models.MobileOtp.otp.ilike(f"%{search}%"),
                    models.MobileOtp.mobile_no.ilike(f"%{search}%"),
                    models.MobileOtp.device_id.ilike(f"%{search}%"),
                    models.MobileOtp.ref_id.ilike(f"%{search}%"),
                    cast(models.MobileOtp.created_at, String).ilike(search)
                )
            )

        otps = (
            db.query(
                models.MobileOtp
            )
            .filter(*filters)
            .all()
        )
        keys = (
            "created_at",
            "otp",
            "mobile_no",
            "device_id",
            "ref_id"
        )
        headers = (
            "Date",
            "OTP",
            "Mobile No",
            "Device ID",
            "Reference ID"
        )

        raw_data = {
            "header": keys,
            "headers": headers,
            "rows": jsonable_encoder(otps)
        }
        data = common.format_excel(rawData=raw_data)
        return common.get_media_return(
            file_name=filename,
            file_type=file_type,
            data=data,
        )


    def send_sms(self, sms: macrodroid_interface, mobile_no: str, message: str):
        ret = sms.client.send(f"+63{mobile_no}", message)
        return ret



    async def send_to_acs_subscriber_api(self, device_id: str):
        # add tayo dito ng calls papunta sa acs

        if True:
            async with ACSZeepClient() as client:
                 # Test 3: Register a new account
                print("\n➕ 3. Registering new subscriber account:")
                username = device_id
                password = ''.join(chr(ord(c) + 8) for c in f"'{device_id}'")[1:-1]

                try:
                    new_subscriber = {
                        "username": username,
                        "password": password,
                        "email": "sample@example.com",
                        "fullName": f"ZEEP-{device_id}"
                    }
                    result = await client.zeep.register_account(new_subscriber, debug=True)
                    print(f"✅ Success: {result}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                # Test 4: Topup bytes for an account
                print("\n💾 4. Topping up bytes for subscriber:")
                try:
                    result = await client.zeep.topup_bytes(username, 1000000000, debug=True)  # 1GB in bytes
                    print(f"✅ Success: {result}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                # Test 5: Topup time for an account
                print("\n⏰ 5. Topping up time for subscriber:")
                try:
                    result = await client.zeep.topup_time(username, 3600, debug=True)  # 1 hour in seconds
                    print(f"✅ Success: {result}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                # Test 6: Activate account
                print("\n🟢 6. Activating subscriber account:")
                try:
                    result = await client.zeep.activate_account(username, debug=True)
                    print(f"✅ Success: {result}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                