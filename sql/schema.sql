PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS data_quality_results;
DROP VIEW IF EXISTS documentation_coverage;
DROP VIEW IF EXISTS topology_link_status_summary;
DROP VIEW IF EXISTS port_role_summary;
DROP VIEW IF EXISTS interface_status_summary;
DROP VIEW IF EXISTS device_count_by_role;

DROP TABLE IF EXISTS topology_links;
DROP TABLE IF EXISTS interfaces;
DROP TABLE IF EXISTS devices;

CREATE TABLE devices (
    device_id TEXT PRIMARY KEY CHECK (TRIM(device_id) <> ''),
    device_name TEXT NOT NULL UNIQUE CHECK (TRIM(device_name) <> ''),
    device_type TEXT NOT NULL CHECK (
        device_type IN ('switch', 'router', 'wireless_bridge', 'client')
    ),
    vendor TEXT NOT NULL CHECK (TRIM(vendor) <> ''),
    model TEXT NOT NULL CHECK (TRIM(model) <> ''),
    role TEXT NOT NULL CHECK (
        role IN ('access_switch', 'edge_router', 'media_bridge', 'lab_client')
    ),
    location TEXT NOT NULL CHECK (TRIM(location) <> ''),
    location_scope TEXT NOT NULL CHECK (
        location_scope IN ('home_lab', 'external_lab')
    ),
    management_scope TEXT NOT NULL CHECK (
        management_scope IN ('managed', 'endpoint', 'unmanaged')
    ),
    is_active INTEGER NOT NULL CHECK (is_active IN (0, 1))
);

CREATE TABLE interfaces (
    interface_id TEXT PRIMARY KEY CHECK (TRIM(interface_id) <> ''),
    device_id TEXT NOT NULL,
    device_name TEXT NOT NULL CHECK (TRIM(device_name) <> ''),
    interface_name TEXT NOT NULL CHECK (TRIM(interface_name) <> ''),
    interface_type TEXT NOT NULL CHECK (TRIM(interface_type) <> ''),
    admin_status TEXT NOT NULL CHECK (
        admin_status IN ('up', 'down')
    ),
    oper_status TEXT NOT NULL CHECK (
        oper_status IN ('up', 'down', 'notconnect', 'unknown')
    ),
    vlan TEXT NOT NULL CHECK (TRIM(vlan) <> ''),
    port_role TEXT NOT NULL CHECK (
        port_role IN (
            'access', 'trunk', 'uplink', 'client_access',
            'lab_access', 'bridge_uplink'
        )
    ),
    speed_mbps INTEGER NOT NULL CHECK (speed_mbps >= 0),
    duplex TEXT NOT NULL CHECK (
        duplex IN ('full', 'half', 'unknown')
    ),
    description TEXT NOT NULL,
    description_present INTEGER NOT NULL CHECK (
        description_present IN (0, 1)
    ),
    expected_downstream_devices TEXT NOT NULL CHECK (
        expected_downstream_devices IN ('none', 'single', 'multiple')
    ),
    FOREIGN KEY (device_id) REFERENCES devices(device_id),
    UNIQUE (device_id, interface_name),
    UNIQUE (device_id, interface_id)
);

CREATE TABLE topology_links (
    link_id TEXT PRIMARY KEY CHECK (TRIM(link_id) <> ''),
    source_device_id TEXT NOT NULL,
    source_interface_id TEXT NOT NULL,
    target_device_id TEXT NOT NULL,
    target_interface_id TEXT NOT NULL CHECK (TRIM(target_interface_id) <> ''),
    link_role TEXT NOT NULL CHECK (
        link_role IN (
            'access', 'trunk', 'uplink', 'client_access',
            'lab_access', 'bridge_uplink'
        )
    ),
    link_status TEXT NOT NULL CHECK (
        link_status IN ('active', 'inactive', 'planned')
    ),
    expected_downstream_devices TEXT NOT NULL CHECK (
        expected_downstream_devices IN ('none', 'single', 'multiple')
    ),
    FOREIGN KEY (source_device_id, source_interface_id)
        REFERENCES interfaces(device_id, interface_id),
    FOREIGN KEY (target_device_id)
        REFERENCES devices(device_id),
    UNIQUE (
        source_device_id,
        source_interface_id,
        target_device_id,
        target_interface_id
    )
);

CREATE INDEX idx_interfaces_device_id
    ON interfaces(device_id);

CREATE INDEX idx_interfaces_status
    ON interfaces(admin_status, oper_status);

CREATE INDEX idx_topology_target_device
    ON topology_links(target_device_id);
