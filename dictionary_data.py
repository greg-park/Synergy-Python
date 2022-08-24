Appliance = {
            "/controller-state.json",                             'controller-state.txt',
            "/rest/appliance/configuration/time-locale",           'time-locale.txt',
            "/rest/appliance/device-read-community-string",        'device-read-community-string.txt',
            "/rest/appliance/eula/status",                         'eula-status.txt',
            "/rest/appliance/firmware/notification",               'firmware-notification.txt',
            "/rest/appliance/firmware/pending",                    'firmware-pending.txt',
            "/rest/appliance/firmware/verificationKey",            'firmware-verificationkey.txt',
            "/rest/appliance/ha-nodes",                            'ha-nodes.txt',
            "/rest/appliance/health-status",                       'health-status.txt',
            "/rest/appliance/network-interfaces",                  'network-interfaces.txt',
    	    "/rest/appliance/network-interfaces/mac-addresses",    'network-interfaces-mac.txt',
            "/rest/appliance/nodeinfo/status",                     'nodeinfo-status.txt',
            "/rest/appliance/nodeinfo/version",                    'nodeinfo-version.txt',
            "/rest/appliance/notifications/email-config",          'notification-email-config.txt',
    	    "/rest/appliance/notifications/test-email-config",     'notification-test-email-config.txt',
            "/rest/appliance/progress",                            'progress.txt',
            "/rest/appliance/proxy-config",                        'proxy-config.txt',           
            "/rest/appliance/settings/serviceaccess",              'settings-serviceaccess.txt',
            "/rest/appliance/snmpv3-trap-forwarding/destinations", 'snmpv3-destinations.txt', 
            "/rest/appliance/snmpv3-trap-forwarding/users",        'snmpv3-users.txt',     
            "/rest/appliance/ssh-access",                          'ssh-access.txt',
            "/rest/appliance/static-routes",                        'static-routes.txt',
            "/rest/appliance/trap-destinations",                   'trap-destinations.txt',
            "/rest/backups",                                       'backups.txt',
    		"/rest/backups/config",                                'backups-config.txt',
            "/rest/deployment-servers/image-streamer-appliances",  'image-streamer-appliances.txt',
            "/rest/domains",                                       'domains.txt',
            "/rest/domains/schema",                                'domains-schema.txt',
            "/rest/firmware-drivers",                              'firmware-drivers.txt',
            "/rest/global-settings",                               'global-settings.txt',
            "/rest/hardware-compliance",                           'hardware-compliance.txt',
            "/rest/hw-appliances",                                 'hw-appliances.txt',
            "/rest/index/resources?query=`\"NOT scopeUris:NULL`\"",  'scopes-resources.txt',
            "/rest/licenses",                                      'licenses.txt',
    		"/rest/remote-syslog",                                 'remote-syslog.txt',
            "/rest/repositories",                                  'repositories.txt',                
            "/rest/restores",                                      'restores.txt',
    		"/rest/scopes",                                        'scopes.txt',
            "/rest/updates",                                       'updates.txt',                
            "/rest/update-settings/schedule",                      'update-settings-schedule.txt',            
            "/rest/version",                                       'version.txt'
}

#HP OneView Version
hponeviewversion = {
       "/rest/appliance/nodeinfo/version", "version.txt"
}


# FC-SANS
fcsans = {
            "/rest/fc-sans/device-managers",   'device-managers.txt',
            "/rest/fc-sans/managed-sans",      'managed-sans.txt',
            "/rest/fc-sans/providers",         'providers.txt',
            "/rest/fc-sans/endpoints",         'endpoints.txt',
            "/rest/fc-sans/zones",             'zones.txt'
}

