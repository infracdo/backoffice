"""
Monitoring API endpoints
"""

from typing import List, Optional, Dict, Any
from .base import BaseAPI


class MonitoringAPI(BaseAPI):
    """API endpoints for monitoring operations"""
    
    async def get_system_status(self, debug: bool = False) -> Dict[str, Any]:
        """Get overall system status"""
        # Try WiFiDog monitoring endpoints
        try:
            result = {}
            result["connected_users"] = await self.get("/api/wifidog/count-current-connected-users", debug=debug)
            result["connected_aps"] = await self.get("/api/wifidog/count-current-connected-aps", debug=debug)
            result["total_connections_today"] = await self.get("/api/wifidog/total-user-connections-today", debug=debug)
            return result
        except:
            return {"status": "unknown"}
    
    async def get_health_check(self, debug: bool = False) -> Dict[str, Any]:
        """Get health check status"""
        # Use a simple endpoint that should always work
        try:
            return await self.get("/api/wifidog/count-current-connected-users", debug=debug)
        except:
            return {"status": "down"}
    
    async def get_service_status(self, service_name: Optional[str] = None, debug: bool = False) -> Dict[str, Any]:
        """Get status of WiFiDog services"""
        if service_name == "bandwidth":
            return await self.get("/api/wifidog/total-bandwidth-consumption-today", debug=debug)
        elif service_name == "connections":
            return await self.get("/api/wifidog/total-user-connections-today", debug=debug)
        else:
            return await self.get("/api/wifidog/current-connected-aps", debug=debug)
    
    async def get_database_status(self, debug: bool = False) -> Dict[str, Any]:
        """Get database connection status (using connected APs as proxy)"""
        return await self.get("/api/wifidog/current-connected-aps", debug=debug)
    
    async def get_performance_metrics(
        self,
        metric_type: Optional[str] = None,
        time_range: Optional[str] = None,
        debug: bool = False
    ) -> Dict[str, Any]:
        """Get performance metrics"""
        if metric_type == "bandwidth":
            return await self.get("/api/wifidog/average-bandwidth-per-connection", debug=debug)
        elif metric_type == "time":
            return await self.get("/api/wifidog/avg-connection-time", debug=debug)
        else:
            # Return comprehensive metrics
            result = {}
            result["avg_connection_time"] = await self.get("/api/wifidog/avg-connection-time", debug=debug)
            result["avg_bandwidth"] = await self.get("/api/wifidog/average-bandwidth-per-connection", debug=debug)
            result["total_bandwidth_today"] = await self.get("/api/wifidog/total-bandwidth-consumption-today", debug=debug)
            return result
    
    async def get_error_logs(
        self,
        page: int = 1,
        page_size: int = 50,
        level: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        debug: bool = False
    ) -> List[Dict[str, Any]]:
        """Get error logs (using connected users per AP as proxy)"""
        response = await self.get("/api/wifidog/count-current-connected-users-per-ap", debug=debug)
        return response if isinstance(response, list) else []
    
    async def get_audit_logs(
        self,
        page: int = 1,
        page_size: int = 50,
        user_id: Optional[str] = None,
        action: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        debug: bool = False
    ) -> List[Dict[str, Any]]:
        """Get audit logs (using current connected users per AP as proxy)"""
        response = await self.get("/api/wifidog/current-connected-users-per-ap", debug=debug)
        return response if isinstance(response, list) else []
    
    async def get_system_info(self, debug: bool = False) -> Dict[str, Any]:
        """Get system information (connected APs info)"""
        return await self.get("/api/wifidog/current-connected-aps", debug=debug)
    
    async def get_uptime(self, debug: bool = False) -> Dict[str, Any]:
        """Get system uptime (total connections today as proxy)"""
        return await self.get("/api/wifidog/total-user-connections-today", debug=debug)
    
    async def run_diagnostics(self, debug: bool = False) -> Dict[str, Any]:
        """Run system diagnostics (comprehensive metrics)"""
        result = {}
        result["connected_users"] = await self.get("/api/wifidog/count-current-connected-users", debug=debug)
        result["connected_aps"] = await self.get("/api/wifidog/count-current-connected-aps", debug=debug)
        result["bandwidth_today"] = await self.get("/api/wifidog/total-bandwidth-consumption-today", debug=debug)
        result["avg_connection_time"] = await self.get("/api/wifidog/avg-connection-time", debug=debug)
        return result
    
    async def get_network_status(self, debug: bool = False) -> Dict[str, Any]:
        """Get network connectivity status (connected APs)"""
        return await self.get("/api/wifidog/current-connected-aps", debug=debug)
    
    async def test_external_services(self, debug: bool = False) -> Dict[str, Any]:
        """Test connectivity to external services (users per AP)"""
        return await self.get("/api/wifidog/count-current-connected-users-per-ap", debug=debug)
