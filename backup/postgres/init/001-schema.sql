-- OpsPortal PostgreSQL 16 schema
-- Execute as the opsportal database user (see scripts/setup_database.sh).

BEGIN;

-- ============================================================
-- USERS (authentication)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id            SERIAL PRIMARY KEY,
    email         VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    name          VARCHAR(255) NOT NULL DEFAULT '',
    role          VARCHAR(50)  NOT NULL DEFAULT 'admin',
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);

-- ============================================================
-- DEPARTMENTS
-- ============================================================
CREATE TABLE IF NOT EXISTS departments (
    id          SERIAL PRIMARY KEY,
    code        VARCHAR(50)  NOT NULL UNIQUE,
    name        VARCHAR(255) NOT NULL,
    description TEXT,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_departments_code ON departments (code);

-- ============================================================
-- EMPLOYEES
-- ============================================================
CREATE TABLE IF NOT EXISTS employees (
    id            SERIAL PRIMARY KEY,
    first_name    VARCHAR(120) NOT NULL,
    last_name     VARCHAR(120) NOT NULL,
    email         VARCHAR(255) NOT NULL UNIQUE,
    phone         VARCHAR(50),
    position      VARCHAR(120),
    department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_employees_email      ON employees (email);
CREATE INDEX IF NOT EXISTS idx_employees_department ON employees (department_id);

-- ============================================================
-- ASSETS
-- ============================================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'asset_status') THEN
        CREATE TYPE asset_status AS ENUM ('available', 'assigned', 'in_repair', 'retired');
    END IF;
END$$;

CREATE TABLE IF NOT EXISTS assets (
    id             SERIAL PRIMARY KEY,
    tag            VARCHAR(80)  NOT NULL UNIQUE,
    name           VARCHAR(255) NOT NULL,
    category       VARCHAR(120),
    status         asset_status NOT NULL DEFAULT 'available',
    assigned_to_id INTEGER REFERENCES employees(id) ON DELETE SET NULL,
    purchased_at   DATE,
    created_at     TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at     TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_assets_tag         ON assets (tag);
CREATE INDEX IF NOT EXISTS idx_assets_assigned_to ON assets (assigned_to_id);
CREATE INDEX IF NOT EXISTS idx_assets_status      ON assets (status);

COMMIT;
