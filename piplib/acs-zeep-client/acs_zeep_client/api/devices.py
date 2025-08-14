"""
Devices API endpoints
"""

from typing import List, Optional, Dict, Any
from .base import BaseAPI
from ..models import Device, APIResponse


class DevicesAPI(BaseAPI):
    """API endpoints for device management"""
    
    async def get_all(
        self,
        page: int = 1,
        page_size: int = 50,
        search: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Device]:
        """Get all devices with optional filtering"""
        # Use the actual endpoint from your Spring Boot app
        response = await self.get("/getdevice")
        
        # Parse response and convert to Device objects
        if isinstance(response, list):
            return [Device(**device_data) for device_data in response]
        elif isinstance(response, dict) and "content" in response:
            return [Device(**device_data) for device_data in response["content"]]
        elif isinstance(response, dict):
            # If single device returned, wrap in list
            return [Device(**response)]
        else:
            return []
    
    async def get_by_id(self, device_id: str) -> Device:
        """Get a specific device by ID"""
        # Note: The Spring Boot app doesn't seem to have a get by ID endpoint
        # We'll get all devices and filter
        devices = await self.get_all()
        for device in devices:
            if device.id == device_id or device.serial_number == device_id:
                return device
        raise Exception(f"Device {device_id} not found")
    
    async def create(self, device_data: Dict[str, Any]) -> Device:
        """Create a new device"""
        response = await self.post("/adddevice", data=device_data)
        return Device(**response) if isinstance(response, dict) else Device()
    
    async def update(self, device_id: str, device_data: Dict[str, Any]) -> Device:
        """Update an existing device"""
        response = await self.put(f"/updatedevice/{device_id}", data=device_data)
        return Device(**response)
    
    async def delete(self, device_id: str) -> bool:
        """Delete a device"""
        await self.delete(f"/api/devices/{device_id}")
        return True
    
    async def get_device_info(self, device_id: str) -> Dict[str, Any]:
        """Get detailed device information"""
        return await self.get(f"/api/devices/{device_id}/info")
    
    async def send_command(
        self,
        device_id: str,
        command: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send a command to a device"""
        data = {"command": command}
        if parameters:
            data["parameters"] = parameters
        
        return await self.post(f"/api/devices/{device_id}/command", data=data)
    
    async def get_parameters(self, device_id: str) -> Dict[str, Any]:
        """Get device parameters"""
        return await self.get(f"/api/devices/{device_id}/parameters")
    
    async def set_parameters(
        self,
        device_id: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Set device parameters"""
        return await self.post(f"/api/devices/{device_id}/parameters", data=parameters)
    
    async def reboot(self, device_id: str) -> Dict[str, Any]:
        """Reboot a device"""
        return await self.get(f"/Reboot/{device_id}")
    
    async def factory_reset(self, device_id: str) -> Dict[str, Any]:
        """Factory reset a device"""
        return await self.get(f"/FactoryReset/{device_id}")
    
    async def send_command(
        self,
        device_id: str,
        command: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send a command to a device"""
        return await self.get(f"/Command/{device_id}")
    
    async def get_parameters(self, device_id: str, object_name: str = "Device.") -> Dict[str, Any]:
        """Get device parameters"""
        return await self.get(f"/GetParameterValues/{device_id}, {object_name}")
    
    async def set_parameters(
        self,
        device_id: str,
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Set device parameters"""
        return await self.post(f"/SetParameterValues/{device_id}", data=parameters)
