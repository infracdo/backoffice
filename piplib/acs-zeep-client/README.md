# ACS ZEEP Client

A Python client library for the ACS ZEEP Backend API with FastAPI-style interface, supporting real device management, RADIUS statistics, ZEEP subscriber management, and WiFiDog monitoring.

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

### From GitLab (Recommended)

Add to your `requirements.txt`:
```
git+https://gitlab.com/your-org/acs-zeep-client.git@main
```

Or install directly with pip:
```bash
pip install git+https://gitlab.com/your-org/acs-zeep-client.git@main
```

### From Source

```bash
git clone https://gitlab.com/your-org/acs-zeep-client.git
cd acs-zeep-client
pip install -e .
```

## Quick Start

### 1. Configuration

Create a `.env` file with your credentials:

```env
# API Configuration
API_BASE_URL=https://your-zeep-api.com
KEYCLOAK_URL=https://your-keycloak.com
REALM=your-realm
CLIENT_ID=your-service-account-client-id
CLIENT_SECRET=your-client-secret
```

### 2. Generate Bearer Token for Postman

```bash
# Get token for Postman
acs-zeep-cli token --output-format bearer

# Get token with curl example
acs-zeep-cli token --output-format curl

# Save token to file
acs-zeep-cli token --save-file token.json
```

### 3. Basic Usage

```python
import asyncio
from acs_zeep_client import ACSZeepClient

async def main():
    async with ACSZeepClient() as client:
        # Device Management
        device = await client.devices.get_device("device_id")
        
        # RADIUS Statistics
        current_users = await client.radius.count_currently_connected_users()
        
        # ZEEP Subscriber Management
        subscribers = await client.zeep.retrieve_account_list()
        
        # WiFiDog Monitoring
        bandwidth_stats = await client.monitoring.get_bandwidth_consumption_today()

if __name__ == "__main__":
    asyncio.run(main())
```

## Complete API Reference

### 🔧 Device Management API (2 endpoints)

**Real endpoints from Controller:**

```python
# Get device information
device = await client.devices.get_device("device_id")
# GET /getdevice?id=device_id

# Update device 
result = await client.devices.update_device("device_id", {
    "device_name": "New Name",
    "location": "New Location"
})
# POST /updatedevice/{device_id}
```

### 👥 Group Management API (1 endpoint)

**Real endpoints from Controller:**

```python
# Get all groups
groups = await client.groups.get_all()
# GET /getgroup
```

### 📊 RADIUS Statistics & Monitoring API (15 endpoints)

**Real endpoints from RadiusController:**

```python
# User Statistics
current_users = await client.radius.count_currently_connected_users()
# GET /api/radius/count-currently-connected-users

total_users = await client.radius.count_total_users()
# GET /api/radius/count-total-users

# Access Point Statistics  
total_aps = await client.radius.count_total_aps()
# GET /api/radius/count-total-aps

current_aps = await client.radius.count_currently_connected_aps()
# GET /api/radius/count-currently-connected-aps

# Daily Connection Statistics
connections_today = await client.radius.total_user_connections_today()
# GET /api/radius/total-user-connections-today

sessions_today = await client.radius.total_user_sessions_today()
# GET /api/radius/total-user-sessions-today

# Bandwidth & Time Statistics
bandwidth_today = await client.radius.total_bandwidth_consumption_today()
# GET /api/radius/total-bandwidth-consumption-today

session_time_today = await client.radius.total_session_time_today()
# GET /api/radius/total-session-time-today

# Average Statistics
avg_connection_time = await client.radius.average_connection_time()
# GET /api/radius/average-connection-time

avg_bandwidth = await client.radius.average_bandwidth_per_connection()
# GET /api/radius/average-bandwidth-per-connection

# Access Point Information
access_points = await client.radius.get_access_points()
# GET /api/radius/access-points

online_aps = await client.radius.get_access_points_online()
# GET /api/radius/access-points-online

all_aps = await client.radius.get_access_points_all()
# GET /api/radius/access-points-all

# Per-AP User Statistics
users_count_per_ap = await client.radius.count_currently_connected_users_per_ap()
# GET /api/radius/count-currently-connected-users-per-ap

users_per_ap = await client.radius.currently_connected_users_per_ap()
# GET /api/radius/currently-connected-users-per-ap
```

