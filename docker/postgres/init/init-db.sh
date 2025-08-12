#!/bin/bash
# Database initialization runner script (for manual use)
# This script runs inside the backend container to check database status
# Note: With backup restoration, this is usually not needed as the backup
# contains all the necessary data and schema

echo "🔄 Checking database status..."

# Wait for PostgreSQL to be available
until pg_isready -h postgres -p 5432 -U zeepuser; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

echo "✅ PostgreSQL is ready!"

# Check if we have tables (from backup restoration)
TABLES=$(docker exec zeep-postgres psql -h localhost -U zeepuser -d zeepdb -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')

if [ "$TABLES" -gt 0 ]; then
    echo "✅ Database has $TABLES tables (likely restored from backup)"
    echo "🎉 Database is ready to use!"
else
    echo "⚠️  No tables found. The backup restoration might not have completed yet."
    echo "Check the PostgreSQL container logs: docker logs zeep-postgres"
fi
