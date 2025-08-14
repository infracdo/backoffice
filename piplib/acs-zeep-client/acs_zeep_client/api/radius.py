"""
Radius API endpoints
"""

from typing import List, Optional, Dict, Any
from .base import BaseAPI
from ..models import RadiusSubscriber, RadiusAccounting


class RadiusAPI(BaseAPI):
    """API endpoints for RADIUS operations"""
    
    async def get_subscribers(
        self,
        page: int = 1,
        page_size: int = 50,
        search: Optional[str] = None
    ) -> List[RadiusSubscriber]:
        """Get all RADIUS subscribers"""
        params = {"page": page, "size": page_size}
        if search:
            params["search"] = search
        
        response = await self.get("/api/radius/subscribers", params=params)
        
        if isinstance(response, dict) and "content" in response:
            return [RadiusSubscriber(**sub_data) for sub_data in response["content"]]
        elif isinstance(response, list):
            return [RadiusSubscriber(**sub_data) for sub_data in response]
        else:
            return []
    
    async def get_subscriber(self, subscriber_id: int) -> RadiusSubscriber:
        """Get a specific RADIUS subscriber"""
        response = await self.get(f"/api/radius/subscribers/{subscriber_id}")
        return RadiusSubscriber(**response)
    
    async def create_subscriber(self, subscriber_data: Dict[str, Any]) -> RadiusSubscriber:
        """Create a new RADIUS subscriber"""
        response = await self.post("/api/radius/subscribers", data=subscriber_data)
        return RadiusSubscriber(**response)
    
    async def update_subscriber(
        self,
        subscriber_id: int,
        subscriber_data: Dict[str, Any]
    ) -> RadiusSubscriber:
        """Update a RADIUS subscriber"""
        response = await self.put(f"/api/radius/subscribers/{subscriber_id}", data=subscriber_data)
        return RadiusSubscriber(**response)
    
    async def delete_subscriber(self, subscriber_id: int) -> bool:
        """Delete a RADIUS subscriber"""
        await self.delete(f"/api/radius/subscribers/{subscriber_id}")
        return True
    
    async def get_accounting_records(
        self,
        page: int = 1,
        page_size: int = 50,
        username: Optional[str] = None,
        nas_ip: Optional[str] = None
    ) -> List[RadiusAccounting]:
        """Get RADIUS accounting records"""
        params = {"page": page, "size": page_size}
        if username:
            params["username"] = username
        if nas_ip:
            params["nas_ip"] = nas_ip
        
        response = await self.get("/api/radius/accounting", params=params)
        
        if isinstance(response, dict) and "content" in response:
            return [RadiusAccounting(**acc_data) for acc_data in response["content"]]
        elif isinstance(response, list):
            return [RadiusAccounting(**acc_data) for acc_data in response]
        else:
            return []
    
    async def get_accounting_record(self, record_id: int) -> RadiusAccounting:
        """Get a specific accounting record"""
        response = await self.get(f"/api/radius/accounting/{record_id}")
        return RadiusAccounting(**response)
    
    async def get_allowed_nas_addresses(self) -> List[Dict[str, Any]]:
        """Get allowed NAS MAC addresses"""
        return await self.get("/api/radius/nas-addresses")
    
    async def add_allowed_nas_address(self, mac_address: str) -> Dict[str, Any]:
        """Add an allowed NAS MAC address"""
        data = {"mac_address": mac_address}
        return await self.post("/api/radius/nas-addresses", data=data)
    
    async def remove_allowed_nas_address(self, address_id: int) -> bool:
        """Remove an allowed NAS MAC address"""
        await self.delete(f"/api/radius/nas-addresses/{address_id}")
        return True
    
    async def test_authentication(self, username: str, password: str) -> Dict[str, Any]:
        """Test RADIUS authentication"""
        data = {"username": username, "password": password}
        return await self.post("/api/radius/test-auth", data=data)
