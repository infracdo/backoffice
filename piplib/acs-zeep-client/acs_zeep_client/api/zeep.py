"""
ZEEP API endpoints - Real ZEEP subscriber management endpoints
"""

from typing import List, Optional, Dict, Any
from .base import BaseAPI


class ZeepAPI(BaseAPI):
    """API endpoints for ZEEP subscriber operations"""
    
    async def verify_account(self, username: str, debug: bool = False) -> Dict[str, Any]:
        """Verify/get subscriber account details"""
        return await self.get("/api/zeep/verifyAccount", params={"username": username}, debug=debug)
    
    async def retrieve_account_list(self, debug: bool = False) -> List[Dict[str, Any]]:
        """Retrieve all subscriber accounts"""
        return await self.get("/api/zeep/retrieveAccountList", debug=debug)
    
    async def register_account(self, subscriber_data: Dict[str, Any], debug: bool = False) -> str:
        """Register a new subscriber account"""
        return await self.post("/api/zeep/registerAccount", data=subscriber_data, debug=debug)
    
    async def topup_bytes(self, username: str, value: int, debug: bool = False) -> str:
        """Add bytes to subscriber account"""
        data = {"username": username, "value": str(value)}
        return await self.post("/api/zeep/topupBytes", data=data, debug=debug)
    
    async def topup_time(self, username: str, value: int, debug: bool = False) -> str:
        """Add time to subscriber account"""
        data = {"username": username, "value": str(value)}
        return await self.post("/api/zeep/topupTime", data=data, debug=debug)
    
    async def activate_account(self, username: str, debug: bool = False) -> str:
        """Activate subscriber account"""
        data = {"username": username}
        return await self.post("/api/zeep/activateAccount", data=data, debug=debug)
    
    async def deactivate_account(self, username: str, debug: bool = False) -> str:
        """Deactivate subscriber account"""
        data = {"username": username}
        return await self.post("/api/zeep/deactivateAccount", data=data, debug=debug)
    
    async def terminate_account(self, username: str, debug: bool = False) -> str:
        """Terminate/delete subscriber account"""
        data = {"username": username}
        return await self.post("/api/zeep/terminateAccount", data=data, debug=debug)
    
    async def change_password(self, username: str, old_password: str, new_password: str, debug: bool = False) -> str:
        """Change subscriber account password"""
        data = {
            "username": username,
            "oldPassword": old_password,
            "newPassword": new_password
        }
        return await self.post("/api/zeep/changePassword", data=data, debug=debug)
