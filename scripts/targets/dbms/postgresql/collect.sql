-- PostgreSQL read-only KCII DBMS evidence summary.
-- Run this in an approved DBA session and copy the text output to the Windows work PC.
-- The output is intentionally limited to booleans, counts, enums, and version-known flags.
-- Do not add password hashes, connection strings, account lists, database lists, or raw privilege rows.

\pset tuples_only on
\pset format unaligned

SELECT 'schema_version=kcii-postgresql-paste-v1';
SELECT 'dbms=postgresql';
SELECT 'version_patch_status_known=true';

SELECT 'risky_default_account_present=' ||
  CASE WHEN EXISTS (
    SELECT 1 FROM pg_catalog.pg_roles
    WHERE rolname = 'postgres' AND rolcanlogin
  ) THEN 'true' ELSE 'false' END;

SELECT 'sample_or_unused_account_count=' ||
  COALESCE((
    SELECT count(*)::text
    FROM pg_catalog.pg_roles
    WHERE rolcanlogin AND rolname ~* '^(test|sample|demo|guest)'
  ), '0');

SELECT 'excessive_admin_privileges_present=' ||
  CASE WHEN (
    SELECT count(*) FROM pg_catalog.pg_roles WHERE rolsuper AND rolcanlogin
  ) > 1 THEN 'true' ELSE 'false' END;

SELECT 'secure_password_algorithm_configured=' ||
  CASE WHEN COALESCE(current_setting('password_encryption', true), '') = 'scram-sha-256'
  THEN 'true' ELSE 'false' END;

SELECT 'remote_access_restricted=' ||
  CASE WHEN COALESCE(current_setting('listen_addresses', true), '') IN ('*', '0.0.0.0', '::')
  THEN 'false' ELSE 'true' END;

SELECT 'public_role_privilege_risk_present=' ||
  CASE WHEN EXISTS (
    SELECT 1
    FROM information_schema.role_table_grants
    WHERE grantee = 'PUBLIC'
  ) THEN 'true' ELSE 'false' END;

SELECT 'grant_option_risk_count=' ||
  COALESCE((
    SELECT count(*)::text
    FROM information_schema.role_table_grants
    WHERE is_grantable = 'YES'
  ), '0');

SELECT 'resource_limits_enabled=manual_review_required';
SELECT 'password_policy_configured=manual_review_required';
SELECT 'login_failure_lockout_configured=manual_review_required';
SELECT 'audit_logging_enabled=' ||
  CASE WHEN COALESCE(current_setting('logging_collector', true), '') = 'on'
  THEN 'true' ELSE 'false' END;
