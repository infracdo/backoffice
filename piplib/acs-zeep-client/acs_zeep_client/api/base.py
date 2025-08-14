"""
Base API client class
"""

import httpx
from typing import Any, Dict, List, Optional, Union
from ..exceptions import APIError, NotFoundError, UnauthorizedError, ForbiddenError
from ..models import APIResponse


class BaseAPI:
    """Base class for all API endpoint classes"""
    
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        self.client = client
        self.base_url = base_url.rstrip('/')
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
        debug: bool = False
    ) -> Any:
        """Make an HTTP request to the API"""
        url = f"{self.base_url}{endpoint}"
        
        # Debug logging (optional)
        if debug:
            print(f"🌐 {method} {url}")
            if params:
                print(f"📝 Params: {params}")
            if data:
                print(f"📦 Data: {data}")
            if headers:
                print(f"🏷️ Headers: {headers}")
        
        try:
            response = await self.client.request(
                method=method,
                url=url,
                params=params,
                json=data if isinstance(data, dict) else None,
                data=data if isinstance(data, str) else None,
                headers=headers
            )
            
            # Debug response
            if debug:
                print(f"📊 Response Status: {response.status_code}")
                print(f"📋 Response Headers: {dict(response.headers)}")
            
            # Handle different status codes
            if response.status_code == 401:
                if debug:
                    print(f"🚫 Unauthorized response: {response.text}")
                raise UnauthorizedError("Unauthorized", 401, response.text)
            elif response.status_code == 403:
                if debug:
                    print(f"🚫 Forbidden response: {response.text}")
                raise ForbiddenError("Forbidden", 403, response.text)
            elif response.status_code == 404:
                if debug:
                    print(f"❌ Not Found response: {response.text}")
                raise NotFoundError("Not Found", 404, response.text)
            elif response.status_code >= 400:
                if debug:
                    print(f"⚠️ Error response: {response.text}")
                raise APIError(
                    f"API request failed: {response.status_code}",
                    response.status_code,
                    response.text
                )
            
            # Try to parse JSON response
            try:
                response_data = response.json()
                if debug:
                    print(f"✅ JSON Response: {response_data}")
                return response_data
            except ValueError:
                # Return raw text if not JSON
                response_text = response.text
                if debug:
                    print(f"📄 Text Response: {response_text}")
                return response_text
                
        except httpx.RequestError as e:
            if debug:
                print(f"🔌 Connection Error: {str(e)}")
            raise APIError(f"Request failed: {str(e)}")
        except Exception as e:
            if debug:
                print(f"💥 Unexpected Error: {str(e)}")
            raise APIError(f"Unexpected error: {str(e)}")
    
    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        debug: bool = False
    ) -> Any:
        """Make a GET request"""
        return await self._request("GET", endpoint, params=params, headers=headers, debug=debug)
    
    async def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        debug: bool = False
    ) -> Any:
        """Make a POST request"""
        return await self._request("POST", endpoint, params=params, data=data, headers=headers, debug=debug)
    
    async def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        debug: bool = False
    ) -> Any:
        """Make a PUT request"""
        return await self._request("PUT", endpoint, params=params, data=data, headers=headers, debug=debug)
    
    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        debug: bool = False
    ) -> Any:
        """Make a DELETE request"""
        return await self._request("DELETE", endpoint, params=params, headers=headers, debug=debug)
