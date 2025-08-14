"""
CLI tool for ACS ZEEP Client
"""

import asyncio
import os
import sys
from typing import Optional

try:
    import typer
    from rich.console import Console
    from rich.table import Table
    from rich.json import JSON
    from rich.panel import Panel
    from dotenv import load_dotenv
except ImportError:
    print("CLI dependencies not installed. Install with: pip install 'acs-zeep-client[dev]'")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

from .client import ACSZeepClient
from .exceptions import ACSZeepException

app = typer.Typer(name="acs-zeep-cli", help="CLI for ACS ZEEP Backend API")
console = Console()

# Create sub-apps for different command groups
devices_app = typer.Typer(help="Device management commands")
monitor_app = typer.Typer(help="Monitoring commands")
groups_app = typer.Typer(help="Group management commands")

# Add sub-apps to main app
app.add_typer(devices_app, name="devices")
app.add_typer(monitor_app, name="monitor")
app.add_typer(groups_app, name="groups")

console = Console()


def create_client() -> ACSZeepClient:
    """Create and configure ACS ZEEP client from environment variables"""
    # Try to load .env files from current directory and parent directories
    from pathlib import Path
    
    current_dir = Path.cwd()
    
    # Check current directory and up to 3 parent directories for .env files
    for i in range(4):
        env_file = current_dir / ".env"
        if env_file.exists():
            load_dotenv(env_file, override=True)  # Override existing environment variables
            break
        current_dir = current_dir.parent
        if current_dir == current_dir.parent:  # Reached root
            break
    
    return ACSZeepClient()


async def async_run(coro):
    """Run async function"""
    return await coro


# Device commands
@devices_app.command("list")
def list_devices(
    page: int = typer.Option(1, help="Page number"),
    size: int = typer.Option(10, help="Page size"),
    search: Optional[str] = typer.Option(None, help="Search term"),
    status: Optional[str] = typer.Option(None, help="Device status filter")
):
    """List all devices"""
    async def _list_devices():
        async with create_client() as client:
            devices = await client.devices.get_all(page=page, page_size=size, search=search, status=status)
            
            if not devices:
                console.print("No devices found", style="yellow")
                return
            
            table = Table(title="Devices")
            table.add_column("ID", style="cyan")
            table.add_column("Serial Number", style="green")
            table.add_column("Model", style="blue")
            table.add_column("IP Address", style="magenta")
            table.add_column("Status", style="yellow")
            
            for device in devices:
                table.add_row(
                    str(device.id or ""),
                    device.serial_number or "",
                    device.model or "",
                    device.ip_address or "",
                    device.status or ""
                )
            
            console.print(table)
    
    try:
        asyncio.run(_list_devices())
    except ACSZeepException as e:
        console.print(f"Error: {e}", style="red")
        raise typer.Exit(1)


@devices_app.command("get")
def get_device(device_id: str = typer.Argument(..., help="Device ID")):
    """Get device details"""
    async def _get_device():
        async with create_client() as client:
            device = await client.devices.get_by_id(device_id)
            console.print(JSON.from_data(device.dict()))
    
    try:
        asyncio.run(_get_device())
    except ACSZeepException as e:
        console.print(f"Error: {e}", style="red")
        raise typer.Exit(1)


@devices_app.command("reboot")
def reboot_device(device_id: str = typer.Argument(..., help="Device ID")):
    """Reboot a device"""
    async def _reboot_device():
        async with create_client() as client:
            result = await client.devices.reboot(device_id)
            console.print(f"Reboot command sent to device {device_id}", style="green")
            console.print(JSON.from_data(result))
    
    try:
        asyncio.run(_reboot_device())
    except ACSZeepException as e:
        console.print(f"Error: {e}", style="red")
        raise typer.Exit(1)


# Monitoring commands
@monitor_app.command("status")
def system_status():
    """Get system status"""
    async def _system_status():
        async with create_client() as client:
            status = await client.monitoring.get_system_status()
            console.print(Panel(JSON.from_data(status), title="System Status"))
    
    try:
        asyncio.run(_system_status())
    except ACSZeepException as e:
        console.print(f"Error: {e}", style="red")
        raise typer.Exit(1)


@monitor_app.command("health")
def health_check():
    """Run health check"""
    async def _health_check():
        async with create_client() as client:
            health = await client.monitoring.get_health_check()
            console.print(Panel(JSON.from_data(health), title="Health Check"))
    
    try:
        asyncio.run(_health_check())
    except ACSZeepException as e:
        console.print(f"Error: {e}", style="red")
        raise typer.Exit(1)


# Group commands
@groups_app.command("list")
def list_groups():
    """List all groups"""
    async def _list_groups():
        async with create_client() as client:
            groups = await client.groups.get_all()
            
            if not groups:
                console.print("No groups found", style="yellow")
                return
            
            table = Table(title="Groups")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Description", style="blue")
            
            for group in groups:
                table.add_row(
                    str(group.id or ""),
                    group.name or "",
                    group.description or ""
                )
            
            console.print(table)
    
    try:
        asyncio.run(_list_groups())
    except ACSZeepException as e:
        console.print(f"Error: {e}", style="red")
        raise typer.Exit(1)


# Test connection command
@app.command("test")
def test_connection():
    """Test connection to ACS ZEEP API"""
    async def _test_connection():
        client = create_client()
        result = await client.test_connection()
        
        if result["success"]:
            console.print("✅ Connection successful!", style="green")
            console.print(JSON.from_data(result))
        else:
            console.print("❌ Connection failed!", style="red")
            console.print(f"Error: {result['message']}", style="red")
        
        await client.close()
    
    try:
        asyncio.run(_test_connection())
    except Exception as e:
        console.print(f"❌ Connection failed: {e}", style="red")
        raise typer.Exit(1)


