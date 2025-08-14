"""
Sample script to test all RADIUS API endpoints
"""

import asyncio
import os
from dotenv import load_dotenv
from acs_zeep_client import ACSZeepClient


async def test_radius_endpoints():
    """Test all RADIUS statistics and monitoring endpoints"""
    
    # Load environment variables
    load_dotenv(override=True)
    
    print("🔧 Testing RADIUS Statistics & Monitoring API")
    print("=" * 60)
    
    try:
        async with ACSZeepClient() as client:
            
            # Test 1: Current User Statistics
            print("\n👥 1. Current User Statistics:")
            try:
                current_users = await client.radius.count_currently_connected_users(debug=True)
                print(f"✅ Currently Connected Users: {current_users}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 2: Total User Count
            print("\n📊 2. Total User Statistics:")
            try:
                total_users = await client.radius.count_total_users(debug=True)
                print(f"✅ Total Users: {total_users}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 3: Access Point Statistics
            print("\n📡 3. Access Point Statistics:")
            try:
                total_aps = await client.radius.count_total_aps(debug=True)
                print(f"✅ Total APs: {total_aps}")
                
                current_aps = await client.radius.count_currently_connected_aps(debug=True)
                print(f"✅ Currently Connected APs: {current_aps}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 4: Daily Connection Statistics
            print("\n📈 4. Daily Connection Statistics:")
            try:
                connections_today = await client.radius.total_user_connections_today(debug=True)
                print(f"✅ Total User Connections Today: {connections_today}")
                
                sessions_today = await client.radius.total_user_sessions_today(debug=True)
                print(f"✅ Total User Sessions Today: {sessions_today}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 5: Daily Bandwidth and Time Statistics
            print("\n💾 5. Daily Bandwidth and Time Statistics:")
            try:
                bandwidth_today = await client.radius.total_bandwidth_consumption_today(debug=True)
                print(f"✅ Total Bandwidth Today: {bandwidth_today}")
                
                session_time_today = await client.radius.total_session_time_today(debug=True)
                print(f"✅ Total Session Time Today: {session_time_today}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 6: Average Statistics
            print("\n⏱️ 6. Average Statistics:")
            try:
                avg_connection_time = await client.radius.average_connection_time(debug=True)
                print(f"✅ Average Connection Time: {avg_connection_time}")
                
                avg_bandwidth = await client.radius.average_bandwidth_per_connection(debug=True)
                print(f"✅ Average Bandwidth per Connection: {avg_bandwidth}")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 7: Access Point Lists
            print("\n🌐 7. Access Point Information:")
            try:
                access_points = await client.radius.get_access_points(debug=True)
                print(f"✅ Access Points List: {access_points}")
                
                online_aps = await client.radius.get_access_points_online(debug=True)
                print(f"✅ Online APs: {len(online_aps) if isinstance(online_aps, list) else 'N/A'} found")
                if isinstance(online_aps, list) and online_aps:
                    print(f"Sample AP: {online_aps[0]}")
                
                all_aps = await client.radius.get_access_points_all(debug=True)
                print(f"✅ All APs: {len(all_aps) if isinstance(all_aps, list) else 'N/A'} found")
            except Exception as e:
                print(f"❌ Error: {e}")
            
            # Test 8: Users per Access Point
            print("\n📊 8. Users per Access Point:")
            try:
                users_count_per_ap = await client.radius.count_currently_connected_users_per_ap(debug=True)
                print(f"✅ User Count per AP: {len(users_count_per_ap) if isinstance(users_count_per_ap, list) else 'N/A'} APs")
                if isinstance(users_count_per_ap, list) and users_count_per_ap:
                    print(f"Sample: {users_count_per_ap[0]}")
                
                users_per_ap = await client.radius.currently_connected_users_per_ap(debug=True)
                print(f"✅ Connected Users per AP: {len(users_per_ap) if isinstance(users_per_ap, list) else 'N/A'} APs")
                if isinstance(users_per_ap, list) and users_per_ap:
                    print(f"Sample: {users_per_ap[0]}")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Client Error: {e}")
    
    print("\n" + "=" * 60)
    print("🏁 RADIUS API Testing Complete!")


async def test_radius_summary():
    """Get a summary of all RADIUS statistics"""
    
    # Load environment variables
    load_dotenv(override=True)
    
    print("📋 RADIUS Statistics Summary")
    print("=" * 40)
    
    try:
        async with ACSZeepClient() as client:
            # Get key statistics
            current_users = await client.radius.count_currently_connected_users()
            total_users = await client.radius.count_total_users()
            current_aps = await client.radius.count_currently_connected_aps()
            total_aps = await client.radius.count_total_aps()
            connections_today = await client.radius.total_user_connections_today()
            bandwidth_today = await client.radius.total_bandwidth_consumption_today()
            
            print(f"👥 Current Users: {current_users.get('currentlyConnectedUsers', 'N/A')}")
            print(f"📊 Total Users: {total_users.get('totalUsers', 'N/A')}")
            print(f"📡 Current APs: {current_aps.get('currentlyConnectedAPs', 'N/A')}")
            print(f"🌐 Total APs: {total_aps.get('totalAPs', 'N/A')}")
            print(f"📈 Connections Today: {connections_today.get('totalUserConnectionsToday', 'N/A')}")
            print(f"💾 Bandwidth Today: {bandwidth_today.get('totalBandwidthConsumptionToday', 'N/A')}")
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Full RADIUS API test")
    print("2. Quick summary")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        asyncio.run(test_radius_summary())
    else:
        asyncio.run(test_radius_endpoints())
