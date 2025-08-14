# ACS ZEEP Client

A Python client library for the ACS ZEEP Backend API with FastAPI-style interface.

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

```bash
cp .env.example .env
# Edit .env with your actual values
```

```env
ACS_ZEEP_BASE_URL=https://your-zeep-api.com
KEYCLOAK_URL=https://your-keycloak.com
KEYCLOAK_REALM=your-realm
KEYCLOAK_CLIENT_ID=your-service-account-client-id
KEYCLOAK_CLIENT_SECRET=your-client-secret
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

### 3. Use the CLI

```bash
# Test connection
acs-zeep-cli test

# List devices
acs-zeep-cli devices list

# List groups
acs-zeep-cli groups list

# System monitoring
acs-zeep-cli monitor status

# Check configuration
acs-zeep-cli config
```

### 4. Use in Python Code

```python
from acs_zeep_client import ACSZeepClient

# Using environment variables
async with ACSZeepClient() as client:
    devices = await client.devices.get_all()
    for device in devices:
        print(f"{device.device_name}: {device.serial_number}")

# Using parameters directly
client = ACSZeepClient(
    base_url="https://your-zeep-api.com",
    keycloak_url="https://your-keycloak.com",
    realm="your-realm",
    client_id="your-service-account-client-id",
    client_secret="your-client-secret"
)

try:
    await client.authenticate()
    devices = await client.devices.get_all()
    groups = await client.groups.get_all()
    status = await client.monitoring.get_system_status()
finally:
    await client.close()
```

## Features

- **🔐 Automatic JWT Authentication**: Handles Keycloak OAuth2 automatically
- **🚀 FastAPI-style Interface**: Clean, modern async/await API
- **📱 CLI Tool**: Command-line interface for testing and automation
- **🔧 Type Safety**: Full Pydantic models with type hints
- **⚙️ Environment Configuration**: Easy setup with .env files
- **🛡️ Token Management**: Automatic token refresh and validation
- **📊 Rich CLI Output**: Beautiful tables and JSON formatting

## API Coverage

### Device Management
- List all devices
- Get device by ID
- Device commands (reboot, factory reset)
- Parameter management

### Group Management  
- List all groups
- Create/manage groups
- Group operations

### Monitoring
- System status
- Connected users/APs
- Connection statistics
- Health checks

### Authentication
- Service account authentication
- Token generation for external tools
- Automatic token refresh

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

## Configuration Options

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `ACS_ZEEP_BASE_URL` | ACS ZEEP API base URL | `http://localhost:7547` |
| `KEYCLOAK_URL` | Keycloak server URL | Required |
| `KEYCLOAK_REALM` | Keycloak realm name | Required |
| `KEYCLOAK_CLIENT_ID` | Service account client ID | Required |
| `KEYCLOAK_CLIENT_SECRET` | Service account client secret | Required |

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
acs-zeep-cli devices reboot DEVICE_ID  # Reboot device

# Group management
acs-zeep-cli groups list    # List all groups

# Monitoring
acs-zeep-cli monitor status # System status
acs-zeep-cli monitor health # Health check
```

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
