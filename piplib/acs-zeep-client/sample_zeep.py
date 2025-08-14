"""
Sample script to test all ZEEP subscriber management API endpoints
"""

import asyncio
import os
from dotenv import load_dotenv
from acs_zeep_client import ACSZeepClient


async def test_zeep_endpoints():
    """Test all ZEEP subscriber management endpoints"""
    
    # Load environment variables
    load_dotenv(override=True)
    
    print("🔧 Testing ZEEP Subscriber Management API")
    print("=" * 60)
    
    try:
        async with ACSZeepClient() as client:
            # Test 1: Retrieve all subscriber accounts
            print("\n📋 1. Retrieving all subscriber accounts:")
            try:
                accounts = await client.zeep.retrieve_account_list(debug=True)
                print(f"✅ Success: Found {len(accounts) if isinstance(accounts, list) else 'N/A'} accounts")
                print(f"Response: {accounts}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 2: Verify a specific account (if any exist)
            print("\n🔍 2. Verifying account (test username):")
            try:
                account_info = await client.zeep.verify_account("testuser", debug=True)
                print(f"✅ Success: {account_info}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 3: Register a new account
            print("\n➕ 3. Registering new subscriber account:")
            try:
                new_subscriber = {
                    "username": "sample_user",
                    "password": "sample_password",
                    "email": "sample@example.com",
                    "fullName": "Sample User"
                }
                result = await client.zeep.register_account(new_subscriber, debug=True)
                print(f"✅ Success: {result}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 4: Topup bytes for an account
            print("\n💾 4. Topping up bytes for subscriber:")
            try:
                result = await client.zeep.topup_bytes("sample_user", 1000000000, debug=True)  # 1GB in bytes
                print(f"✅ Success: {result}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 5: Topup time for an account
            print("\n⏰ 5. Topping up time for subscriber:")
            try:
                result = await client.zeep.topup_time("sample_user", 3600, debug=True)  # 1 hour in seconds
                print(f"✅ Success: {result}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 6: Activate account
            print("\n🟢 6. Activating subscriber account:")
            try:
                result = await client.zeep.activate_account("sample_user", debug=True)
                print(f"✅ Success: {result}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 7: Deactivate account
            print("\n🔴 7. Deactivating subscriber account:")
            try:
                result = await client.zeep.deactivate_account("sample_user", debug=True)
                print(f"✅ Success: {result}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 8: Change password
            print("\n🔑 8. Changing subscriber password:")
            try:
                result = await client.zeep.change_password("sample_user", "sample_password", "new_password", debug=True)
                print(f"✅ Success: {result}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 9: Terminate account (delete)
            print("\n🗑️  9. Terminating subscriber account:")
            try:
                result = await client.zeep.terminate_account("sample_user", debug=True)
                print(f"✅ Success: {result}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 10: Test all available endpoints
            print("\n📊 10. Testing all ZEEP endpoints:")
            try:
                # List all accounts
                all_accounts = await client.zeep.retrieve_account_list(debug=True)
                print(f"✅ All accounts: {len(all_accounts) if isinstance(all_accounts, list) else 'N/A'} found")
                
                # If we have accounts, verify the first one
                if isinstance(all_accounts, list) and all_accounts:
                    first_account = all_accounts[0]
                    if isinstance(first_account, dict) and 'username' in first_account:
                        username = first_account['username']
                        account_details = await client.zeep.verify_account(username, debug=True)
                        print(f"✅ Verified account '{username}': {account_details}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Client Error: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 ZEEP API Testing Complete!")


async def test_specific_subscriber(username: str):
    """Test operations for a specific subscriber"""
    
    # Load environment variables
    load_dotenv(override=True)
    
    print(f"🔧 Testing ZEEP operations for subscriber: {username}")
    print("=" * 60)
    
    try:
        async with ACSZeepClient() as client:
            # Verify account exists
            print(f"\n🔍 Verifying account: {username}")
            account_info = await client.zeep.verify_account(username, debug=True)
            print(f"Account info: {account_info}")
            
            # Get all accounts to see if our user is there
            print(f"\n📋 Checking all accounts:")
            all_accounts = await client.zeep.retrieve_account_list(debug=True)
            print(f"Total accounts: {len(all_accounts) if isinstance(all_accounts, list) else 'N/A'}")
            
            # Try to activate the account
            print(f"\n🟢 Activating account: {username}")
            result = await client.zeep.activate_account(username, debug=True)
            print(f"Activation result: {result}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Test all ZEEP endpoints")
    print("2. Test specific subscriber")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        username = input("Enter username to test: ").strip()
        if username:
            asyncio.run(test_specific_subscriber(username))
        else:
            print("No username provided, running full test suite")
            asyncio.run(test_zeep_endpoints())
    else:
        asyncio.run(test_zeep_endpoints())