# Token generation command for Postman
@app.command("token")
def generate_token(
    output_format: str = typer.Option("json", help="Output format: json, bearer, curl"),
    save_file: Optional[str] = typer.Option(None, help="Save token to file"),
    show_expires: bool = typer.Option(False, help="Show token expiration time")
):
    """Generate bearer token for Postman/API testing"""
    async def _generate_token():
        from datetime import datetime, timedelta
        
        # Load .env file for current directory
        from pathlib import Path
        current_dir = Path.cwd()
        
        for i in range(4):
            env_file = current_dir / ".env"
            if env_file.exists():
                load_dotenv(env_file, override=True)
                break
            current_dir = current_dir.parent
            if current_dir == current_dir.parent:
                break
        
        # Create auth manager directly
        from acs_zeep_client.auth import AuthManager
        
        keycloak_url = os.getenv("KEYCLOAK_URL")
        realm = os.getenv("KEYCLOAK_REALM")
        client_id = os.getenv("KEYCLOAK_CLIENT_ID")
        client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET")
        
        if not all([keycloak_url, realm, client_id, client_secret]):
            console.print("❌ Missing Keycloak configuration. Check your .env file.", style="red")
            return
        
        try:
            auth_manager = AuthManager(keycloak_url, realm, client_id, client_secret)
            console.print("🔐 Requesting token from Keycloak...", style="blue")
            
            token_response = await auth_manager.authenticate()
            
            # Calculate expiration time
            expires_at = datetime.now() + timedelta(seconds=token_response.expires_in)
            
            if output_format.lower() == "bearer":
                # Just the bearer token
                result = f"Bearer {token_response.access_token}"
                console.print(result)
                
            elif output_format.lower() == "curl":
                # curl command example
                base_url = os.getenv("ACS_ZEEP_BASE_URL", "http://localhost:7547")
                result = f'curl -H "Authorization: Bearer {token_response.access_token}" "{base_url}/api/devices"'
                console.print(result)
                
            else:  # json format (default)
                result_data = {
                    "access_token": token_response.access_token,
                    "token_type": token_response.token_type,
                    "expires_in": token_response.expires_in,
                    "expires_at": expires_at.isoformat(),
                    "bearer_header": f"Bearer {token_response.access_token}",
                    "curl_example": f'curl -H "Authorization: Bearer {token_response.access_token}" "{os.getenv("ACS_ZEEP_BASE_URL", "http://localhost:7547")}/api/devices"'
                }
                
                if show_expires:
                    result_data["expires_at_local"] = expires_at.strftime("%Y-%m-%d %H:%M:%S")
                    result_data["valid_for_minutes"] = round(token_response.expires_in / 60, 1)
                
                console.print(Panel(JSON.from_data(result_data), title="🔑 Bearer Token"))
                result = token_response.access_token
            
            # Save to file if requested
            if save_file:
                with open(save_file, 'w') as f:
                    if output_format.lower() == "json":
                        import json
                        json.dump(result_data, f, indent=2)
                    else:
                        f.write(result)
                console.print(f"💾 Token saved to {save_file}", style="green")
            
            # Show usage instructions
            console.print("\n📋 Postman Usage:", style="bold blue")
            console.print("1. Copy the access_token value")
            console.print("2. In Postman, go to Authorization tab")
            console.print("3. Select 'Bearer Token' type")
            console.print("4. Paste the token")
            console.print(f"5. Token expires in {round(token_response.expires_in / 60, 1)} minutes")
            
            console.print("✅ Token generated successfully!", style="green")
            
        except Exception as e:
            console.print(f"❌ Failed to generate token: {e}", style="red")
            raise typer.Exit(1)
    
    try:
        asyncio.run(_generate_token())
    except KeyboardInterrupt:
        console.print("\n❌ Token generation cancelled", style="yellow")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        raise typer.Exit(1)


# Configuration command
@app.command("config")
def show_config():
    """Show current configuration"""
    # Try to load .env files from current directory and parent directories
    from pathlib import Path
    
    env_files_found = []
    current_dir = Path.cwd()
    
    # Check current directory and up to 3 parent directories
    for i in range(4):
        env_file = current_dir / ".env"
        if env_file.exists():
            env_files_found.append(str(env_file))
            load_dotenv(env_file, override=True)  # Override existing environment variables
        current_dir = current_dir.parent
        if current_dir == current_dir.parent:  # Reached root
            break
    
    config = {
        "Environment Files Found": env_files_found if env_files_found else ["None"],
        "ACS_ZEEP_BASE_URL": os.getenv("ACS_ZEEP_BASE_URL", "Not set"),
        "KEYCLOAK_URL": os.getenv("KEYCLOAK_URL", "Not set"),
        "KEYCLOAK_REALM": os.getenv("KEYCLOAK_REALM", "Not set"),
        "KEYCLOAK_CLIENT_ID": os.getenv("KEYCLOAK_CLIENT_ID", "Not set"),
        "KEYCLOAK_CLIENT_SECRET": "***" if os.getenv("KEYCLOAK_CLIENT_SECRET") else "Not set"
    }
    
    console.print(Panel(JSON.from_data(config), title="Configuration"))


def main():
    """Main CLI entry point"""
    app()


if __name__ == "__main__":
    main()
