"""
Radius API endpoints - Real RADIUS statistics and monitoring endpoints
"""

from typing import List, Optional, Dict, Any
from .base import BaseAPI


class RadiusAPI(BaseAPI):
    """API endpoints for RADIUS operations - Statistics and monitoring"""
    
    async def count_currently_connected_users(self, debug: bool = False) -> Dict[str, Any]:
        """Get number of current active users"""
        return await self.get("/api/radius/count-currently-connected-users", debug=debug)
    
    async def count_total_users(self, debug: bool = False) -> Dict[str, Any]:
        """Get number of total users"""
        return await self.get("/api/radius/count-total-users", debug=debug)
    
    async def count_total_aps(self, debug: bool = False) -> Dict[str, Any]:
        """Get number of total access points"""
        return await self.get("/api/radius/count-total-aps", debug=debug)
    
    async def count_currently_connected_aps(self, debug: bool = False) -> Dict[str, Any]:
        """Get number of current active access points"""
        return await self.get("/api/radius/count-currently-connected-aps", debug=debug)
    
    async def total_user_connections_today(self, debug: bool = False) -> Dict[str, Any]:
        """Get total number of user connections for today"""
        return await self.get("/api/radius/total-user-connections-today", debug=debug)
    
    async def total_user_sessions_today(self, debug: bool = False) -> Dict[str, Any]:
        """Get total number of user sessions for today"""
        return await self.get("/api/radius/total-user-sessions-today", debug=debug)
    
    async def total_bandwidth_consumption_today(self, debug: bool = False) -> Dict[str, Any]:
        """Get total bandwidth consumption for today"""
        return await self.get("/api/radius/total-bandwidth-consumption-today", debug=debug)
    
    async def total_session_time_today(self, debug: bool = False) -> Dict[str, Any]:
        """Get total session time for today"""
        return await self.get("/api/radius/total-session-time-today", debug=debug)
    
    async def average_connection_time(self, debug: bool = False) -> Dict[str, str]:
        """Get average connection time"""
        return await self.get("/api/radius/average-connection-time", debug=debug)
    
    async def average_bandwidth_per_connection(self, debug: bool = False) -> Dict[str, Any]:
        """Get average bandwidth per connection"""
        return await self.get("/api/radius/average-bandwidth-per-connection", debug=debug)
    
    async def get_access_points(self, debug: bool = False) -> Dict[str, Any]:
        """Get list of access points"""
        return await self.get("/api/radius/access-points", debug=debug)
    
    async def get_access_points_online(self, debug: bool = False) -> List[Dict[str, Any]]:
        """Get list of online access points info"""
        return await self.get("/api/radius/access-points-online", debug=debug)
    
    async def get_access_points_all(self, debug: bool = False) -> List[Dict[str, Any]]:
        """Get list of all access points info"""
        return await self.get("/api/radius/access-points-all", debug=debug)
    
    async def count_currently_connected_users_per_ap(self, debug: bool = False) -> List[Dict[str, Any]]:
        """Get number of currently connected users per access point"""
        return await self.get("/api/radius/count-currently-connected-users-per-ap", debug=debug)
    
    async def currently_connected_users_per_ap(self, debug: bool = False) -> List[Dict[str, Any]]:
        """Get list of currently connected users per access point"""
        return await self.get("/api/radius/currently-connected-users-per-ap", debug=debug)
