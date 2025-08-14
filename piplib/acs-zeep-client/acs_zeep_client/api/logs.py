"""
Logs API endpoints
"""

from typing import List, Optional, Dict, Any
from .base import BaseAPI
from ..models import CPEResponseLog, WebCLIResponseLog, HTTPRequestLog


class LogsAPI(BaseAPI):
    """API endpoints for log management"""
    
    async def get_cpe_response_logs(
        self,
        page: int = 1,
        page_size: int = 50,
        device_id: Optional[str] = None,
        request_type: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[CPEResponseLog]:
        """Get CPE response logs"""
        params = {"page": page, "size": page_size}
        if device_id:
            params["device_id"] = device_id
        if request_type:
            params["request_type"] = request_type
        if start_time:
            params["start"] = start_time
        if end_time:
            params["end"] = end_time
        
        response = await self.get("/api/logs/cpe-response", params=params)
        
        if isinstance(response, dict) and "content" in response:
            return [CPEResponseLog(**log_data) for log_data in response["content"]]
        elif isinstance(response, list):
            return [CPEResponseLog(**log_data) for log_data in response]
        else:
            return []
    
    async def get_cpe_response_log(self, log_id: int) -> CPEResponseLog:
        """Get a specific CPE response log"""
        response = await self.get(f"/api/logs/cpe-response/{log_id}")
        return CPEResponseLog(**response)
    
    async def get_webcli_response_logs(
        self,
        page: int = 1,
        page_size: int = 50,
        command: Optional[str] = None,
        user_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[WebCLIResponseLog]:
        """Get WebCLI response logs"""
        params = {"page": page, "size": page_size}
        if command:
            params["command"] = command
        if user_id:
            params["user_id"] = user_id
        if start_time:
            params["start"] = start_time
        if end_time:
            params["end"] = end_time
        
        response = await self.get("/api/logs/webcli-response", params=params)
        
        if isinstance(response, dict) and "content" in response:
            return [WebCLIResponseLog(**log_data) for log_data in response["content"]]
        elif isinstance(response, list):
            return [WebCLIResponseLog(**log_data) for log_data in response]
        else:
            return []
    
    async def get_webcli_response_log(self, log_id: int) -> WebCLIResponseLog:
        """Get a specific WebCLI response log"""
        response = await self.get(f"/api/logs/webcli-response/{log_id}")
        return WebCLIResponseLog(**response)
    
    async def get_http_request_logs(
        self,
        page: int = 1,
        page_size: int = 50,
        method: Optional[str] = None,
        url_pattern: Optional[str] = None,
        status_code: Optional[int] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> List[HTTPRequestLog]:
        """Get HTTP request logs"""
        params = {"page": page, "size": page_size}
        if method:
            params["method"] = method
        if url_pattern:
            params["url"] = url_pattern
        if status_code:
            params["status"] = status_code
        if start_time:
            params["start"] = start_time
        if end_time:
            params["end"] = end_time
        
        response = await self.get("/api/logs/http-request", params=params)
        
        if isinstance(response, dict) and "content" in response:
            return [HTTPRequestLog(**log_data) for log_data in response["content"]]
        elif isinstance(response, list):
            return [HTTPRequestLog(**log_data) for log_data in response]
        else:
            return []
    
    async def get_http_request_log(self, log_id: int) -> HTTPRequestLog:
        """Get a specific HTTP request log"""
        response = await self.get(f"/api/logs/http-request/{log_id}")
        return HTTPRequestLog(**response)
    
    async def search_logs(
        self,
        query: str,
        log_type: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ) -> List[Dict[str, Any]]:
        """Search across all log types"""
        params = {
            "query": query,
            "page": page,
            "size": page_size
        }
        if log_type:
            params["type"] = log_type
        if start_time:
            params["start"] = start_time
        if end_time:
            params["end"] = end_time
        
        response = await self.get("/api/logs/search", params=params)
        return response if isinstance(response, list) else []
    
    async def get_log_statistics(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get log statistics"""
        params = {}
        if start_time:
            params["start"] = start_time
        if end_time:
            params["end"] = end_time
        
        return await self.get("/api/logs/statistics", params=params)
    
    async def export_logs(
        self,
        log_type: str,
        format_type: str = "json",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Export logs in specified format"""
        data = {
            "log_type": log_type,
            "format": format_type
        }
        if start_time:
            data["start"] = start_time
        if end_time:
            data["end"] = end_time
        if filters:
            data["filters"] = filters
        
        return await self.post("/api/logs/export", data=data)
