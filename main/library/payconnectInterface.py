import os
import requests
import json
from main.core.config import settings

class PayconnectInterface():

    def __init__(self):
        self.payconnect_url = settings.PAYCONNECT_BASEURL
        self.payconnect_auth = settings.PAYCONNECT_AUTH

    async def get_qr_string(self, ref_no: str, amount: float):
        headers = {
            "Content-Type" : "application/json",
            "Authorization" : self.payconnect_auth
        }
        url = f"{self.payconnect_url}/payments/generateqr"
        data = {
            "processorCode": "QRPH-RBG",
            "initMethod": "static",
            "currency": "PHP",
            "amount": str(amount),
            "merchantReferenceNumber": f"{ref_no}"
        }
        print(f"------ get_qr_string {data}")
        r = requests.post(url=url, json=data, headers=headers)
        print(r.text)
        ret_json = r.json()

        print(ret_json)
        return ret_json
    

payconnect_interface = PayconnectInterface()


      
    #   webhook
    #   print(webhookData)
    #     qrdata = await rdb.get(f"paymentgateway:{webhookData.chargeReference}")
    #     if qrdata is None:
    #         # data is not available in redis
    #         # return error here
    #         return {
    #             "errorCode":"0000",
    #             "errorDescription":"success"
    #         }
    #     # get the data from redis
    #     qrdata_dict = json.loads(qrdata)
    #     params_data = RequestQR.parse_obj(qrdata_dict)
    #     # base on that data get the payment
    #     print("params_data >>>", params_data)
    #     from datetime import date
    #     today_str = date.today().strftime('%Y-%m-%d')
    #     amount = str(webhookData.amount)
    #     if settings.TESTAMOUNT != 0:
    #         amount= str(params_data.amount)

    #     payload = PayInvoice(
    #         amount=amount,
    #         invoice_id=params_data.invoice_id,
    #         note=f"Online Payment Ref {webhookData.retrievalReference}",
    #         payment_date=today_str,
    #     )
    #     background_tasks.add_task(bgtask_xgatePayment, rdb=rdb, sessionid=webhookData.chargeReference, payload=payload)

    #     retval = {
    #         "errorCode":"0000",
    #         "errorDescription":"success"
    #     }
    #     return retval

        # class PayConnectWebhook(BaseModel):
        #     result: str
        #     retrievalReference: str
        #     amount: str
        #     authCode: str
        #     paymentCode: str = ""
        #     signature: str
        #     chargeReference: str
        #     timestamp: str
        #     paymentType: str