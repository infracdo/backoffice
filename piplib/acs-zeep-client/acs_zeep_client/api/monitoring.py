"""
Monitoring API endpoints
"""

from typing import List, Optional, Dict, Any
from .base import BaseAPI


class MonitoringAPI(BaseAPI):
    """API endpoints for monitoring operations"""
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        # Try WiFiDog monitoring endpoints
        try:
            result = {}
            result["connected_users"] = await self.get("/api/wifidog/count-current-connected-users")
            result["connected_aps"] = await self.get("/api/wifidog/count-current-connected-aps")
            result["total_connections_today"] = await self.get("/api/wifidog/total-user-connections-today")
            return result
        except:
            return {"status": "unknown"}
    
    async def get_health_check(self) -> Dict[str, Any]:
        """Get health check status"""
        # Use a simple endpoint that should always work
        try:
            return await self.get("/api/wifidog/count-current-connected-users")
        except:
            return {"status": "down"}
    
    async def get_service_status(self, service_name: Optional[str] = None) -> Dict[str, Any]:
        """Get status of specific service or all services"""
        if service_name:
            return await self.get(f"/api/monitoring/services/{service_name}")
        else:
            return await self.get("/api/monitoring/services")
    
    async def get_database_status(self) -> Dict[str, Any]:
        """Get database connection status"""
        return await self.get("/api/monitoring/database")
    
    async def get_performance_metrics(
        self,
        metric_type: Optional[str] = None,
        time_range: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get performance metrics"""
        params = {}
        if metric_type:
            params["type"] = metric_type
        if time_range:
            params["range"] = time_range
        
        return await self.get("/api/monitoring/metrics", params=params)
    
    async def get_error_logs(
        self,
        page: int = 1,
        page_size: int = 50,
        level: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get error logs"""
        params = {"page": page, "size": page_size}
        if level:
            params["level"] = level
        if start_time:
            params["start"] = start_time
        if end_time:
            params["end"] = end_time
        
        response = await self.get("/api/monitoring/logs/errors", params=params)
        return response if isinstance(response, list) else []
    
    async def get_audit_logs(
        self,
        page: int = 1,
        page_size: int = 50,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get audit logs"""
        params = {"page": page, "size": page_size}
        if user_id:
            params["user_id"] = user_id
        if action:
            params["action"] = action
        if start_time:
            params["start"] = start_time
        if end_time:
            params["end"] = end_time
        
        response = await self.get("/api/monitoring/logs/audit", params=params)
        return response if isinstance(response, list) else []
    
    async def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return await self.get("/api/monitoring/system-info")
    
    async def get_uptime(self) -> Dict[str, Any]:
        """Get system uptime"""
        return await self.get("/api/monitoring/uptime")
    
    async def run_diagnostics(self) -> Dict[str, Any]:
        """Run system diagnostics"""
        return await self.post("/api/monitoring/diagnostics")
    
    async def get_network_status(self) -> Dict[str, Any]:
        """Get network connectivity status"""
        return await self.get("/api/monitoring/network")
    
    async def test_external_services(self) -> Dict[str, Any]:
        """Test connectivity to external services"""
        return await self.post("/api/monitoring/test-external")