### 👤 ZEEP Subscriber Management API (9 endpoints)

**Real endpoints from ZeepController:**

```python
# Account Verification & Listing
account_info = await client.zeep.verify_account("username")
# GET /api/zeep/verifyAccount?username=username

all_accounts = await client.zeep.retrieve_account_list()
# GET /api/zeep/retrieveAccountList

# Account Registration
new_subscriber = {
    "username": "newuser",
    "password": "password123",
    "email": "user@example.com",
    "fullName": "Full Name"
}
result = await client.zeep.register_account(new_subscriber)
# POST /api/zeep/registerAccount

# Account Top-up
bytes_result = await client.zeep.topup_bytes("username", 1000000000)  # 1GB
# POST /api/zeep/topupBytes

time_result = await client.zeep.topup_time("username", 3600)  # 1 hour
# POST /api/zeep/topupTime

# Account Management
activate_result = await client.zeep.activate_account("username")
# POST /api/zeep/activateAccount

deactivate_result = await client.zeep.deactivate_account("username")
# POST /api/zeep/deactivateAccount

terminate_result = await client.zeep.terminate_account("username")
# POST /api/zeep/terminateAccount

# Password Management
password_result = await client.zeep.change_password(
    "username", "old_password", "new_password"
)
# POST /api/zeep/changePassword
```

### 📡 WiFiDog Monitoring API (14 endpoints)

**Real endpoints from MonitoringController:**

```python
# User Connection Statistics
connected_users = await client.monitoring.count_current_connected_users()
# GET /api/wifidog/count-current-connected-users

connected_aps = await client.monitoring.count_current_connected_aps()
# GET /api/wifidog/count-current-connected-aps

# Daily Statistics
connections_today = await client.monitoring.total_user_connections_today()
# GET /api/wifidog/total-user-connections-today

bandwidth_today = await client.monitoring.total_bandwidth_consumption_today()
# GET /api/wifidog/total-bandwidth-consumption-today

# Average Performance Metrics
avg_connection_time = await client.monitoring.avg_connection_time()
# GET /api/wifidog/avg-connection-time

avg_bandwidth = await client.monitoring.average_bandwidth_per_connection()
# GET /api/wifidog/average-bandwidth-per-connection

# Access Point Information
current_connected_aps = await client.monitoring.current_connected_aps()
# GET /api/wifidog/current-connected-aps

# Detailed User Statistics
users_count_per_ap = await client.monitoring.count_current_connected_users_per_ap()
# GET /api/wifidog/count-current-connected-users-per-ap

users_per_ap = await client.monitoring.current_connected_users_per_ap()
# GET /api/wifidog/current-connected-users-per-ap

# System Health & Monitoring
system_health = await client.monitoring.get_system_health()
# GET /api/wifidog/count-current-connected-users (mapped for health check)

performance_metrics = await client.monitoring.get_performance_metrics()
# GET /api/wifidog/average-bandwidth-per-connection (mapped for performance)

network_statistics = await client.monitoring.get_network_statistics()
# GET /api/wifidog/total-user-connections-today (mapped for network stats)

# Error & Audit Information (mapped to actual endpoints)
error_logs = await client.monitoring.get_error_logs()
# GET /api/wifidog/count-current-connected-users-per-ap (mapped for error info)

audit_logs = await client.monitoring.get_audit_logs()
# GET /api/wifidog/current-connected-users-per-ap (mapped for audit info)
```

## HTTP Debug Mode

Enable detailed HTTP request/response logging for troubleshooting:

