DROP VIEW IF EXISTS device_count_by_role;
DROP VIEW IF EXISTS interface_status_summary;
DROP VIEW IF EXISTS port_role_summary;
DROP VIEW IF EXISTS topology_link_status_summary;
DROP VIEW IF EXISTS documentation_coverage;

CREATE VIEW device_count_by_role AS
SELECT
    role,
    COUNT(*) AS device_count
FROM devices
GROUP BY role;

CREATE VIEW interface_status_summary AS
SELECT
    admin_status,
    oper_status,
    COUNT(*) AS interface_count
FROM interfaces
GROUP BY admin_status, oper_status;

CREATE VIEW port_role_summary AS
SELECT
    port_role,
    COUNT(*) AS port_count
FROM interfaces
GROUP BY port_role;

CREATE VIEW topology_link_status_summary AS
SELECT
    link_role,
    link_status,
    COUNT(*) AS link_count
FROM topology_links
GROUP BY link_role, link_status;

CREATE VIEW documentation_coverage AS
SELECT
    COUNT(*) AS interface_count,
    SUM(CASE WHEN description_present = 1 THEN 1 ELSE 0 END) AS documented_interfaces,
    ROUND(
        100.0 * SUM(CASE WHEN description_present = 1 THEN 1 ELSE 0 END)
        / NULLIF(COUNT(*), 0),
        1
    ) AS description_coverage_pct
FROM interfaces;
