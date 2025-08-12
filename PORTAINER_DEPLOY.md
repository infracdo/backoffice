# Portainer Deployment Guide for Zeep Backend

This guide helps you deploy the Zeep Backend application in Portainer using Git.

## Prerequisites

1. **Portainer Setup**: Ensure Portainer is running and you have access to it
2. **Git Repository**: Your code should be in a Git repository (GitHub, GitLab, etc.)
3. **Network**: The `portainer_default` network should exist in your Portainer environment
4. **Database Backup**: Ensure `zeep_backend_staging_bak.backup` is in your repository root

## Deployment Steps

### 1. Create the Stack in Portainer

1. Log into your Portainer instance
2. Navigate to **Stacks** → **Add Stack**
3. Choose **Git Repository** as the build method

### 2. Git Configuration

- **Repository URL**: `https://github.com/yourusername/zeep-backend.git` (replace with your repo)
- **Reference**: `refs/heads/main` (or your default branch)
- **Compose path**: `docker-compose.yml`

### 3. Environment Variables

Since the `.env` file contains sensitive credentials and shouldn't be in the Git repository, add these environment variables directly in Portainer:

**Required Variables:**
```
SECRET=E1M4A2R2viq07GmeAZT7EdzdtqgGom5C
JWT_ALGO=HS256
MANDRILL_API=UE7P3rxrVOSJCmlR21t9LQ
MANDRILL_NAME=Zeep Team
MANDRILL_EMAIL=no-reply@thousandminds.com
MACRODROID_URL=https://trigger.macrodroid.com/f9cc1189-e67b-423e-a97a-91505bfbc0ca/smssender
ROUTER_URL=http://rport.thousandminds.com:21828/api/acs/add
IBM_COS_API_KEY=K4AY20CmkYiPWgRO71HsMKiDTCIcjvmhomrPrNDSpLRI
IBM_COS_SERVICE_INSTANCE_ID=crn:v1:bluemix:public:cloud-object-storage:global:a/166940ec986c4cd58d2ec271ca75ba8e:c9732616-9fa5-4f6f-881a-b3bd1610b2c0::
IBM_COS_BUSCKET_NAME=zeep
IBM_COS_REGION=jp-tok
PAYCONNECT_BASEURL=https://sbx-paygateway-api.payconnect.io
PAYCONNECT_AUTH=Basic Y1h2eXhHY3ZUaVJnQ255VjFRNFdQWGg2c1NwMExrb3Y3SHpjVU80aXNWeGQ0bHVHY2tGNGc2YWFiYUR3bnJBUTo=
```

**Note**: Database connection variables are automatically configured in the Docker Compose file to use the containerized PostgreSQL instance.

### 4. Deploy the Stack

1. Click **Deploy the stack**
2. Wait for both containers to start (postgres should be healthy before backend starts)
3. Check the logs to ensure everything is working correctly

## Post-Deployment Steps

### 1. Verify Database Restoration

Check that your backup was restored successfully:

```bash
# Check container logs to see restoration progress
docker logs zeep-postgres

# Connect to database and verify tables exist
docker exec -it zeep-postgres psql -U zeepuser -d zeepdb -c "\dt"
```

### 2. Access the Application

- **Backend API**: `http://your-server:5050`
- **PostgreSQL**: `your-server:5432` (if you need direct access)

### 3. Health Check

Visit `http://your-server:5050/docs` to see the FastAPI documentation and verify the API is working with your restored data.

## Configuration Notes

### Database Configuration
The Docker Compose file is configured to:
- Use PostgreSQL 15 Alpine for smaller size
- Store data in a persistent volume (`postgres_data`)
- Wait for PostgreSQL to be healthy before starting the backend
- Use the external `portainer_default` network

### Security Considerations
- Change default database passwords in production
- Use strong secrets for JWT and other sensitive data
- Consider using Docker secrets for sensitive environment variables
- Enable SSL/TLS for production deployments

### Updating the Application

To update your application:
1. Push changes to your Git repository
2. In Portainer, go to your stack
3. Click **Editor** tab and then **Update the stack**
4. Or use the **Git** tab to pull latest changes

### Scaling

The current setup is designed for single-instance deployment. For scaling:
- Consider using a managed PostgreSQL service
- Add load balancing for multiple backend instances
- Implement session storage (Redis) if needed

## Troubleshooting

### Common Issues

1. **Network not found**: Ensure `portainer_default` network exists
2. **Database connection failed**: Check if PostgreSQL container is healthy
3. **Environment variables not loaded**: Verify `.env` file or Portainer env vars
4. **Port conflicts**: Change ports in docker-compose.yml if needed

### Checking Logs

```bash
# Backend logs
docker logs zeep-backend

# Database logs  
docker logs zeep-postgres

# Follow logs in real-time
docker logs -f zeep-backend
```

## Backup and Recovery

### Database Backup

```bash
# Create backup
docker exec zeep-postgres pg_dump -U zeepuser zeepdb > backup.sql

# Restore backup
docker exec -i zeep-postgres psql -U zeepuser zeepdb < backup.sql
```

### Volume Backup

The database data is stored in the `postgres_data` volume. Make sure to back up this volume regularly in your production environment.
