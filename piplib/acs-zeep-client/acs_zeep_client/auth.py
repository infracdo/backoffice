"""
Authentication handler for Keycloak OAuth2
"""

import httpx
from datetime import datetime, timedelta
from typing import Optional
from .models import TokenResponse
from .exceptions import AuthenticationError


class AuthManager:
    """Handles authentication with Keycloak"""
    
    def __init__(
        self,
        keycloak_url: str,
        realm: str,
        client_id: str,
        client_secret: str
    ):
        self.keycloak_url = keycloak_url.rstrip('/')
        self.realm = realm
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_data: Optional[TokenResponse] = None
        self.token_expires_at: Optional[datetime] = None
    
    @property
    def token_url(self) -> str:
        """Get the token endpoint URL"""
        return f"{self.keycloak_url}/auth/realms/{self.realm}/protocol/openid-connect/token"
    
    async def get_access_token(self) -> str:
        """Get a valid access token, refreshing if necessary"""
        if self.is_token_valid():
            return self.token_data.access_token
        
        await self.authenticate()
        return self.token_data.access_token
    
    def is_token_valid(self) -> bool:
        """Check if the current token is still valid"""
        if not self.token_data or not self.token_expires_at:
            return False
        
        # Add 30 second buffer
        return datetime.now() + timedelta(seconds=30) < self.token_expires_at
    
    async def authenticate(self) -> TokenResponse:
        """Authenticate with Keycloak using client credentials"""
        async with httpx.AsyncClient() as client:
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
            
            try:
                response = await client.post(
                    self.token_url,
                    data=data,
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                response.raise_for_status()
                
                token_data = response.json()
                self.token_data = TokenResponse(**token_data)
                self.token_expires_at = datetime.now() + timedelta(
                    seconds=self.token_data.expires_in
                )
                
                return self.token_data
                
            except httpx.HTTPStatusError as e:
                raise AuthenticationError(
                    f"Authentication failed: {e.response.status_code} {e.response.text}"
                )
            except httpx.RequestError as e:
                raise AuthenticationError(f"Authentication request failed: {str(e)}")
    
    def get_auth_headers(self) -> dict:
        """Get authorization headers for API requests"""
        if not self.token_data:
            raise AuthenticationError("No valid token available")
        
        return {
            "Authorization": f"Bearer {self.token_data.access_token}",
            "Content-Type": "application/json"
        }
