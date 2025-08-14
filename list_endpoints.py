import os
import httpx
import json
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def list_endpoints():
    api_key = os.getenv('PORTAINER_API_KEY')
    portainer_url = os.getenv('PORTAINER_URL')
    
    if not api_key or not portainer_url:
        print("Missing PORTAINER_API_KEY or PORTAINER_URL in .env file")
        return
    
    url = f"{portainer_url}/api/endpoints"
    headers = {"X-API-Key": api_key}
    
    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            
            endpoints = response.json()
            print("Available endpoints:")
            for endpoint in endpoints:
                print(f"  ID: {endpoint.get('Id')}, Name: {endpoint.get('Name')}, URL: {endpoint.get('URL')}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(list_endpoints())
