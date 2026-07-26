DROP VIEW IF EXISTS data_quality_results;

CREATE VIEW data_quality_results AS
WITH raw_checks AS (
SELECT 1 AS check_no, 'Row count: devices' AS check_name, 'summary' AS category,
       (SELECT COUNT(*) FROM devices) AS affected_rows,
       'Total number of rows in devices.csv.' AS description
UNION ALL
SELECT 1, 'Row count: interfaces', 'summary',
       (SELECT COUNT(*) FROM interfaces),
       'Total number of rows in interfaces.csv.'
UNION ALL
SELECT 2, 'Missing device identifiers', 'data_quality',
       (SELECT COUNT(*) FROM devices WHERE TRIM(device_id) = ''),
       'Devices with a missing or empty device_id.'
UNION ALL
SELECT 3, 'Duplicate device IDs', 'data_quality',
       (SELECT COALESCE(SUM(row_count), 0) FROM (
            SELECT COUNT(*) AS row_count FROM devices
            GROUP BY device_id HAVING COUNT(*) > 1
        )),
       'Rows sharing a non-empty device_id with another row.'
UNION ALL
SELECT 4, 'Missing device names', 'data_quality',
       (SELECT COUNT(*) FROM devices WHERE TRIM(device_name) = ''),
       'Devices with a missing or empty device_name.'
UNION ALL
SELECT 5, 'Duplicate device names', 'data_quality',
       (SELECT COALESCE(SUM(row_count), 0) FROM (
            SELECT COUNT(*) AS row_count FROM devices
            GROUP BY device_name HAVING COUNT(*) > 1
        )),
       'Rows sharing a non-empty device_name with another row.'
UNION ALL
SELECT 6, 'Missing interface device references', 'data_quality',
       (SELECT COUNT(*) FROM interfaces WHERE TRIM(device_name) = ''),
       'Interfaces with a missing or empty device_name reference.'
UNION ALL
SELECT 7, 'Missing interface names', 'data_quality',
       (SELECT COUNT(*) FROM interfaces WHERE TRIM(interface_name) = ''),
       'Interfaces with a missing or empty interface_name.'
UNION ALL
SELECT 8, 'Duplicate interface rows per device', 'data_quality',
       (SELECT COALESCE(SUM(row_count), 0) FROM (
            SELECT COUNT(*) AS row_count FROM interfaces
            GROUP BY device_id, interface_name HAVING COUNT(*) > 1
        )),
       'Rows sharing the same device_id and interface_name with another row.'
UNION ALL
SELECT 9, 'Interfaces referencing unknown device names', 'data_quality',
       (SELECT COUNT(*) FROM interfaces AS i
        LEFT JOIN devices AS d ON i.device_name = d.device_name
        WHERE d.device_id IS NULL),
       'Interfaces whose device_name does not exist in devices.'
UNION ALL
SELECT 10, 'Missing administrative or operational status', 'data_quality',
       (SELECT COUNT(*) FROM interfaces
        WHERE TRIM(admin_status) = '' OR TRIM(oper_status) = ''),
       'Interfaces with a missing admin_status or oper_status.'
UNION ALL
SELECT 11, 'Admin up but operationally down', 'operational_condition',
       (SELECT COUNT(*) FROM interfaces
        WHERE admin_status = 'up' AND oper_status IN ('down', 'notconnect')),
       'Interfaces admin up while operationally down or not connected.'
UNION ALL
SELECT 12, 'Access-family ports without VLAN documentation', 'data_quality',
       (SELECT COUNT(*) FROM interfaces
        WHERE port_role IN ('access', 'client_access', 'lab_access')
          AND TRIM(vlan) = ''),
       'Access-family ports with a missing VLAN value.'
UNION ALL
SELECT 13, 'Trunk ports without trunk documentation', 'data_quality',
       (SELECT COUNT(*) FROM interfaces
        WHERE port_role = 'trunk' AND LOWER(TRIM(vlan)) <> 'trunk'),
       'Trunk ports whose vlan field is not set to trunk.'
UNION ALL
SELECT 14, 'Missing interface descriptions', 'data_quality',
       (SELECT COUNT(*) FROM interfaces WHERE TRIM(description) = ''),
       'Interfaces with a missing or empty description.'
UNION ALL
SELECT 15, 'Device count by role: distinct roles', 'summary',
       (SELECT COUNT(DISTINCT role) FROM devices),
       'Number of distinct device roles present.'
UNION ALL
SELECT 16, 'Interface status summary: distinct combinations', 'summary',
       (SELECT COUNT(*) FROM (
            SELECT admin_status, oper_status FROM interfaces
            GROUP BY admin_status, oper_status
        )),
       'Number of distinct administrative and operational status combinations.'
UNION ALL
SELECT 17, 'Port role summary: distinct roles', 'summary',
       (SELECT COUNT(DISTINCT port_role) FROM interfaces),
       'Number of distinct port roles present.'
UNION ALL
SELECT 18, 'Row count: topology_links', 'summary',
       (SELECT COUNT(*) FROM topology_links),
       'Total number of rows in topology_links.csv.'
UNION ALL
SELECT 19, 'Interfaces with unknown device_id', 'data_quality',
       (SELECT COUNT(*) FROM interfaces AS i
        LEFT JOIN devices AS d ON i.device_id = d.device_id
        WHERE d.device_id IS NULL),
       'Interfaces whose device_id does not exist in devices.'
UNION ALL
SELECT 20, 'Duplicate interface IDs', 'data_quality',
       (SELECT COALESCE(SUM(row_count), 0) FROM (
            SELECT COUNT(*) AS row_count FROM interfaces
            GROUP BY interface_id HAVING COUNT(*) > 1
        )),
       'Rows sharing a non-empty interface_id with another row.'
UNION ALL
SELECT 21, 'Duplicate device_id and interface_name pairs', 'data_quality',
       (SELECT COALESCE(SUM(row_count), 0) FROM (
            SELECT COUNT(*) AS row_count FROM interfaces
            GROUP BY device_id, interface_name HAVING COUNT(*) > 1
        )),
       'Rows sharing the same device_id and interface_name with another row.'
UNION ALL
SELECT 22, 'Interfaces with unexpected port_role', 'data_quality',
       (SELECT COUNT(*) FROM interfaces
        WHERE port_role NOT IN (
            'access', 'trunk', 'uplink', 'client_access',
            'lab_access', 'bridge_uplink'
        )),
       'Interfaces whose port_role is outside the controlled vocabulary.'
UNION ALL
SELECT 23, 'Invalid description_present values', 'data_quality',
       (SELECT COUNT(*) FROM interfaces WHERE description_present NOT IN (0, 1)),
       'Interfaces with description_present outside the Boolean domain.'
UNION ALL
SELECT 24, 'Active interfaces without description', 'data_quality',
       (SELECT COUNT(*) FROM interfaces
        WHERE admin_status = 'up' AND oper_status = 'up'
          AND TRIM(description) = ''),
       'Operationally active interfaces without a description.'
UNION ALL
SELECT 25, 'Uplink interfaces with unexpected downstream cardinality', 'data_quality',
       (SELECT COUNT(*) FROM interfaces
        WHERE port_role = 'uplink'
          AND expected_downstream_devices <> 'multiple'),
       'Uplink interfaces not documented with multiple downstream devices.'
UNION ALL
SELECT 26, 'Client access interfaces with unexpected downstream cardinality', 'data_quality',
       (SELECT COUNT(*) FROM interfaces
        WHERE port_role = 'client_access'
          AND expected_downstream_devices <> 'single'),
       'Client access interfaces not documented with one downstream device.'
UNION ALL
SELECT 27, 'Topology links with unknown source_device_id', 'data_quality',
       (SELECT COUNT(*) FROM topology_links AS l
        LEFT JOIN devices AS d ON l.source_device_id = d.device_id
        WHERE d.device_id IS NULL),
       'Links whose source_device_id does not exist in devices.'
UNION ALL
SELECT 28, 'Topology links with unknown source interface', 'data_quality',
       (SELECT COUNT(*) FROM topology_links AS l
        LEFT JOIN interfaces AS i
          ON l.source_device_id = i.device_id
         AND l.source_interface_id = i.interface_id
        WHERE i.interface_id IS NULL),
       'Links whose source device and interface pair does not exist.'
UNION ALL
SELECT 29, 'Topology links with unknown target_device_id', 'data_quality',
       (SELECT COUNT(*) FROM topology_links AS l
        LEFT JOIN devices AS d ON l.target_device_id = d.device_id
        WHERE d.device_id IS NULL),
       'Links whose target_device_id does not exist in devices.'
UNION ALL
SELECT 30, 'Active links with source interface not operationally up', 'operational_condition',
       (SELECT COUNT(*) FROM topology_links AS l
        LEFT JOIN interfaces AS i
          ON l.source_device_id = i.device_id
         AND l.source_interface_id = i.interface_id
        WHERE l.link_status = 'active'
          AND COALESCE(i.oper_status, 'missing') <> 'up'),
       'Active links whose source interface is missing or not operationally up.'
UNION ALL
SELECT 31, 'Links where link_role does not match source port_role', 'data_quality',
       (SELECT COUNT(*) FROM topology_links AS l
        JOIN interfaces AS i
          ON l.source_device_id = i.device_id
         AND l.source_interface_id = i.interface_id
        WHERE l.link_role <> i.port_role),
       'Links whose role differs from the source interface port role.'
UNION ALL
SELECT 32, 'Devices with missing required attributes', 'data_quality',
       (SELECT COUNT(*) FROM devices
        WHERE TRIM(device_type) = '' OR TRIM(vendor) = ''
           OR TRIM(model) = '' OR TRIM(role) = '' OR TRIM(location) = ''),
       'Devices missing a required descriptive attribute.'
UNION ALL
SELECT 33, 'Invalid device active-state values', 'data_quality',
       (SELECT COUNT(*) FROM devices WHERE is_active NOT IN (0, 1)),
       'Devices with is_active outside the Boolean domain.'
UNION ALL
SELECT 34, 'Devices with unexpected scope values', 'data_quality',
       (SELECT COUNT(*) FROM devices
        WHERE location_scope NOT IN ('home_lab', 'external_lab')
           OR management_scope NOT IN ('managed', 'endpoint', 'unmanaged')),
       'Devices with location_scope or management_scope outside the controlled vocabulary.'
UNION ALL
SELECT 35, 'Missing interface identifiers', 'data_quality',
       (SELECT COUNT(*) FROM interfaces WHERE TRIM(interface_id) = ''),
       'Interfaces with a missing interface_id.'
UNION ALL
SELECT 36, 'Interface device names inconsistent with device IDs', 'data_quality',
       (SELECT COUNT(*) FROM interfaces AS i
        JOIN devices AS d ON i.device_id = d.device_id
        WHERE i.device_name <> d.device_name),
       'Interfaces whose device_name does not match the referenced device_id.'
UNION ALL
SELECT 37, 'Interfaces with unexpected status values', 'data_quality',
       (SELECT COUNT(*) FROM interfaces
        WHERE admin_status NOT IN ('up', 'down')
           OR oper_status NOT IN ('up', 'down', 'notconnect', 'unknown')),
       'Interfaces with status values outside the controlled vocabularies.'
UNION ALL
SELECT 38, 'Interfaces with implausible speed values', 'data_quality',
       (SELECT COUNT(*) FROM interfaces
        WHERE speed_mbps < 0 OR (oper_status = 'up' AND speed_mbps <= 0)),
       'Interfaces with a negative speed or an operationally up link without positive speed.'
UNION ALL
SELECT 39, 'Interfaces with unexpected duplex values', 'data_quality',
       (SELECT COUNT(*) FROM interfaces
        WHERE duplex NOT IN ('full', 'half', 'unknown')),
       'Interfaces with duplex outside the controlled vocabulary.'
UNION ALL
SELECT 40, 'Interface description flag mismatches', 'data_quality',
       (SELECT COUNT(*) FROM interfaces
        WHERE (description_present = 1 AND TRIM(description) = '')
           OR (description_present = 0 AND TRIM(description) <> '')),
       'Interfaces where description_present disagrees with the description text.'
UNION ALL
SELECT 41, 'Missing or duplicate topology link IDs', 'data_quality',
       ((SELECT COUNT(*) FROM topology_links WHERE TRIM(link_id) = '')
        + COALESCE((SELECT SUM(row_count) FROM (
            SELECT COUNT(*) AS row_count FROM topology_links
            GROUP BY link_id HAVING COUNT(*) > 1
        )), 0)),
       'Topology links with a missing link_id or an ID shared by multiple rows.'
UNION ALL
SELECT 42, 'Topology links with unexpected status values', 'data_quality',
       (SELECT COUNT(*) FROM topology_links
        WHERE link_status NOT IN ('active', 'inactive', 'planned')),
       'Topology links with link_status outside the controlled vocabulary.'
UNION ALL
SELECT 43, 'Unexpected downstream cardinality values', 'data_quality',
       ((SELECT COUNT(*) FROM interfaces
         WHERE expected_downstream_devices NOT IN ('none', 'single', 'multiple'))
        + (SELECT COUNT(*) FROM topology_links
           WHERE expected_downstream_devices NOT IN ('none', 'single', 'multiple'))),
       'Interface or topology rows with downstream cardinality outside the controlled vocabulary.'
UNION ALL
SELECT 44, 'Duplicate topology relationships', 'data_quality',
       (SELECT COALESCE(SUM(row_count), 0) FROM (
            SELECT COUNT(*) AS row_count FROM topology_links
            GROUP BY source_device_id, source_interface_id,
                     target_device_id, target_interface_id
            HAVING COUNT(*) > 1
        )),
       'Rows describing the same directed source and target relationship more than once.'
UNION ALL
SELECT 45, 'Topology links with unresolved modeled target interfaces', 'data_quality',
       (SELECT COUNT(*) FROM topology_links AS l
        LEFT JOIN interfaces AS i
          ON l.target_device_id = i.device_id
         AND l.target_interface_id = i.interface_id
        WHERE l.target_interface_id <> 'unknown'
          AND i.interface_id IS NULL),
       'Links with a specific target_interface_id that is not present in interfaces.'
UNION ALL
SELECT 46, 'Interfaces with missing interface type', 'data_quality',
       (SELECT COUNT(*) FROM interfaces WHERE TRIM(interface_type) = ''),
       'Interfaces with a missing interface_type.'
)
SELECT
    check_no,
    check_name,
    category,
    CASE
        WHEN category = 'summary' THEN 'INFO'
        WHEN category = 'operational_condition' AND affected_rows > 0 THEN 'WARN'
        WHEN category = 'operational_condition' THEN 'OK'
        WHEN affected_rows > 0 THEN 'FAIL'
        ELSE 'OK'
    END AS status,
    affected_rows,
    description
FROM raw_checks;
