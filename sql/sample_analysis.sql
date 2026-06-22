-- Sample analysis queries for network operations data

-- Count devices by role
SELECT
    role,
    COUNT(*) AS device_count
FROM devices
GROUP BY role;

-- Count interfaces by operational status
SELECT
    oper_status,
    COUNT(*) AS interface_count
FROM interfaces
GROUP BY oper_status;

-- Count access and trunk ports
SELECT
    port_role,
    COUNT(*) AS port_count
FROM interfaces
GROUP BY port_role;