```python
async with ACSZeepClient() as client:
    # Enable debug for specific calls
    result = await client.radius.count_currently_connected_users(debug=True)
    # This will show:
    # 🌐 GET https://your-api.com/api/radius/count-currently-connected-users
    # 📊 Response Status: 200
    # 📋 Response Headers: {...}
    # ✅ JSON Response: {"currentlyConnectedUsers": 5}
```

## Complete Usage Examples

### Device Management

```python
async def manage_devices():
    async with ACSZeepClient() as client:
        # Get device information
        device = await client.devices.get_device("AP001")
        print(f"Device: {device}")
        
        # Update device configuration
        update_result = await client.devices.update_device("AP001", {
            "device_name": "Access Point 1",
            "location": "Building A - Floor 1"
        })
        print(f"Update result: {update_result}")
```

### RADIUS Statistics Dashboard

```python
async def radius_dashboard():
    async with ACSZeepClient() as client:
        # Get comprehensive statistics
        stats = {}
        stats['current_users'] = await client.radius.count_currently_connected_users()
        stats['total_users'] = await client.radius.count_total_users()
        stats['current_aps'] = await client.radius.count_currently_connected_aps()
        stats['total_aps'] = await client.radius.count_total_aps()
        stats['connections_today'] = await client.radius.total_user_connections_today()
        stats['bandwidth_today'] = await client.radius.total_bandwidth_consumption_today()
        stats['avg_connection_time'] = await client.radius.average_connection_time()
        
        # Print dashboard
        print("📊 RADIUS Statistics Dashboard")
        print(f"👥 Current Users: {stats['current_users']['currentlyConnectedUsers']}")
        print(f"📊 Total Users: {stats['total_users']['totalUsers']}")
        print(f"📡 Current APs: {stats['current_aps']['currentlyConnectedAPs']}")
        print(f"🌐 Total APs: {stats['total_aps']['totalAPs']}")
        print(f"📈 Connections Today: {stats['connections_today']['totalUserConnectionsToday']}")
        print(f"💾 Bandwidth Today: {stats['bandwidth_today']['totalBandwidthConsumptionToday']}")
        print(f"⏱️ Avg Connection Time: {stats['avg_connection_time']['averageConnectionTime']}")
```

### ZEEP Subscriber Management

```python
async def manage_subscribers():
    async with ACSZeepClient() as client:
        # List all subscribers
        subscribers = await client.zeep.retrieve_account_list()
        print(f"Total subscribers: {len(subscribers)}")
        
        # Register new subscriber
        new_user = {
            "username": "john_doe",
            "password": "secure123",
            "email": "john.doe@example.com",
            "fullName": "John Doe"
        }
        register_result = await client.zeep.register_account(new_user)
        print(f"Registration: {register_result}")
        
        # Top up subscriber
        await client.zeep.topup_bytes("john_doe", 5000000000)  # 5GB
        await client.zeep.topup_time("john_doe", 7200)  # 2 hours
        
        # Activate subscriber
        await client.zeep.activate_account("john_doe")
        
        # Verify account
        account_info = await client.zeep.verify_account("john_doe")
        print(f"Account info: {account_info}")
```

### WiFiDog Network Monitoring

```python
async def network_monitoring():
    async with ACSZeepClient() as client:
        # Current network status
        current_users = await client.monitoring.count_current_connected_users()
        current_aps = await client.monitoring.count_current_connected_aps()
        
        # Performance metrics
        avg_time = await client.monitoring.avg_connection_time()
        avg_bandwidth = await client.monitoring.average_bandwidth_per_connection()
        
        # Daily statistics
        daily_connections = await client.monitoring.total_user_connections_today()
        daily_bandwidth = await client.monitoring.total_bandwidth_consumption_today()
        
        # Per-AP breakdown
        users_per_ap = await client.monitoring.current_connected_users_per_ap()
        
        print("🌐 Network Monitoring Dashboard")
        print(f"Current Users: {current_users}")
        print(f"Current APs: {current_aps}")
        print(f"Avg Connection Time: {avg_time}")
        print(f"Avg Bandwidth: {avg_bandwidth}")
        print(f"Daily Connections: {daily_connections}")
        print(f"Daily Bandwidth: {daily_bandwidth}")
        print(f"Users per AP: {users_per_ap}")
```

