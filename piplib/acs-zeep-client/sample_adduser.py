import asyncio
from acs_zeep_client import ACSZeepClient
from datetime import datetime, timedelta
import json

async def main():
    """Test all ZEEP API endpoints with debug enabled"""
    try:
        # Using environment variables from .env file
        async with ACSZeepClient() as client:
            print("🔌 Connected to ACS ZEEP API")
            print("=" * 60)
            print("🧪 Testing all ZEEP API endpoints with HTTP debug enabled")
            print("=" * 60)
            
            # 1. Get ZEEP Status
            print("\n🟦 1. Testing get_status()")
            try:
                status = await client.zeep.get_status(debug=True)
                print(f"✅ Status: {json.dumps(status, indent=2)}")
            except Exception as e:
                print(f"❌ get_status failed: {e}")
            
            # 2. Get Monitoring Data
            print("\n🟦 2. Testing get_monitoring_data()")
            try:
                monitoring = await client.zeep.get_monitoring_data(debug=True)
                print(f"✅ Monitoring Data: {json.dumps(monitoring, indent=2)}")
            except Exception as e:
                print(f"❌ get_monitoring_data failed: {e}")
                
            # 3. Get Monitoring Data with time range
            print("\n🟦 3. Testing get_monitoring_data() with time range")
            try:
                end_time = datetime.now()
                start_time = end_time - timedelta(hours=1)
                monitoring_range = await client.zeep.get_monitoring_data(
                    start_time=start_time.isoformat(), 
                    end_time=end_time.isoformat(),
                    debug=True
                )
                print(f"✅ Monitoring Data (1h): {json.dumps(monitoring_range, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_monitoring_data with range failed: {e}")
            
            # 4. Get Services
            print("\n� 4. Testing get_services()")
            try:
                services = await client.zeep.get_services(debug=True)
                print(f"✅ Services: {json.dumps(services, indent=2)}")
            except Exception as e:
                print(f"❌ get_services failed: {e}")
            
            # 5. Get Service Details (try with a common service name)
            print("\n🟦 5. Testing get_service_details()")
            try:
                service_details = await client.zeep.get_service_details("zeep-backend", debug=True)
                print(f"✅ Service Details: {json.dumps(service_details, indent=2)}")
            except Exception as e:
                print(f"❌ get_service_details failed: {e}")
            
            # 6. Get Configuration
            print("\n🟦 6. Testing get_configuration()")
            try:
                config = await client.zeep.get_configuration(debug=True)
                print(f"✅ Configuration: {json.dumps(config, indent=2)}")
            except Exception as e:
                print(f"❌ get_configuration failed: {e}")
            
            # 7. Get Metrics
            print("\n🟦 7. Testing get_metrics()")
            try:
                metrics = await client.zeep.get_metrics(debug=True)
                print(f"✅ Metrics: {json.dumps(metrics, indent=2)}")
            except Exception as e:
                print(f"❌ get_metrics failed: {e}")
                
            # 8. Get Metrics with time range
            print("\n🟦 8. Testing get_metrics() with time range")
            try:
                end_time = datetime.now()
                start_time = end_time - timedelta(minutes=30)
                metrics_range = await client.zeep.get_metrics(
                    start_time=start_time.isoformat(),
                    end_time=end_time.isoformat(),
                    debug=True
                )
                print(f"✅ Metrics (30m): {json.dumps(metrics_range, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_metrics with range failed: {e}")
            
            # 9. Get Alerts
            print("\n🟦 9. Testing get_alerts()")
            try:
                alerts = await client.zeep.get_alerts(debug=True)
                print(f"✅ Alerts: {json.dumps(alerts, indent=2)}")
            except Exception as e:
                print(f"❌ get_alerts failed: {e}")
                
            # 10. Get Alerts with severity filter
            print("\n🟦 10. Testing get_alerts() with severity filter")
            try:
                critical_alerts = await client.zeep.get_alerts(severity="critical", debug=True)
                print(f"✅ Critical Alerts: {json.dumps(critical_alerts, indent=2)}")
            except Exception as e:
                print(f"❌ get_alerts with severity failed: {e}")
                
            # 11. Get Alerts with status filter
            print("\n🟦 11. Testing get_alerts() with status filter")
            try:
                active_alerts = await client.zeep.get_alerts(status="active", debug=True)
                print(f"✅ Active Alerts: {json.dumps(active_alerts, indent=2)}")
            except Exception as e:
                print(f"❌ get_alerts with status failed: {e}")
            
            print("\n" + "=" * 60)
            print("🎉 ZEEP API endpoint testing completed!")
            print("=" * 60)
            
            # Summary
            print("\n📊 ZEEP API Endpoints Tested:")
            endpoints = [
                "get_status()",
                "get_monitoring_data()",
                "get_monitoring_data(start_time, end_time)",
                "get_services()",
                "get_service_details(service_name)",
                "get_configuration()",
                "get_metrics()",
                "get_metrics(start_time, end_time)",
                "get_alerts()",
                "get_alerts(severity)",
                "get_alerts(status)"
            ]
            
            for i, endpoint in enumerate(endpoints, 1):
                print(f"  {i:2d}. {endpoint}")
                
            print("\n💡 Note: Some endpoints may return 404 if not implemented in the actual Spring Boot backend")
            print("🔍 Check the HTTP debug output above to see the actual API responses")
         
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())


