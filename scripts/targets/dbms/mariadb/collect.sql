-- MariaDB read-only KCII DBMS evidence summary.
-- Run this in an approved DBA session and copy the text output to the Windows work PC.
-- The output is intentionally limited to booleans, counts, enums, and version-known flags.
-- Do not add password hashes, connection strings, account lists, database lists, or raw privilege rows.

SELECT 'schema_version=kcii-mariadb-paste-v1' AS kcii_evidence;
SELECT 'dbms=mariadb' AS kcii_evidence;
SELECT 'version_patch_status_known=true' AS kcii_evidence;

SELECT CONCAT(
  'risky_default_account_present=',
  IF(EXISTS (
    SELECT 1 FROM mysql.user
    WHERE User = 'root'
  ), 'true', 'false')
) AS kcii_evidence;

SELECT CONCAT(
  'sample_or_unused_account_count=',
  COALESCE((
    SELECT COUNT(*)
    FROM mysql.user
    WHERE User REGEXP '^(test|sample|demo|guest)'
  ), 0)
) AS kcii_evidence;

SELECT CONCAT(
  'excessive_admin_privileges_present=',
  IF((
    SELECT COUNT(*)
    FROM mysql.user
    WHERE Super_priv = 'Y'
  ) > 1, 'true', 'false')
) AS kcii_evidence;

SELECT CONCAT(
  'secure_password_algorithm_configured=',
  IF((
    SELECT COUNT(*)
    FROM mysql.user
    WHERE plugin IN ('mysql_old_password')
  ) = 0, 'true', 'false')
) AS kcii_evidence;

SELECT CONCAT(
  'remote_access_restricted=',
  IF((
    SELECT COUNT(*)
    FROM mysql.user
    WHERE Host IN ('%', '0.0.0.0', '::')
  ) = 0, 'true', 'false')
) AS kcii_evidence;

SELECT CONCAT(
  'public_role_privilege_risk_present=',
  IF(EXISTS (
    SELECT 1
    FROM information_schema.user_privileges
    WHERE grantee LIKE '''PUBLIC''@%'
  ), 'true', 'false')
) AS kcii_evidence;

SELECT CONCAT(
  'grant_option_risk_count=',
  COALESCE((
    SELECT COUNT(*)
    FROM information_schema.user_privileges
    WHERE is_grantable = 'YES'
  ), 0)
) AS kcii_evidence;

SELECT 'resource_limits_enabled=manual_review_required' AS kcii_evidence;
SELECT 'password_policy_configured=manual_review_required' AS kcii_evidence;
SELECT 'login_failure_lockout_configured=manual_review_required' AS kcii_evidence;

SELECT CONCAT(
  'audit_logging_enabled=',
  IF(EXISTS (
    SELECT 1
    FROM information_schema.plugins
    WHERE plugin_name = 'SERVER_AUDIT' AND plugin_status = 'ACTIVE'
  ), 'true', 'false')
) AS kcii_evidence;