# Security
security = {
            "/rest/active-user-sessions",                      'active-user-sessions.txt',
            "/rest/appliance-encryption-key",                  'appliance-encryption-key.txt',
            "/rest/authz/category-actions",                    'authz-category-actions.txt',
            "/rest/certificates",                              'certificates.txt',
            "/rest/certificates/ca",                           'certificates-ca.txt',
            "/rest/certificates/https",                        'certificates-https.txt',
            "/rest/logindetails",                              'logindetails.txt',
            "/rest/logindomains",                              'logindomains.txt',
            "/rest/logindomains/global-settings",              'logindomains-global-settings.txt',
            "/rest/logindomains/grouptorolemapping",           'logindomains-grouptorolemapping.txt',
            "/rest/roles",                                     'roles.txt',
            "/rest/secure-data-at-rest",                       'secure-data-at-rest.txt',
            "/rest/security-standards/modes",                  'security-modes.txt',
            "/rest/security-standards/modes/current-mode",     'security-current-mode.txt',
            "/rest/security-standards/protocols",              'security-protocols.txt',
            "/rest/appliance/sshhostkeys",                     'sshhostkeys.txt',
            "/rest/users",                                     'users.txt'
}

#Activity
activity =
    {
    "/rest/audit-logs?filter=`"DATE >= '" + historyDate + "'`""},                 'audit-logs.txt',
    "/rest/audit-logs/settings"},                                                  'audit-logs-settings.txt',
    "/rest/alerts?start=0&count=300&sort=created:descending",                       'alerts.txt',
    "/rest/alerts?sort=created:descending&filter=`\"serviceEventSource='true'`\"",    'alerts-service-events.txt',
    "/rest/events?start=0&count=300&sort=created:descending",                       'events.txt',
    "/rest/tasks?sort=created:descending&filter=`\"created ge " + historyDateTasks + "T00:00:01.830Z`\"",  'tasks.txt'
}

#Servers
servers = {
    		"/rest/connections",                  'connections.txt',
    		"/rest/server-hardware",              'server-hardware.txt',
    		"/rest/server-hardware-types",        'server-hardware-types.txt',
    		"/rest/server-profiles?count=2048",   'server-profiles.txt',
    		"/rest/server-profile-templates",     'server-profile-templates.txt',
    		"/rest/server-hardware/*/firmware",   'firmware.txt',
            "/rest/rack-managers",                'rack-managers.txt'
}

#Enclosures
enclosures= {
    		"/rest/logical-enclosures",      'logical-enclosures.txt',
    		"/rest/enclosure-groups",        'enclosure-groups.txt',
    		"/rest/enclosures",              'enclosures.txt'
		}

#Networking
networking = {
    		"/rest/connection-templates",            'connection-templates.txt',
            "/rest/connections",                     'connections.txt',
    		"/rest/ethernet-networks",               'ethernet-networks.txt',
            "/rest/fabric-managers",                 'fabric-managers.txt',  
            "/rest/fabrics",                         'fabrics.txt',
    		"/rest/fc-networks",                     'fc-networks.txt',
            "/rest/fcoe-networks",                   'fcoe-networks.txt',  
            "/rest/roce-networks",                   'roce-networks.txt',  
            "/rest/interconnect-link-topologies",    'interconnect-link-topologies.txt',
            "/rest/interconnect-types",              'interconnect-types.txt',
    		"/rest/interconnects",                   'interconnects.txt',
            "/rest/internal-link-sets",              'internal-link-sets.txt',    # v2.1
    		"/rest/logical-downlinks",               'logical-downlinks.txt',     # v2.1
    		"/rest/logical-interconnect-groups",     'logical-interconnect-groups.txt',
    		"/rest/logical-interconnects",           'logical-interconnects.txt',
            "/rest/logical-switch-groups",           'logical-switch-groups.txt',  
            "/rest/logical-switches",                'logical-switches.txt',  
    		"/rest/network-sets",                    'network-sets.txt',
            "/rest/switch-types",                    'switch-types.txt',
  	        "/rest/switches",                        'switches.txt',
    		"/rest/uplink-sets",                     'uplink-sets.txt'
}

#Storage
storage = {
    		"/rest/storage-pools",               'storage-pools.txt',
            "/rest/storage-systems",             'storage-systems.txt',
    		"/rest/storage-volume-attachments",  'storage-volume-attachments.txt',
            "/rest/storage-volume-sets",         'storage-volume-sets.txt',
    		"/rest/storage-volume-templates",    'storage-volume-templates.txt',
            "/rest/storage-volumes",             'storage-volumes.txt'
}

#Hypervisor
hypervisor = {
    		"/rest/hypervisor-cluster-profiles", 'hypervisor-cluster-profiles.txt',
    		"/rest/hypervisor-host-profiles",    'hypervisor-host-profiles.txt',
            "/rest/hypervisor-managers",         'hypervisor-managers.txt'
}

