"""
Pydantic models for ACS ZEEP API data structures
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Device(BaseModel):
    """Device model"""
    id: Optional[int] = None  # Changed from str to int to match API response
    device_name: Optional[str] = None
    mac_address: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    parent: Optional[str] = None
    date_created: Optional[str] = None  # API returns string dates
    date_modified: Optional[str] = None
    date_offline: Optional[str] = None
    activated: Optional[bool] = None
    # Keep these for backwards compatibility
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    ip_address: Optional[str] = None
    connection_request_url: Optional[str] = None
    last_inform: Optional[datetime] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Group(BaseModel):
    """Group model"""
    id: Optional[int] = None
    name: Optional[str] = None
    group_name: Optional[str] = None
    location: Optional[str] = None
    parent: Optional[str] = None
    child: Optional[str] = None
    date_created: Optional[str] = None
    date_modified: Optional[str] = None
    parent_concat: Optional[str] = None # can you concat parent and group_name
    
    def model_post_init(self, __context) -> None:
        """Concatenate parent and group_name after data is loaded"""
        # Set name to be the same as group_name
        if self.group_name:
            self.name = self.group_name
            
        # Set parent_concat to combine parent and group_name
        if self.parent and self.group_name:
            self.parent_concat = f"{self.parent}/{self.group_name}"
        elif self.group_name:
            self.parent_concat = self.group_name

class GroupCommand(BaseModel):
    """Group Command model"""
    id: Optional[int] = None
    group_id: Optional[int] = None
    command: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    executed_at: Optional[datetime] = None


class TaskHandler(BaseModel):
    """Task Handler model"""
    id: Optional[int] = None
    task_name: Optional[str] = None
    status: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CPEResponseLog(BaseModel):
    """CPE Response Log model"""
    id: Optional[int] = None
    device_id: Optional[str] = None
    request_type: Optional[str] = None
    request_data: Optional[str] = None
    response_data: Optional[str] = None
    timestamp: Optional[datetime] = None
    status_code: Optional[int] = None


class WebCLIResponseLog(BaseModel):
    """WebCLI Response Log model"""
    id: Optional[int] = None
    command: Optional[str] = None
    response: Optional[str] = None
    timestamp: Optional[datetime] = None
    user_id: Optional[str] = None


class HTTPRequestLog(BaseModel):
    """HTTP Request Log model"""
    id: Optional[int] = None
    method: Optional[str] = None
    url: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    body: Optional[str] = None
    response_status: Optional[int] = None
    response_body: Optional[str] = None
    timestamp: Optional[datetime] = None


# Radius Models
class RadiusSubscriber(BaseModel):
    """Radius Subscriber model"""
    id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    nas_ip_address: Optional[str] = None
    nas_port: Optional[int] = None
    framed_ip_address: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None


class RadiusAccounting(BaseModel):
    """Radius Accounting model"""
    id: Optional[int] = None
    username: Optional[str] = None
    nas_ip_address: Optional[str] = None
    session_id: Optional[str] = None
    start_time: Optional[datetime] = None
    stop_time: Optional[datetime] = None
    session_time: Optional[int] = None
    input_octets: Optional[int] = None
    output_octets: Optional[int] = None


# ZEEP Models
class ZeepMonitoringData(BaseModel):
    """ZEEP Monitoring Data model"""
    service_name: Optional[str] = None
    status: Optional[str] = None
    last_check: Optional[datetime] = None
    response_time: Optional[float] = None
    metrics: Optional[Dict[str, Any]] = None


# API Response Models
class APIResponse(BaseModel):
    """Generic API Response model"""
    success: bool = True
    data: Optional[Any] = None
    message: Optional[str] = None
    error: Optional[str] = None


class PaginatedResponse(BaseModel):
    """Paginated API Response model"""
    success: bool = True
    data: List[Any] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    page_size: int = 50
    total_pages: int = 1


# Authentication Models
class TokenResponse(BaseModel):
    """Keycloak Token Response model"""
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
