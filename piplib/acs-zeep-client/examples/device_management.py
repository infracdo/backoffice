"""
Device management example for ACS ZEEP Client
"""

import asyncio
from acs_zeep_client import ACSZeepClient


async def device_management_example():
    """Example of device management operations"""
    
    async with ACSZeepClient() as client:
        print("=== Device Management Example ===\n")
        
        # List all devices
        print("1. Listing all devices...")
        devices = await client.devices.get_all()
        print(f"Total devices: {len(devices)}")
        
        if not devices:
            print("No devices found. Make sure your ACS has some registered devices.")
            return
        
        # Get first device for examples
        device = devices[0]
        device_id = device.id or device.serial_number
        print(f"Using device: {device_id} ({device.model})")
        
        # Get detailed device information
        print("\n2. Getting device details...")
        device_info = await client.devices.get_device_info(device_id)
        print(f"Device info keys: {list(device_info.keys())}")
        
        # Get device parameters
        print("\n3. Getting device parameters...")
        try:
            parameters = await client.devices.get_parameters(device_id)
            print(f"Device has {len(parameters)} parameters")
            
            # Show some example parameters
            for key, value in list(parameters.items())[:5]:
                print(f"  {key}: {value}")
        except Exception as e:
            print(f"Could not get parameters: {e}")
        
        # Get connection status
        print("\n4. Checking connection status...")
        try:
            status = await client.devices.get_connection_status(device_id)
            print(f"Connection status: {status}")
        except Exception as e:
            print(f"Could not get connection status: {e}")
        
        # Send a simple command (GetParameterNames)
        print("\n5. Sending GetParameterNames command...")
        try:
            command_result = await client.devices.send_command(
                device_id,
                "GetParameterNames",
                {"ParameterPath": "Device.", "NextLevel": True}
            )
            print(f"Command result: {command_result}")
        except Exception as e:
            print(f"Command failed: {e}")
        
        # Search for devices
        print("\n6. Searching devices...")
        search_results = await client.devices.get_all(
            search="Device",  # Search for devices with "Device" in any field
            page_size=3
        )
        print(f"Search found {len(search_results)} devices")
        
        print("\n=== Device Management Example Complete ===")


async def device_operations_example():
    """Example of device operations"""
    
    async with ACSZeepClient() as client:
        print("\n=== Device Operations Example ===\n")
        
        devices = await client.devices.get_all(page_size=1)
        if not devices:
            print("No devices available for operations")
            return
        
        device_id = devices[0].id or devices[0].serial_number
        print(f"Using device: {device_id}")
        
        # Note: These operations will actually affect the device
        # Uncomment only if you want to test with real devices
        
        print("\n1. Device operations (commented out for safety):")
        print("   # Reboot device")
        # await client.devices.reboot(device_id)
        
        print("   # Factory reset device")  
        # await client.devices.factory_reset(device_id)
        
        print("   # Set parameters")
        # await client.devices.set_parameters(device_id, {
        #     "Device.WiFi.SSID.1.SSID": "MyNewSSID"
        # })
        
        print("\n2. Safe operations:")
        
        # Get current parameters (safe operation)
        try:
            params = await client.devices.get_parameters(device_id)
            wifi_params = {k: v for k, v in params.items() if "WiFi" in k}
            print(f"   Found {len(wifi_params)} WiFi parameters")
        except Exception as e:
            print(f"   Could not get WiFi parameters: {e}")
        
        print("\n=== Device Operations Example Complete ===")


if __name__ == "__main__":
    asyncio.run(device_management_example())
    asyncio.run(device_operations_example())