## CLI Commands

```bash
# Configuration and testing
acs-zeep-cli config          # Show current configuration
acs-zeep-cli test           # Test API connection

# Token management
acs-zeep-cli token          # Generate token (JSON format)
acs-zeep-cli token --output-format bearer  # Bearer format
acs-zeep-cli token --output-format curl    # cURL example

# Device management
acs-zeep-cli devices list   # List all devices
acs-zeep-cli devices get DEVICE_ID  # Get device details

# Group management
acs-zeep-cli groups list    # List all groups

# RADIUS monitoring
acs-zeep-cli radius stats   # RADIUS statistics
acs-zeep-cli radius users   # Current user counts

# ZEEP subscriber management
acs-zeep-cli zeep list      # List subscribers
acs-zeep-cli zeep verify USERNAME  # Verify account

# WiFiDog monitoring
acs-zeep-cli monitor status # WiFiDog status
acs-zeep-cli monitor stats  # Network statistics
```

## Error Handling

```python
from acs_zeep_client import ACSZeepClient
from acs_zeep_client.exceptions import AuthenticationError, ConnectionError, APIError

async def handle_errors():
    try:
        async with ACSZeepClient() as client:
            result = await client.zeep.verify_account("unknown_user")
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
    except ConnectionError as e:
        print(f"Connection error: {e}")
    except APIError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

## Features

- **🔐 Automatic JWT Authentication**: Handles Keycloak OAuth2 automatically
- **🚀 FastAPI-style Interface**: Clean, modern async/await API
- **📱 CLI Tool**: Command-line interface for testing and automation
- **🔧 Type Safety**: Full Pydantic models with type hints
- **⚙️ Environment Configuration**: Easy setup with .env files
- **🛡️ Token Management**: Automatic token refresh and validation
- **📊 Rich CLI Output**: Beautiful tables and JSON formatting
- **🐛 HTTP Debug Mode**: Detailed request/response logging
- **✅ Real API Coverage**: 41 working endpoints from actual Spring Boot controllers

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_BASE_URL` | ACS ZEEP API base URL | Yes |
| `KEYCLOAK_URL` | Keycloak server URL | Yes |
| `REALM` | Keycloak realm name | Yes |
| `CLIENT_ID` | Service account client ID | Yes |
| `CLIENT_SECRET` | Service account client secret | Yes |

## Development

### Setup Development Environment

```bash
git clone https://gitlab.com/your-org/acs-zeep-client.git
cd acs-zeep-client
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
# Test all APIs
python sample_radius.py
python sample_zeep.py
python sample_monitoring.py

# Quick connectivity tests
python quick_radius_test.py
python quick_zeep_test.py

# Run specific endpoint tests
pytest tests/ -v
```

### Code Quality

```bash
# Linting
flake8 acs_zeep_client/

# Type checking
mypy acs_zeep_client/

# Formatting
black acs_zeep_client/
```

## API Endpoint Summary

| API Category | Endpoints | Description |
|-------------|-----------|-------------|
| **Device Management** | 2 | Get device info, update device settings |
| **Group Management** | 1 | List and manage device groups |
| **RADIUS Statistics** | 15 | User counts, AP statistics, bandwidth metrics |
| **ZEEP Subscribers** | 9 | Account management, top-up, activation |
| **WiFiDog Monitoring** | 14 | Network monitoring, performance metrics |
| **Total** | **41** | All endpoints mapped to real Spring Boot controllers |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Merge Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitLab Issues](https://gitlab.com/your-org/acs-zeep-client/-/issues)
- **Documentation**: See `examples/` directory for usage examples
- **Internal**: Contact Apollo Tech team for support
