"""
Basic tests for ACS ZEEP Client
"""

import pytest
import os
from unittest.mock import AsyncMock, patch
from acs_zeep_client import ACSZeepClient
from acs_zeep_client.exceptions import AuthenticationError


@pytest.fixture
def mock_env_vars():
    """Mock environment variables for testing"""
    env_vars = {
        "ACS_ZEEP_BASE_URL": "http://localhost:7547",
        "KEYCLOAK_URL": "https://test-keycloak.com:8443",
        "KEYCLOAK_REALM": "test-realm",
        "KEYCLOAK_CLIENT_ID": "test-client",
        "KEYCLOAK_CLIENT_SECRET": "test-secret"
    }
    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def client(mock_env_vars):
    """Create test client"""
    return ACSZeepClient()


@pytest.mark.asyncio
async def test_client_initialization(mock_env_vars):
    """Test client initialization"""
    client = ACSZeepClient()
    
    assert client.base_url == "http://localhost:7547"
    assert client.auth_manager.keycloak_url == "https://test-keycloak.com:8443"
    assert client.auth_manager.realm == "test-realm"
    assert client.auth_manager.client_id == "test-client"
    assert client.auth_manager.client_secret == "test-secret"
    
    await client.close()


@pytest.mark.asyncio
async def test_client_initialization_with_params():
    """Test client initialization with parameters"""
    client = ACSZeepClient(
        base_url="http://custom:8080",
        keycloak_url="https://custom-keycloak.com",
        realm="custom-realm",
        client_id="custom-client",
        client_secret="custom-secret"
    )
    
    assert client.base_url == "http://custom:8080"
    assert client.auth_manager.keycloak_url == "https://custom-keycloak.com"
    assert client.auth_manager.realm == "custom-realm"
    
    await client.close()


def test_client_initialization_missing_params():
    """Test client initialization with missing parameters"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            ACSZeepClient()


@pytest.mark.asyncio
@patch('acs_zeep_client.auth.AuthManager.authenticate')
async def test_authentication_success(mock_authenticate, client):
    """Test successful authentication"""
    mock_authenticate.return_value = AsyncMock()
    
    await client.authenticate()
    
    assert client._authenticated
    mock_authenticate.assert_called_once()


@pytest.mark.asyncio
@patch('acs_zeep_client.auth.AuthManager.authenticate')
async def test_authentication_failure(mock_authenticate, client):
    """Test authentication failure"""
    mock_authenticate.side_effect = Exception("Auth failed")
    
    with pytest.raises(AuthenticationError):
        await client.authenticate()
    
    assert not client._authenticated


@pytest.mark.asyncio
async def test_context_manager(mock_env_vars):
    """Test async context manager"""
    with patch('acs_zeep_client.client.ACSZeepClient.authenticate') as mock_auth:
        mock_auth.return_value = AsyncMock()
        
        async with ACSZeepClient() as client:
            assert isinstance(client, ACSZeepClient)
            mock_auth.assert_called_once()


@pytest.mark.asyncio
@patch('acs_zeep_client.client.ACSZeepClient.ensure_authenticated')
@patch('acs_zeep_client.api.monitoring.MonitoringAPI.get_health_check')
async def test_test_connection_success(mock_health, mock_ensure_auth, client):
    """Test successful connection test"""
    mock_ensure_auth.return_value = AsyncMock()
    mock_health.return_value = {"status": "healthy"}
    
    result = await client.test_connection()
    
    assert result["success"] is True
    assert "Connection successful" in result["message"]
    mock_ensure_auth.assert_called_once()
    mock_health.assert_called_once()


@pytest.mark.asyncio
@patch('acs_zeep_client.client.ACSZeepClient.ensure_authenticated')
async def test_test_connection_failure(mock_ensure_auth, client):
    """Test connection test failure"""
    mock_ensure_auth.side_effect = Exception("Connection failed")
    
    result = await client.test_connection()
    
    assert result["success"] is False
    assert "Connection failed" in result["message"]


if __name__ == "__main__":
    pytest.main([__file__])
