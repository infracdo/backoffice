"""
Monitoring and logging example for ACS ZEEP Client
"""

import asyncio
from datetime import datetime, timedelta
from acs_zeep_client import ACSZeepClient


async def monitoring_example():
    """Example of monitoring operations"""
    
    async with ACSZeepClient() as client:
        print("=== Monitoring Example ===\n")
        
        # System health check
        print("1. Health Check...")
        try:
            health = await client.monitoring.get_health_check()
            print(f"Health status: {health}")
        except Exception as e:
            print(f"Health check failed: {e}")
        
        # System status
        print("\n2. System Status...")
        try:
            status = await client.monitoring.get_system_status()
            print(f"System status: {status}")
        except Exception as e:
            print(f"System status failed: {e}")
        
        # Database status
        print("\n3. Database Status...")
        try:
            db_status = await client.monitoring.get_database_status()
            print(f"Database status: {db_status}")
        except Exception as e:
            print(f"Database status failed: {e}")
        
        # Performance metrics
        print("\n4. Performance Metrics...")
        try:
            metrics = await client.monitoring.get_performance_metrics()
            print(f"Performance metrics: {metrics}")
        except Exception as e:
            print(f"Performance metrics failed: {e}")
        
        # System info
        print("\n5. System Information...")
        try:
            system_info = await client.monitoring.get_system_info()
            print(f"System info: {system_info}")
        except Exception as e:
            print(f"System info failed: {e}")
        
        print("\n=== Monitoring Example Complete ===")


async def logging_example():
    """Example of logging operations"""
    
    async with ACSZeepClient() as client:
        print("\n=== Logging Example ===\n")
        
        # Get recent CPE response logs
        print("1. CPE Response Logs...")
        try:
            cpe_logs = await client.logs.get_cpe_response_logs(page_size=5)
            print(f"Found {len(cpe_logs)} CPE response logs")
            
            for log in cpe_logs[:3]:
                print(f"  - {log.timestamp}: {log.request_type} -> {log.status_code}")
        except Exception as e:
            print(f"CPE logs failed: {e}")
        
        # Get WebCLI response logs
        print("\n2. WebCLI Response Logs...")
        try:
            webcli_logs = await client.logs.get_webcli_response_logs(page_size=5)
            print(f"Found {len(webcli_logs)} WebCLI response logs")
            
            for log in webcli_logs[:3]:
                print(f"  - {log.timestamp}: {log.command}")
        except Exception as e:
            print(f"WebCLI logs failed: {e}")
        
        # Get HTTP request logs
        print("\n3. HTTP Request Logs...")
        try:
            http_logs = await client.logs.get_http_request_logs(page_size=5)
            print(f"Found {len(http_logs)} HTTP request logs")
            
            for log in http_logs[:3]:
                print(f"  - {log.timestamp}: {log.method} {log.url} -> {log.response_status}")
        except Exception as e:
            print(f"HTTP logs failed: {e}")
        
        # Search logs
        print("\n4. Log Search...")
        try:
            search_results = await client.logs.search_logs(
                query="error",
                page_size=5
            )
            print(f"Found {len(search_results)} logs matching 'error'")
        except Exception as e:
            print(f"Log search failed: {e}")
        
        # Get log statistics
        print("\n5. Log Statistics...")
        try:
            stats = await client.logs.get_log_statistics()
            print(f"Log statistics: {stats}")
        except Exception as e:
            print(f"Log statistics failed: {e}")
        
        print("\n=== Logging Example Complete ===")


async def zeep_monitoring_example():
    """Example of ZEEP monitoring operations"""
    
    async with ACSZeepClient() as client:
        print("\n=== ZEEP Monitoring Example ===\n")
        
        # ZEEP status
        print("1. ZEEP Status...")
        try:
            zeep_status = await client.zeep.get_status()
            print(f"ZEEP status: {zeep_status}")
        except Exception as e:
            print(f"ZEEP status failed: {e}")
        
        # ZEEP services
        print("\n2. ZEEP Services...")
        try:
            services = await client.zeep.get_services()
            print(f"Found {len(services)} ZEEP services")
            
            for service in services[:3]:
                print(f"  - {service.get('name', 'Unknown')}: {service.get('status', 'Unknown')}")
        except Exception as e:
            print(f"ZEEP services failed: {e}")
        
        # ZEEP monitoring data
        print("\n3. ZEEP Monitoring Data...")
        try:
            monitoring_data = await client.zeep.get_monitoring_data()
            print(f"Found {len(monitoring_data)} monitoring records")
        except Exception as e:
            print(f"ZEEP monitoring data failed: {e}")
        
        # ZEEP configuration
        print("\n4. ZEEP Configuration...")
        try:
            config = await client.zeep.get_configuration()
            print(f"ZEEP config keys: {list(config.keys()) if isinstance(config, dict) else 'Not a dict'}")
        except Exception as e:
            print(f"ZEEP configuration failed: {e}")
        
        # ZEEP metrics
        print("\n5. ZEEP Metrics...")
        try:
            metrics = await client.zeep.get_metrics()
            print(f"ZEEP metrics: {metrics}")
        except Exception as e:
            print(f"ZEEP metrics failed: {e}")
        
        print("\n=== ZEEP Monitoring Example Complete ===")


if __name__ == "__main__":
    asyncio.run(monitoring_example())
    asyncio.run(logging_example())
    asyncio.run(zeep_monitoring_example())
