-- OpsPortal seed data
-- Prefer running `python -m app.seed` from the backend venv so the admin password
-- gets hashed with bcrypt. This SQL seed provides departments/employees/assets
-- only (no admin user) and is safe to re-run.

BEGIN;

INSERT INTO departments (code, name, description) VALUES
  ('ENG', 'Engineering',       'Software engineering department'),
  ('HR',  'Human Resources',   'People operations'),
  ('FIN', 'Finance',           'Finance and accounting'),
  ('OPS', 'Operations',        'Business operations')
ON CONFLICT (code) DO NOTHING;

INSERT INTO employees (first_name, last_name, email, phone, position, department_id) VALUES
  ('Alice', 'Anderson', 'alice@opsportal.local', '+1-555-1001', 'Senior Engineer', (SELECT id FROM departments WHERE code='ENG')),
  ('Bob',   'Brown',    'bob@opsportal.local',   '+1-555-1002', 'DevOps Engineer', (SELECT id FROM departments WHERE code='ENG')),
  ('Carol', 'Clark',    'carol@opsportal.local', '+1-555-1003', 'HR Manager',      (SELECT id FROM departments WHERE code='HR')),
  ('David', 'Davis',    'david@opsportal.local', '+1-555-1004', 'Accountant',      (SELECT id FROM departments WHERE code='FIN')),
  ('Eve',   'Evans',    'eve@opsportal.local',   '+1-555-1005', 'Operations Lead', (SELECT id FROM departments WHERE code='OPS'))
ON CONFLICT (email) DO NOTHING;

INSERT INTO assets (tag, name, category, status, assigned_to_id, purchased_at) VALUES
  ('LT-0001', 'MacBook Pro 16"',       'Laptop',     'assigned',  (SELECT id FROM employees WHERE email='alice@opsportal.local'), DATE '2024-03-15'),
  ('LT-0002', 'Dell XPS 15',           'Laptop',     'assigned',  (SELECT id FROM employees WHERE email='bob@opsportal.local'),   DATE '2024-04-20'),
  ('MN-0001', 'LG UltraFine 27"',      'Monitor',    'assigned',  (SELECT id FROM employees WHERE email='alice@opsportal.local'), DATE '2024-03-15'),
  ('KB-0001', 'Logitech MX Keys',      'Peripheral', 'available', NULL,                                                            DATE '2024-01-10'),
  ('PH-0001', 'iPhone 15',             'Phone',      'assigned',  (SELECT id FROM employees WHERE email='carol@opsportal.local'), DATE '2024-06-01'),
  ('SV-0001', 'Dell PowerEdge R750',   'Server',     'in_repair', NULL,                                                            DATE '2023-11-12')
ON CONFLICT (tag) DO NOTHING;

COMMIT;
