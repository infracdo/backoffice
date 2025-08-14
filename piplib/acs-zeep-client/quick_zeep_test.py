"""
Quick test script to verify ZEEP API connectivity and authentication
"""

import asyncio
import os
from dotenv import load_dotenv
from acs_zeep_client import ACSZeepClient


async def quick_zeep_test():
    """Quick test of ZEEP API connectivity"""
    
    # Load environment variables
    load_dotenv(override=True)
    
    print("🚀 Quick ZEEP API Test")
    print("=" * 40)
    
    # Check environment variables
    print("\n🔧 Environment Check:")
    keycloak_url = os.getenv("KEYCLOAK_URL")
    api_base_url = os.getenv("API_BASE_URL")
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    
    print(f"Keycloak URL: {keycloak_url}")
    print(f"API Base URL: {api_base_url}")
    print(f"Client ID: {client_id}")
    print(f"Client Secret: {'*' * 20 if client_secret else 'Not set'}")
    
    if not all([keycloak_url, api_base_url, client_id, client_secret]):
        print("❌ Missing required environment variables!")
        return
    
    try:
        async with ACSZeepClient() as client:
            print("\n🔑 Authentication successful!")
            
            # Test simple API call
            print("\n📋 Testing account list retrieval:")
            accounts = await client.zeep.retrieve_account_list(debug=True)
            
            if isinstance(accounts, list):
                print(f"✅ Success: Found {len(accounts)} subscriber accounts")
                if accounts:
                    print("Sample account data:")
                    print(f"  {accounts[0]}")
            else:
                print(f"✅ Response received: {accounts}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if the Spring Boot API is running")
        print("2. Verify Keycloak server is accessible")
        print("3. Confirm client credentials are correct")
        print("4. Check network connectivity")


if __name__ == "__main__":
    asyncio.run(quick_zeep_test())
