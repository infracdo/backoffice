"""
ZEEP API endpoints
"""

from typing import List, Optional, Dict, Any
from .base import BaseAPI
from ..models import ZeepMonitoringData


class ZeepAPI(BaseAPI):
    """API endpoints for ZEEP operations"""
    
    async def get_status(self) -> Dict[str, Any]:
        """Get ZEEP service status"""
        return await self.get("/api/zeep/status")
    
    async def get_monitoring_data(
        self,
        service_name: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[ZeepMonitoringData]:
        """Get ZEEP monitoring data"""
        params = {}
        if service_name:
            params["service"] = service_name
        if start_time:
            params["start"] = start_time
        if end_time:
            params["end"] = end_time
        
        response = await self.get("/api/zeep/monitoring", params=params)
        
        if isinstance(response, list):
            return [ZeepMonitoringData(**data) for data in response]
        else:
            return []
    
    async def get_services(self) -> List[Dict[str, Any]]:
        """Get all ZEEP services"""
        return await self.get("/api/zeep/services")
    
    async def get_service_details(self, service_name: str) -> Dict[str, Any]:
        """Get details for a specific ZEEP service"""
        return await self.get(f"/api/zeep/services/{service_name}")
    
    async def restart_service(self, service_name: str) -> Dict[str, Any]:
        """Restart a ZEEP service"""
        return await self.post(f"/api/zeep/services/{service_name}/restart")
    
    async def stop_service(self, service_name: str) -> Dict[str, Any]:
        """Stop a ZEEP service"""
        return await self.post(f"/api/zeep/services/{service_name}/stop")
    
    async def start_service(self, service_name: str) -> Dict[str, Any]:
        """Start a ZEEP service"""
        return await self.post(f"/api/zeep/services/{service_name}/start")
    
    async def get_configuration(self) -> Dict[str, Any]:
        """Get ZEEP configuration"""
        return await self.get("/api/zeep/config")
    
    async def update_configuration(self, config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update ZEEP configuration"""
        return await self.put("/api/zeep/config", data=config_data)
    
    async def get_metrics(
        self,
        metric_type: Optional[str] = None,
        time_range: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get ZEEP metrics"""
        params = {}
        if metric_type:
            params["type"] = metric_type
        if time_range:
            params["range"] = time_range
        
        return await self.get("/api/zeep/metrics", params=params)
    
    async def get_alerts(
        self,
        severity: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get ZEEP alerts"""
        params = {}
        if severity:
            params["severity"] = severity
        if status:
            params["status"] = status
        
        response = await self.get("/api/zeep/alerts", params=params)
        return response if isinstance(response, list) else []
    
    async def acknowledge_alert(self, alert_id: str) -> Dict[str, Any]:
        """Acknowledge a ZEEP alert"""
        return await self.post(f"/api/zeep/alerts/{alert_id}/acknowledge")
