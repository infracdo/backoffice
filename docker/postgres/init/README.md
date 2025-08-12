# Database Setup Guide

This directory contains the database initialization scripts for the Zeep Backend application.

## Files Overview

- `01-create-database.sql`: Creates the database, extensions, and sets up permissions
- `99-restore-backup.sh`: Shell script that restores the database from the backup file
- `02-sample-data.sql.bak`: Sample data (SQL version - disabled, use backup instead)
- `03-init-tables.py.bak`: Python initialization script (disabled, use backup instead)
- `init-db.sh`: Manual initialization script (not used with backup restoration)

## Automatic Setup with Backup Restoration

When you run `docker-compose up`, the following happens automatically:

1. PostgreSQL container starts and runs the SQL scripts in alphabetical order:
   - `01-create-database.sql` sets up extensions and permissions
   - `99-restore-backup.sh` restores your `zeep_backend_staging_bak.backup` file
2. The backend application starts and connects to the restored database
3. All your existing data from the backup is now available

## Backup File

The system expects your backup file at:
- **Location**: `./zeep_backend_staging_bak.backup` (root of project)
- **Format**: PostgreSQL custom format backup (created with `pg_dump -Fc`)
- **Restoration**: Automatic on first container startup

## Manual Database Operations

### Re-restore the backup (if needed)
If you need to manually restore the backup again:

```bash
# Copy the backup into the running container
docker cp ./zeep_backend_staging_bak.backup zeep-postgres:/tmp/backup.backup

# Restore the backup
docker exec -it zeep-postgres pg_restore -h localhost -U zeepuser -d zeepdb -c --if-exists -v /tmp/backup.backup
```

### Create a new backup
To create a backup of your current database:

```bash
# Create a new backup
docker exec -it zeep-postgres pg_dump -h localhost -U zeepuser -d zeepdb -Fc -f /tmp/new_backup.backup

# Copy the backup out of the container
docker cp zeep-postgres:/tmp/new_backup.backup ./new_backup.backup
```

## Database Connection Details

- **Host**: `postgres` (container name)
- **Port**: `5432`
- **Database**: `zeepdb`
- **Username**: `zeepuser`
- **Password**: `zeeppassword123`

## Database Content

The database will be restored from your `zeep_backend_staging_bak.backup` file, which contains:
- All your existing tables and schema
- Real data from your staging environment
- User accounts, transactions, and other production-like data

**Note**: The backup restoration replaces any sample data scripts. Your actual data from the backup will be used instead.

## Production Considerations

1. **Change default passwords**: Update the PostgreSQL and admin user passwords
2. **Environment variables**: Copy `.env.example` to `.env` and update all values
3. **Database backup**: Set up regular backups for your PostgreSQL data
4. **Security**: Use strong passwords and consider using secrets management
5. **Monitoring**: Add database monitoring and health checks

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL container is healthy: `docker ps`
- Check logs: `docker logs zeep-postgres`
- Verify environment variables in `.env` file

### Table Creation Issues
- Check backend logs: `docker logs zeep-backend`
- Ensure all model imports are working in `03-init-tables.py`
- Verify SQLAlchemy models are properly defined

### Data Persistence
- Database data is stored in the `postgres_data` Docker volume
- To reset the database: `docker-compose down -v` (⚠️ This will delete all data!)
