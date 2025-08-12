#!/bin/bash
# Database verification script
# This script checks if the backup restoration was successful

echo "🔍 Verifying database restoration..."

# Check if PostgreSQL is running
if ! pg_isready -h localhost -p 5432 -U $POSTGRES_USER -d $POSTGRES_DB; then
    echo "❌ PostgreSQL is not ready"
    exit 1
fi

echo "✅ PostgreSQL is running"

# Count tables
TABLE_COUNT=$(psql -h localhost -p 5432 -U $POSTGRES_USER -d $POSTGRES_DB -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';" | tr -d ' ')

echo "📊 Found $TABLE_COUNT tables in the database"

if [ "$TABLE_COUNT" -gt 0 ]; then
    echo "✅ Database restoration verification successful!"
    
    # List all tables
    echo "📋 Tables in the database:"
    psql -h localhost -p 5432 -U $POSTGRES_USER -d $POSTGRES_DB -c "\dt"
    
    # Check for common tables (adjust these based on your actual table names)
    echo "🔎 Checking for common tables..."
    
    COMMON_TABLES=("Users" "Transactions" "UserRoles" "Tiers")
    for table in "${COMMON_TABLES[@]}"; do
        EXISTS=$(psql -h localhost -p 5432 -U $POSTGRES_USER -d $POSTGRES_DB -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = '$table');" | tr -d ' ')
        if [ "$EXISTS" = "t" ]; then
            COUNT=$(psql -h localhost -p 5432 -U $POSTGRES_USER -d $POSTGRES_DB -t -c "SELECT COUNT(*) FROM \"$table\";" | tr -d ' ')
            echo "✅ Table '$table' exists with $COUNT records"
        else
            echo "⚠️  Table '$table' not found (this might be expected if your schema is different)"
        fi
    done
    
else
    echo "❌ No tables found in the database - restoration may have failed"
    exit 1
fi

echo "🎉 Database verification completed!"
