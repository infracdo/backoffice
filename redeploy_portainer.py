import os
import httpx
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class PortainerRedeployer:
    def __init__(self):
        self.api_key = os.getenv('PORTAINER_API_KEY')
        self.portainer_url = os.getenv('PORTAINER_URL')
        self.stack_name = os.getenv('PORTAINER_STACK_NAME')
        self.endpoint_id = os.getenv('PORTAINER_ENDPOINT_ID', '1')  # Default to 1
        
        if not all([self.api_key, self.portainer_url, self.stack_name]):
            raise ValueError("Missing required environment variables: PORTAINER_API_KEY, PORTAINER_URL, PORTAINER_STACK_NAME")

    async def get_stack_id(self):
        """Get the stack ID by stack name"""
        url = f"{self.portainer_url}/api/stacks"
        headers = {
            "X-API-Key": self.api_key
        }
        
        async with httpx.AsyncClient(verify=False) as client:  # verify=False equivalent to -k flag
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                stacks = response.json()
                for stack in stacks:
                    if stack.get('Name') == self.stack_name:
                        print(f"Found stack '{self.stack_name}' with ID: {stack.get('Id')}")
                        return stack.get('Id')
                
                print(f"Stack '{self.stack_name}' not found")
                return None
                
            except httpx.RequestError as e:
                print(f"Error getting stack ID: {e}")
                return None
            except httpx.HTTPStatusError as e:
                print(f"HTTP error getting stack ID: {e.response.status_code} - {e.response.text}")
                return None

    async def get_stack_details(self, stack_id):
        """Get full stack details including git config"""
        url = f"{self.portainer_url}/api/stacks/{stack_id}"
        headers = {
            "X-API-Key": self.api_key
        }
        
        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Error getting stack details: {e}")
                return None

    def get_env_variables_from_dotenv(self, existing_stack_env=None):
        """Get environment variables from .env file and merge with existing stack env vars"""
        env_vars = []
        
        # Start with existing stack environment variables if provided
        if existing_stack_env:
            for env_var in existing_stack_env:
                env_vars.append({
                    "name": env_var.get("name"),
                    "value": env_var.get("value")
                })
        
        # List of environment variables to include/override from .env file
        # Automatically include all variables from .env file
        dotenv_vars = [key for key in os.environ.keys() if key not in ['PORTAINER_API_KEY', 'PORTAINER_URL', 'PORTAINER_STACK_NAME', 'PORTAINER_ENDPOINT_ID']]
        
        # Override or add variables from .env file
        for var_name in dotenv_vars:
            var_value = os.getenv(var_name)
            if var_value:  # Only include if the variable has a value
                # Check if variable already exists in stack env vars
                found = False
                for i, env_var in enumerate(env_vars):
                    if env_var["name"] == var_name:
                        env_vars[i]["value"] = var_value  # Override existing value
                        found = True
                        break
                
                if not found:
                    # Add new variable
                    env_vars.append({
                        "name": var_name,
                        "value": var_value
                    })
        
        return env_vars

    async def redeploy_stack(self, stack_id):
        """Redeploy the stack using git"""
        # First get the full stack details to use existing configuration
        stack_details = await self.get_stack_details(stack_id)
        if not stack_details:
            print("Failed to get stack details")
            return False
        
        git_config = stack_details.get('GitConfig', {})
        if not git_config:
            print("Stack is not a git-based stack")
            return False
        
        url = f"{self.portainer_url}/api/stacks/{stack_id}/git/redeploy?endpointId={self.endpoint_id}"
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Use the existing stack's git configuration
        payload = {
            "RepositoryReferenceName": git_config.get('ReferenceName', 'refs/heads/master'),
            "RepositoryAuthentication": bool(git_config.get('Authentication')),
            "RepositoryUsername": git_config.get('Authentication', {}).get('Username', '') if git_config.get('Authentication') else '',
            "RepositoryPassword": git_config.get('Authentication', {}).get('Password', '') if git_config.get('Authentication') else '',
            "Env": self.get_env_variables_from_dotenv(stack_details.get('Env', [])),  # Merge .env and existing stack env vars
            "Prune": True,
            "PullImage": True
        }
        print(f"payload: {payload}")

        async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
            try:
                print(f"Redeploying stack '{self.stack_name}' using git reference: {payload['RepositoryReferenceName']}")
                
                response = await client.put(url, headers=headers, json=payload)
                print(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"Stack '{self.stack_name}' redeployed successfully!")
                    return True
                else:
                    print(f"Response text: {response.text}")
                    response.raise_for_status()
                
            except httpx.HTTPStatusError as e:
                print(f"HTTP error redeploying stack: {e.response.status_code} - {e.response.text}")
                return False
            except Exception as e:
                print(f"Error redeploying stack: {type(e).__name__}: {e}")
                return False

    async def redeploy(self):
        """Main method to get stack ID and redeploy"""
        print(f"Starting redeploy process for stack: {self.stack_name}")
        
        # Get stack ID
        stack_id = await self.get_stack_id()
        if not stack_id:
            return False
        
        # Redeploy stack
        success = await self.redeploy_stack(stack_id)
        return success

async def main():
    try:
        redeployer = PortainerRedeployer()
        success = await redeployer.redeploy()
        
        if success:
            print("Redeploy completed successfully!")
        else:
            print("Redeploy failed!")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())