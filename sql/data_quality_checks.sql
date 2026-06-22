-- Network Operations Data Lab
-- Data-quality checks for public-safe sample network operations data
--
-- Expected tables:
-- - devices
-- - interfaces
--
-- Expected devices columns:
-- device_id, device_name, device_type, vendor, model, role, location
--
-- Expected interfaces columns:
-- device_name, interface_name, interface_type, admin_status, oper_status, vlan, port_role, description
--
-- These queries are intentionally simple and reporting-oriented.
-- They show which checks should run before SQL analysis or BI reporting.

-- 1. Row counts
SELECT
    'devices' AS table_name,
    COUNT(*) AS row_count
FROM devices
UNION ALL
SELECT
    'interfaces' AS table_name,
    COUNT(*) AS row_count
FROM interfaces;

-- 2. Missing device identifiers
SELECT
    *
FROM devices
WHERE device_id IS NULL
   OR TRIM(CAST(device_id AS TEXT)) = '';

-- 3. Duplicate device IDs
SELECT
    device_id,
    COUNT(*) AS duplicate_count
FROM devices
GROUP BY device_id
HAVING COUNT(*) > 1;

-- 4. Missing device names
SELECT
    *
FROM devices
WHERE device_name IS NULL
   OR TRIM(device_name) = '';

-- 5. Duplicate device names
SELECT
    device_name,
    COUNT(*) AS duplicate_count
FROM devices
GROUP BY device_name
HAVING COUNT(*) > 1;

-- 6. Missing interface device references
SELECT
    *
FROM interfaces
WHERE device_name IS NULL
   OR TRIM(device_name) = '';

-- 7. Missing interface names
SELECT
    *
FROM interfaces
WHERE interface_name IS NULL
   OR TRIM(interface_name) = '';

-- 8. Duplicate interface rows per device
SELECT
    device_name,
    interface_name,
    COUNT(*) AS duplicate_count
FROM interfaces
GROUP BY
    device_name,
    interface_name
HAVING COUNT(*) > 1;

-- 9. Interfaces referencing unknown devices
SELECT
    i.device_name,
    i.interface_name
FROM interfaces AS i
LEFT JOIN devices AS d
    ON i.device_name = d.device_name
WHERE d.device_name IS NULL;

-- 10. Missing administrative or operational status
SELECT
    device_name,
    interface_name,
    admin_status,
    oper_status
FROM interfaces
WHERE admin_status IS NULL
   OR TRIM(admin_status) = ''
   OR oper_status IS NULL
   OR TRIM(oper_status) = '';

-- 11. Interfaces administratively up but operationally down
SELECT
    device_name,
    interface_name,
    admin_status,
    oper_status,
    port_role,
    description
FROM interfaces
WHERE LOWER(TRIM(admin_status)) = 'up'
  AND LOWER(TRIM(oper_status)) IN ('down', 'notconnect', 'not connected');

-- 12. Access ports without VLAN documentation
SELECT
    device_name,
    interface_name,
    vlan,
    port_role,
    description
FROM interfaces
WHERE LOWER(TRIM(port_role)) = 'access'
  AND (
      vlan IS NULL
      OR TRIM(vlan) = ''
  );

-- 13. Trunk ports without trunk documentation in the VLAN field
SELECT
    device_name,
    interface_name,
    vlan,
    port_role,
    description
FROM interfaces
WHERE LOWER(TRIM(port_role)) = 'trunk'
  AND LOWER(TRIM(vlan)) <> 'trunk';

-- 14. Missing interface descriptions
SELECT
    device_name,
    interface_name,
    description
FROM interfaces
WHERE description IS NULL
   OR TRIM(description) = '';

-- 15. Device count by role
SELECT
    role,
    COUNT(*) AS device_count
FROM devices
GROUP BY role
ORDER BY device_count DESC;

-- 16. Interface status summary
SELECT
    admin_status,
    oper_status,
    COUNT(*) AS interface_count
FROM interfaces
GROUP BY
    admin_status,
    oper_status
ORDER BY interface_count DESC;

-- 17. Port role summary
SELECT
    port_role,
    COUNT(*) AS port_count
FROM interfaces
GROUP BY port_role
ORDER BY port_count DESC;
