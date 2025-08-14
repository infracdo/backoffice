"""
Basic usage example for ACS ZEEP Client
"""

import asyncio
import os
from dotenv import load_dotenv
from acs_zeep_client import ACSZeepClient

# Load environment variables from .env file
load_dotenv()


async def main():
    """Basic usage example"""
    
    # Initialize client with environment variables
    # You can also pass parameters directly
    client = ACSZeepClient(
        base_url="http://localhost:7547",
        keycloak_url="https://wcdssi.apolloglobal.net:8443",
        realm="workconnect-test",
        client_id="your-service-account-client-id",
        client_secret="your-client-secret"
    )
    
    try:
        # Test connection
        print("Testing connection...")
        connection_test = await client.test_connection()
        if connection_test["success"]:
            print("✅ Connected successfully!")
        else:
            print(f"❌ Connection failed: {connection_test['message']}")
            return
        
        # Get system status
        print("\nGetting system status...")
        status = await client.monitoring.get_system_status()
        print(f"System status: {status}")
        
        # List devices
        print("\nListing devices...")
        devices = await client.devices.get_all(page_size=5)
        print(f"Found {len(devices)} devices")
        
        for device in devices[:3]:  # Show first 3 devices
            print(f"  - {device.serial_number}: {device.model} ({device.status})")
        
        # List groups
        print("\nListing groups...")
        groups = await client.groups.get_all()
        print(f"Found {len(groups)} groups")
        
        for group in groups[:3]:  # Show first 3 groups
            print(f"  - {group.name}: {group.description}")
        
        # Get ZEEP status
        print("\nGetting ZEEP status...")
        zeep_status = await client.zeep.get_status()
        print(f"ZEEP status: {zeep_status}")
        
        print("\n✅ Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Always close the client
        await client.close()


# Context manager example
async def context_manager_example():
    """Example using async context manager"""
    
    async with ACSZeepClient() as client:
        # Client is automatically authenticated
        devices = await client.devices.get_all(page_size=3)
        print(f"Found {len(devices)} devices using context manager")
        
        # Client is automatically closed when exiting context


if __name__ == "__main__":
    print("Running basic usage example...")
    asyncio.run(main())
    
    print("\nRunning context manager example...")
    asyncio.run(context_manager_example())
