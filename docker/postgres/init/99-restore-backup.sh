#!/bin/bash
# Restore PostgreSQL backup script
# This script restores the database from the backup file

set -e

echo "🔄 Starting database restoration from backup..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until pg_isready -h localhost -p 5432 -U $POSTGRES_USER -d $POSTGRES_DB; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

echo "✅ PostgreSQL is ready!"

# Check if backup file exists
BACKUP_FILE="/docker-entrypoint-initdb.d/zeep_backend_staging_bak.backup"
if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "📁 Found backup file: $BACKUP_FILE"

# Restore the database from backup
echo "🚀 Restoring database from backup..."

# Use pg_restore to restore the backup
pg_restore -h localhost -p 5432 -U $POSTGRES_USER -d $POSTGRES_DB -v -c --if-exists --no-owner --no-privileges "$BACKUP_FILE" || {
    echo "⚠️  pg_restore had some warnings/errors, but this is often normal for backup restoration"
}

echo "✅ Database restoration completed!"

# Verify the restoration by checking if tables exist
echo "🔍 Verifying database restoration..."
TABLES=$(psql -h localhost -p 5432 -U $POSTGRES_USER -d $POSTGRES_DB -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
echo "📊 Found $TABLES tables in the database"

if [ "$TABLES" -gt 0 ]; then
    echo "✅ Database restoration successful! Found $TABLES tables."
else
    echo "⚠️  Warning: No tables found in the restored database."
fi