#Deployment
deployment = {
    		"/rest/os-deployment-plans/",                            'os-deployment-plans.txt',
    		"/rest/deployment-servers",                              'deployment-servers.txt',
            "/rest/deployment-servers/image-streamer-appliances",    'image-streamer-appliances.txt',
            "/rest/deployment-servers/network",                      'network.txt'
}

#Facilities
facilities = {
    		"/rest/datacenters",     'datacenters.txt',
    		"/rest/power-devices",   'power-devices.txt',
    		"/rest/racks",           'racks.txt'
}

#Uncategorized
uncategorized = {
    		"/rest/migratable-vc-domains",  'migratable-vc-domains.txt',
    		"/rest/unmanaged-devices",       'unmanaged-devices.txt'
}

#Index
#index = {
#		"/rest/index/associations",
#		"/rest/index/associations/resources",
#		"/rest/index/resources",
#		"/rest/index/resources/aggregated",
#		"/rest/index/trees",
#		"/rest/index/trees/minified",
#		"/rest/labels"
#}

# SAS Storage
sas= {
            "/rest/drive-enclosures",                  'drive-enclosures.txt',
            "/rest/sas-interconnect-types",            'sas-interconnect-types.txt',
            "/rest/sas-interconnects",                 'sas-interconnects.txt',
            "/rest/sas-logical-interconnect-groups",   'sas-logical-interconnect-groups.txt',
            "/rest/sas-logical-interconnects",         'sas-logical-interconnects.txt',
            "/rest/sas-logical-jbod-attachments",      'sas-logical-jbod-attachments.txt',
            "/rest/sas-logical-jbods",                 'sas-logical-jbods.txt'
}

# Service Automation
sa = {
            "/rest/support/channel-partners",              'channel-partners.txt',
            "/rest/support/configuration",                 'configuration.txt',
            "/rest/support/contacts",                      'contacts.txt',
            "/rest/support/entitlements",                   'entitlements.txt',
            # "/rest/support/datacenters",                   'datacenters.txt',
            # "/rest/support/data-collections",              'data-collections.txt',
            # "/rest/support/enclosures",                    'enclosures.txt',
            "/rest/support/portal-registration",           'portal-registration.txt',
            "/rest/support/registration",                  'registration.txt',
            "/rest/support/schedules",                     'schedules.txt',
            "/rest/support/sites/default",                 'sites-default.txt'
            # "/rest/support/server-hardware",               'server-hardware.txt',
            # "/rest/support/sites",                         'sites.txt'
}

# id-pools
idpools= {
        "/rest/id-pools/schema",               'schema.txt',
        "/rest/id-pools/ipv4/ranges/schema",   'ipv4-ranges-schema.txt',
        "/rest/id-pools/ipv4/subnets",         'subnets.txt',
        "/rest/id-pools/ipv6/ranges/schema",   'ipv6-ranges-schema.txt',
        "/rest/id-pools/ipv6/subnets",         'ipv6-subnets.txt',
        "/rest/id-pools/vmac",                 'vmac.txt',
        "/rest/id-pools/vmac/ranges/schema",   'vmac-ranges-schema.txt',
        "/rest/id-pools/vsn",                  'vsn.txt',
        "/rest/id-pools/vsn/ranges/schema",    'vsn-ranges-schema.txt',
        "/rest/id-pools/vwwn",                 'vwwn.txt',
        "/rest/id-pools/vwwn/ranges/schema",   'vwwn-ranges-schema.txt'
}

resourceArray = {
    "Appliance",          Appliance,
    "HP-OneView-Version", hponeviewversion,
    "FC-SAN",             fcsans,
    "Security",           security,
    "Activity",           activity,
    "Servers",            servers,
    "Enclosures",         enclosures,
    "Networking",         networking,
    "Storage",            storage,
    "Deployment",         deployment,
    "Hypervisor",         hypervisor,
    "Facilities",         facilities,
    "Uncategorized",      uncategorized,
    #{"Index",              index},
    "SAS-Storage",        sas,
    "Service-Automation", sa,
    "Facilities",         facilities,
    "ID-Pools",           idpools
}