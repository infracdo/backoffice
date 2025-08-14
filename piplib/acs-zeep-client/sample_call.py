import asyncio
from acs_zeep_client import ACSZeepClient

device_id = "G1LQAJU141938"

async def main():
    """Sample usage of ACS ZEEP Client"""
    try:
        # Using environment variables from .env file
        async with ACSZeepClient() as client:
            print("🔌 Connected to ACS ZEEP API")
            # get groups
            groups = await client.groups.get_all()
            parent_concat = None
            print(f"📁 Found {len(groups)} groups:")
            for group in groups:
                print(group)
                print(f" - {group.name} (ID: {group.id})")
                parent_concat = group.parent_concat

            # Get a specific device by ID
            print(f"🔍 Fetching device with ID: {device_id}")
            device = await client.devices.get_by_id(device_id)
            if device:
                print(device)
                print(f"✅ Found device: {device.device_name} (ID: {device.serial_number})")

                # # update device information
                new_name = f"ZEEP-{device.serial_number}"
                print(f"✏️ Updating device name to: {new_name}")
                device.device_name = new_name
                device.parent = parent_concat
                await client.devices.update(device.id, device_data=device.model_dump())
                print(f"✅ Device name updated to: {new_name}")

            else:
                print(f"📭 Device with ID {device_id} not found")

                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())


