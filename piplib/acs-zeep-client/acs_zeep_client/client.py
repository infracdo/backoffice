"""
Main ACS ZEEP Client
"""

import os
import httpx
from typing import Optional
from dotenv import load_dotenv
from .auth import AuthManager
from .exceptions import ConnectionError, AuthenticationError
from .api import DevicesAPI, GroupsAPI, RadiusAPI, ZeepAPI, MonitoringAPI, TasksAPI, LogsAPI

# Load environment variables from .env file
load_dotenv(override=True)


class ACSZeepClient:
    """Main client for ACS ZEEP Backend API"""
    
    def __init__(
        self,
        base_url: Optional[str] = None,
        keycloak_url: Optional[str] = None,
        realm: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        timeout: float = 30.0,
        verify_ssl: bool = True
    ):
        """
        Initialize ACS ZEEP Client
        
        Args:
            base_url: Base URL of the ACS ZEEP API
            keycloak_url: Keycloak server URL
            realm: Keycloak realm
            client_id: OAuth2 client ID
            client_secret: OAuth2 client secret
            timeout: Request timeout in seconds
            verify_ssl: Whether to verify SSL certificates
        """
        # Load from environment variables if not provided
        self.base_url = (base_url or os.getenv("ACS_ZEEP_BASE_URL", "http://localhost:7547")).rstrip('/')
        keycloak_url = keycloak_url or os.getenv("KEYCLOAK_URL")
        realm = realm or os.getenv("KEYCLOAK_REALM")
        client_id = client_id or os.getenv("KEYCLOAK_CLIENT_ID")
        client_secret = client_secret or os.getenv("KEYCLOAK_CLIENT_SECRET")
        
        if not all([keycloak_url, realm, client_id, client_secret]):
            raise ValueError(
                "Missing required authentication parameters. Please provide keycloak_url, "
                "realm, client_id, and client_secret either as parameters or environment variables."
            )
        
        # Initialize auth manager
        self.auth_manager = AuthManager(keycloak_url, realm, client_id, client_secret)
        
        # Initialize HTTP client
        self.http_client = httpx.AsyncClient(
            timeout=timeout,
            verify=verify_ssl,
            headers={"User-Agent": "ACS-ZEEP-Client/1.0.0"}
        )
        
        # Initialize API endpoints
        self.devices = DevicesAPI(self.http_client, self.base_url)
        self.groups = GroupsAPI(self.http_client, self.base_url)
        self.radius = RadiusAPI(self.http_client, self.base_url)
        self.zeep = ZeepAPI(self.http_client, self.base_url)
        self.monitoring = MonitoringAPI(self.http_client, self.base_url)
        self.tasks = TasksAPI(self.http_client, self.base_url)
        self.logs = LogsAPI(self.http_client, self.base_url)
        
        self._authenticated = False
    
    async def authenticate(self) -> None:
        """Authenticate with Keycloak and set up authorization headers"""
        try:
            await self.auth_manager.authenticate()
            
            # Update HTTP client headers with auth token
            auth_headers = self.auth_manager.get_auth_headers()
            self.http_client.headers.update(auth_headers)
            
            self._authenticated = True
            
        except Exception as e:
            raise AuthenticationError(f"Authentication failed: {str(e)}")
    
    async def ensure_authenticated(self) -> None:
        """Ensure the client is authenticated, refreshing token if needed"""
        if not self._authenticated or not self.auth_manager.is_token_valid():
            await self.authenticate()
    
    async def test_connection(self) -> dict:
        """Test connection to the API"""
        try:
            await self.ensure_authenticated()
            
            # Try to get system status as a connection test
            response = await self.monitoring.get_health_check()
            return {
                "success": True,
                "message": "Connection successful",
                "data": response
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}",
                "error": str(e)
            }
    
    async def close(self) -> None:
        """Close the HTTP client"""
        await self.http_client.aclose()
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.authenticate()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    # Utility methods
    async def get_server_info(self) -> dict:
        """Get server information"""
        await self.ensure_authenticated()
        return await self.monitoring.get_system_info()
    
    async def get_api_version(self) -> dict:
        """Get API version information"""
        try:
            # Try to get from a public endpoint first
            response = await self.http_client.get(f"{self.base_url}/api/version")
            return response.json()
        except:
            # Fallback to authenticated endpoint
            await self.ensure_authenticated()
            return await self.monitoring.get_system_info()
    
    def __repr__(self) -> str:
        return f"ACSZeepClient(base_url='{self.base_url}', authenticated={self._authenticated})"
