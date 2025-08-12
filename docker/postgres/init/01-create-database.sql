-- Database initialization script for Zeep Backend
-- This script prepares the database for backup restoration

-- Create extensions if needed (these might be in your backup, but it's safe to create them first)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Set timezone
SET timezone = 'UTC';

-- Grant permissions to the user
GRANT ALL PRIVILEGES ON DATABASE zeepdb TO zeepuser;
GRANT ALL ON SCHEMA public TO zeepuser;

-- These will be granted after tables are restored
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO zeepuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO zeepuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO zeepuser;

-- Prepare for backup restoration
-- The backup will be restored by the 99-restore-backup.sh script
