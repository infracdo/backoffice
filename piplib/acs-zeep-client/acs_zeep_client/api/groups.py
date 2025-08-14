"""
Groups API endpoints
"""

from typing import List, Optional, Dict, Any
from .base import BaseAPI
from ..models import Group, GroupCommand


class GroupsAPI(BaseAPI):
    """API endpoints for group management"""
    
    async def get_all(
        self,
        page: int = 1,
        page_size: int = 50
    ) -> List[Group]:
        """Get all groups"""
        response = await self.get("/getgroup")
        
        if isinstance(response, list):
            return [Group(**group_data) for group_data in response]
        elif isinstance(response, dict):
            return [Group(**response)]
        else:
            return []
    
    async def get_by_id(self, group_id: int) -> Group:
        """Get a specific group by ID"""
        # Get all groups and filter by ID
        groups = await self.get_all()
        for group in groups:
            if group.id == group_id:
                return group
        raise Exception(f"Group {group_id} not found")
    
    async def create(self, group_data: Dict[str, Any]) -> Group:
        """Create a new group"""
        response = await self.post("/addgroup", data=group_data)
        return Group(**response) if isinstance(response, dict) else Group()
    
    async def update(self, group_id: int, group_data: Dict[str, Any]) -> Group:
        """Update an existing group"""
        response = await self.put(f"/api/groups/{group_id}", data=group_data)
        return Group(**response)
    
    async def delete(self, group_id: int) -> bool:
        """Delete a group"""
        await self.delete(f"/api/groups/{group_id}")
        return True
    
    async def get_devices(self, group_id: int) -> List[Dict[str, Any]]:
        """Get devices in a group"""
        return await self.get(f"/api/groups/{group_id}/devices")
    
    async def add_device(self, group_id: int, device_id: str) -> bool:
        """Add a device to a group"""
        data = {"device_id": device_id}
        await self.post(f"/api/groups/{group_id}/devices", data=data)
        return True
    
    async def remove_device(self, group_id: int, device_id: str) -> bool:
        """Remove a device from a group"""
        await self.delete(f"/api/groups/{group_id}/devices/{device_id}")
        return True
    
    async def get_commands(self, group_id: int) -> List[GroupCommand]:
        """Get commands for a group"""
        response = await self.get(f"/api/groups/{group_id}/commands")
        
        if isinstance(response, list):
            return [GroupCommand(**cmd_data) for cmd_data in response]
        else:
            return []
    
    async def send_command(
        self,
        group_id: int,
        command: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> GroupCommand:
        """Send a command to all devices in a group"""
        data = {"command": command}
        if parameters:
            data["parameters"] = parameters
        
        response = await self.post(f"/api/groups/{group_id}/commands", data=data)
        return GroupCommand(**response)
    
    async def get_command_status(self, group_id: int, command_id: int) -> GroupCommand:
        """Get status of a group command"""
        response = await self.get(f"/api/groups/{group_id}/commands/{command_id}")
        return GroupCommand(**response)
