import asyncio
from acs_zeep_client import ACSZeepClient
from datetime import datetime, timedelta
import json

async def main():
    """Test all Monitoring API endpoints with debug enabled"""
    try:
        # Using environment variables from .env file
        async with ACSZeepClient() as client:
            print("🔌 Connected to ACS ZEEP API")
            print("=" * 70)
            print("🧪 Testing all MONITORING API endpoints with HTTP debug enabled")
            print("=" * 70)
            
            # 1. Get System Status
            print("\n🟦 1. Testing get_system_status()")
            try:
                status = await client.monitoring.get_system_status(debug=True)
                print(f"✅ System Status: {json.dumps(status, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_system_status failed: {e}")
            
            # 2. Get Health Check
            print("\n🟦 2. Testing get_health_check()")
            try:
                health = await client.monitoring.get_health_check(debug=True)
                print(f"✅ Health Check: {json.dumps(health, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_health_check failed: {e}")
                
            # 3. Get Service Status
            print("\n🟦 3. Testing get_service_status()")
            try:
                service_status = await client.monitoring.get_service_status(debug=True)
                print(f"✅ Service Status: {json.dumps(service_status, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_service_status failed: {e}")
                
            # 4. Get Service Status with bandwidth
            print("\n🟦 4. Testing get_service_status(bandwidth)")
            try:
                bandwidth_status = await client.monitoring.get_service_status("bandwidth", debug=True)
                print(f"✅ Bandwidth Status: {json.dumps(bandwidth_status, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_service_status(bandwidth) failed: {e}")
            
            # 5. Get Database Status
            print("\n🟦 5. Testing get_database_status()")
            try:
                db_status = await client.monitoring.get_database_status(debug=True)
                print(f"✅ Database Status: {json.dumps(db_status, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_database_status failed: {e}")
            
            # 6. Get Performance Metrics
            print("\n🟦 6. Testing get_performance_metrics()")
            try:
                perf_metrics = await client.monitoring.get_performance_metrics(debug=True)
                print(f"✅ Performance Metrics: {json.dumps(perf_metrics, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_performance_metrics failed: {e}")
                
            # 7. Get Performance Metrics with bandwidth type
            print("\n🟦 7. Testing get_performance_metrics(bandwidth)")
            try:
                bandwidth_metrics = await client.monitoring.get_performance_metrics("bandwidth", debug=True)
                print(f"✅ Bandwidth Metrics: {json.dumps(bandwidth_metrics, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_performance_metrics(bandwidth) failed: {e}")
                
            # 8. Get Error Logs
            print("\n🟦 8. Testing get_error_logs()")
            try:
                error_logs = await client.monitoring.get_error_logs(debug=True)
                print(f"✅ Error Logs: {json.dumps(error_logs, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_error_logs failed: {e}")
                
            # 9. Get Audit Logs
            print("\n🟦 9. Testing get_audit_logs()")
            try:
                audit_logs = await client.monitoring.get_audit_logs(debug=True)
                print(f"✅ Audit Logs: {json.dumps(audit_logs, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_audit_logs failed: {e}")
                
            # 10. Get System Info
            print("\n🟦 10. Testing get_system_info()")
            try:
                system_info = await client.monitoring.get_system_info(debug=True)
                print(f"✅ System Info: {json.dumps(system_info, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_system_info failed: {e}")
                
            # 11. Get Uptime
            print("\n🟦 11. Testing get_uptime()")
            try:
                uptime = await client.monitoring.get_uptime(debug=True)
                print(f"✅ Uptime: {json.dumps(uptime, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_uptime failed: {e}")
                
            # 12. Run Diagnostics
            print("\n🟦 12. Testing run_diagnostics()")
            try:
                diagnostics = await client.monitoring.run_diagnostics(debug=True)
                print(f"✅ Diagnostics: {json.dumps(diagnostics, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ run_diagnostics failed: {e}")
                
            # 13. Get Network Status
            print("\n🟦 13. Testing get_network_status()")
            try:
                network_status = await client.monitoring.get_network_status(debug=True)
                print(f"✅ Network Status: {json.dumps(network_status, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ get_network_status failed: {e}")
                
            # 14. Test External Services
            print("\n🟦 14. Testing test_external_services()")
            try:
                external_test = await client.monitoring.test_external_services(debug=True)
                print(f"✅ External Services Test: {json.dumps(external_test, indent=2, default=str)}")
            except Exception as e:
                print(f"❌ test_external_services failed: {e}")
            
            print("\n" + "=" * 70)
            print("🎉 MONITORING API endpoint testing completed!")
            print("=" * 70)
            
            # Summary
            print("\n📊 Monitoring API Endpoints Tested:")
            endpoints = [
                "get_system_status()",
                "get_health_check()",
                "get_service_status()",
                "get_service_status('bandwidth')",
                "get_database_status()",
                "get_performance_metrics()",
                "get_performance_metrics('bandwidth')",
                "get_error_logs()",
                "get_audit_logs()",
                "get_system_info()",
                "get_uptime()",
                "run_diagnostics()",
                "get_network_status()",
                "test_external_services()"
            ]
            
            for i, endpoint in enumerate(endpoints, 1):
                print(f"  {i:2d}. {endpoint}")
                
            print("\n💡 All endpoints mapped to actual WiFiDog monitoring endpoints")
            print("🔍 Check the HTTP debug output above to see the actual API responses")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())


