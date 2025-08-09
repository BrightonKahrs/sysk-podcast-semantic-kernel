param databaseAccounts_cdb_name string = 'ai-sysk-demo-dev-cdb'

resource databaseAccounts_cdb_name_resource 'Microsoft.DocumentDB/databaseAccounts@2025-05-01-preview' = {
  name: databaseAccounts_cdb_name
  location: 'Central US'
  tags: {
    defaultExperience: 'Core (SQL)'
    'hidden-workload-type': 'Development/Testing'
    'hidden-cosmos-mmspecial': ''
  }
  kind: 'GlobalDocumentDB'
  identity: {
    type: 'None'
  }
  properties: {
    publicNetworkAccess: 'Enabled'
    enableAutomaticFailover: true
    enableMultipleWriteLocations: false
    isVirtualNetworkFilterEnabled: false
    virtualNetworkRules: []
    disableKeyBasedMetadataWriteAccess: false
    enableFreeTier: false
    enableAnalyticalStorage: false
    analyticalStorageConfiguration: {
      schemaType: 'WellDefined'
    }
    databaseAccountOfferType: 'Standard'
    enableMaterializedViews: false
    capacityMode: 'Serverless'
    defaultIdentity: 'FirstPartyIdentity'
    networkAclBypass: 'None'
    disableLocalAuth: false
    enablePartitionMerge: false
    enablePerRegionPerPartitionAutoscale: false
    enableBurstCapacity: false
    enablePriorityBasedExecution: false
    defaultPriorityLevel: 'High'
    minimalTlsVersion: 'Tls12'
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
      maxIntervalInSeconds: 5
      maxStalenessPrefix: 100
    }
    locations: [
      {
        locationName: 'Central US'
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    cors: []
    capabilities: []
    ipRules: []
    backupPolicy: {
      type: 'Periodic'
      periodicModeProperties: {
        backupIntervalInMinutes: 240
        backupRetentionIntervalInHours: 8
        backupStorageRedundancy: 'Geo'
      }
    }
    networkAclBypassResourceIds: []
    diagnosticLogSettings: {
      enableFullTextQuery: 'None'
    }
    capacity: {
      totalThroughputLimit: 4000
    }
  }
}

resource databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000003 'Microsoft.DocumentDB/databaseAccounts/cassandraRoleDefinitions@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '00000000-0000-0000-0000-000000000003'
  properties: {
    roleName: 'Cosmos DB Built-in Data Reader'
    type: 'BuiltInRole'
    assignableScopes: [
      databaseAccounts_cdb_name_resource.id
    ]
    permissions: [
      {
        dataActions: [
          'Microsoft.DocumentDB/databaseAccounts/readMetadata'
          'Microsoft.DocumentDB/databaseAccounts/throughputSettings/read'
          'Microsoft.DocumentDB/databaseAccounts/cassandra/containers/executeQuery'
          'Microsoft.DocumentDB/databaseAccounts/cassandra/containers/readChangeFeed'
          'Microsoft.DocumentDB/databaseAccounts/cassandra/containers/entities/read'
        ]
        notDataActions: []
      }
    ]
  }
}

resource databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000004 'Microsoft.DocumentDB/databaseAccounts/cassandraRoleDefinitions@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '00000000-0000-0000-0000-000000000004'
  properties: {
    roleName: 'Cosmos DB Built-in Data Contributor'
    type: 'BuiltInRole'
    assignableScopes: [
      databaseAccounts_cdb_name_resource.id
    ]
    permissions: [
      {
        dataActions: [
          'Microsoft.DocumentDB/databaseAccounts/readMetadata'
          'Microsoft.DocumentDB/databaseAccounts/throughputSettings/read'
          'Microsoft.DocumentDB/databaseAccounts/throughputSettings/write'
          'Microsoft.DocumentDB/databaseAccounts/cassandra/*'
          'Microsoft.DocumentDB/databaseAccounts/cassandra/write'
          'Microsoft.DocumentDB/databaseAccounts/cassandra/delete'
          'Microsoft.DocumentDB/databaseAccounts/cassandra/containers/*'
          'Microsoft.DocumentDB/databaseAccounts/cassandra/containers/entities/*'
        ]
        notDataActions: []
      }
    ]
  }
}

resource Microsoft_DocumentDB_databaseAccounts_gremlinRoleDefinitions_databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000003 'Microsoft.DocumentDB/databaseAccounts/gremlinRoleDefinitions@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '00000000-0000-0000-0000-000000000003'
  properties: {
    roleName: 'Cosmos DB Built-in Data Reader'
    type: 'BuiltInRole'
    assignableScopes: [
      databaseAccounts_cdb_name_resource.id
    ]
    permissions: [
      {
        dataActions: [
          'Microsoft.DocumentDB/databaseAccounts/readMetadata'
          'Microsoft.DocumentDB/databaseAccounts/throughputSettings/read'
          'Microsoft.DocumentDB/databaseAccounts/gremlin/containers/executeQuery'
          'Microsoft.DocumentDB/databaseAccounts/gremlin/containers/readChangeFeed'
          'Microsoft.DocumentDB/databaseAccounts/gremlin/containers/entities/read'
        ]
        notDataActions: []
      }
    ]
  }
}

resource Microsoft_DocumentDB_databaseAccounts_gremlinRoleDefinitions_databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000004 'Microsoft.DocumentDB/databaseAccounts/gremlinRoleDefinitions@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '00000000-0000-0000-0000-000000000004'
  properties: {
    roleName: 'Cosmos DB Built-in Data Contributor'
    type: 'BuiltInRole'
    assignableScopes: [
      databaseAccounts_cdb_name_resource.id
    ]
    permissions: [
      {
        dataActions: [
          'Microsoft.DocumentDB/databaseAccounts/readMetadata'
          'Microsoft.DocumentDB/databaseAccounts/throughputSettings/read'
          'Microsoft.DocumentDB/databaseAccounts/throughputSettings/write'
          'Microsoft.DocumentDB/databaseAccounts/gremlin/*'
          'Microsoft.DocumentDB/databaseAccounts/gremlin/write'
          'Microsoft.DocumentDB/databaseAccounts/gremlin/delete'
          'Microsoft.DocumentDB/databaseAccounts/gremlin/containers/*'
          'Microsoft.DocumentDB/databaseAccounts/gremlin/containers/entities/*'
        ]
        notDataActions: []
      }
    ]
  }
}

resource Microsoft_DocumentDB_databaseAccounts_mongoMIRoleDefinitions_databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000003 'Microsoft.DocumentDB/databaseAccounts/mongoMIRoleDefinitions@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '00000000-0000-0000-0000-000000000003'
  properties: {
    roleName: 'Cosmos DB Built-in Data Reader'
    type: 'BuiltInRole'
    assignableScopes: [
      databaseAccounts_cdb_name_resource.id
    ]
    permissions: [
      {
        dataActions: [
          'Microsoft.DocumentDB/databaseAccounts/readMetadata'
          'Microsoft.DocumentDB/databaseAccounts/throughputSettings/read'
          'Microsoft.DocumentDB/databaseAccounts/mongoMI/containers/executeQuery'
          'Microsoft.DocumentDB/databaseAccounts/mongoMI/containers/readChangeFeed'
          'Microsoft.DocumentDB/databaseAccounts/mongoMI/containers/entities/read'
        ]
        notDataActions: []
      }
    ]
  }
}

resource Microsoft_DocumentDB_databaseAccounts_mongoMIRoleDefinitions_databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000004 'Microsoft.DocumentDB/databaseAccounts/mongoMIRoleDefinitions@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '00000000-0000-0000-0000-000000000004'
  properties: {
    roleName: 'Cosmos DB Built-in Data Contributor'
    type: 'BuiltInRole'
    assignableScopes: [
      databaseAccounts_cdb_name_resource.id
    ]
    permissions: [
      {
        dataActions: [
          'Microsoft.DocumentDB/databaseAccounts/readMetadata'
          'Microsoft.DocumentDB/databaseAccounts/throughputSettings/read'
          'Microsoft.DocumentDB/databaseAccounts/throughputSettings/write'
          'Microsoft.DocumentDB/databaseAccounts/mongoMI/*'
          'Microsoft.DocumentDB/databaseAccounts/mongoMI/write'
          'Microsoft.DocumentDB/databaseAccounts/mongoMI/delete'
          'Microsoft.DocumentDB/databaseAccounts/mongoMI/containers/*'
          'Microsoft.DocumentDB/databaseAccounts/mongoMI/containers/entities/*'
        ]
        notDataActions: []
      }
    ]
  }
}

resource databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000001 'Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '00000000-0000-0000-0000-000000000001'
  properties: {
    roleName: 'Cosmos DB Built-in Data Reader'
    type: 'BuiltInRole'
    assignableScopes: [
      databaseAccounts_cdb_name_resource.id
    ]
    permissions: [
      {
        dataActions: [
          'Microsoft.DocumentDB/databaseAccounts/readMetadata'
          'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/executeQuery'
          'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/readChangeFeed'
          'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/read'
        ]
        notDataActions: []
      }
    ]
  }
}

resource databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000002 'Microsoft.DocumentDB/databaseAccounts/sqlRoleDefinitions@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '00000000-0000-0000-0000-000000000002'
  properties: {
    roleName: 'Cosmos DB Built-in Data Contributor'
    type: 'BuiltInRole'
    assignableScopes: [
      databaseAccounts_cdb_name_resource.id
    ]
    permissions: [
      {
        dataActions: [
          'Microsoft.DocumentDB/databaseAccounts/readMetadata'
          'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/*'
          'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers/items/*'
        ]
        notDataActions: []
      }
    ]
  }
}

resource Microsoft_DocumentDB_databaseAccounts_tableRoleDefinitions_databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000001 'Microsoft.DocumentDB/databaseAccounts/tableRoleDefinitions@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '00000000-0000-0000-0000-000000000001'
  properties: {
    roleName: 'Cosmos DB Built-in Data Reader'
    type: 'BuiltInRole'
    assignableScopes: [
      databaseAccounts_cdb_name_resource.id
    ]
    permissions: [
      {
        dataActions: [
          'Microsoft.DocumentDB/databaseAccounts/readMetadata'
          'Microsoft.DocumentDB/databaseAccounts/tables/containers/executeQuery'
          'Microsoft.DocumentDB/databaseAccounts/tables/containers/readChangeFeed'
          'Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/read'
        ]
        notDataActions: []
      }
    ]
  }
}

resource Microsoft_DocumentDB_databaseAccounts_tableRoleDefinitions_databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000002 'Microsoft.DocumentDB/databaseAccounts/tableRoleDefinitions@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '00000000-0000-0000-0000-000000000002'
  properties: {
    roleName: 'Cosmos DB Built-in Data Contributor'
    type: 'BuiltInRole'
    assignableScopes: [
      databaseAccounts_cdb_name_resource.id
    ]
    permissions: [
      {
        dataActions: [
          'Microsoft.DocumentDB/databaseAccounts/readMetadata'
          'Microsoft.DocumentDB/databaseAccounts/tables/*'
          'Microsoft.DocumentDB/databaseAccounts/tables/containers/*'
          'Microsoft.DocumentDB/databaseAccounts/tables/containers/entities/*'
        ]
        notDataActions: []
      }
    ]
  }
}

resource databaseAccounts_cdb_name_0276e190_1983_4f9e_8015_5bd361da4106 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '0276e190-1983-4f9e-8015-5bd361da4106'
  properties: {
    roleDefinitionId: databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000002.id
    principalId: '7456a61f-c865-43b5-8299-7f42f3ab90c9'
    scope: databaseAccounts_cdb_name_resource.id
  }
}

resource databaseAccounts_cdb_name_df0cd689_a5e3_4de7_b487_639da3a64d5e 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: 'df0cd689-a5e3-4de7-b487-639da3a64d5e'
  properties: {
    roleDefinitionId: databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000002.id
    principalId: '7456a61f-c865-43b5-8299-7f42f3ab90c9'
    scope: databaseAccounts_cdb_name_resource.id
  }
}

resource Microsoft_DocumentDB_databaseAccounts_tableRoleAssignments_databaseAccounts_cdb_name_0276e190_1983_4f9e_8015_5bd361da4106 'Microsoft.DocumentDB/databaseAccounts/tableRoleAssignments@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '0276e190-1983-4f9e-8015-5bd361da4106'
  properties: {
    roleDefinitionId: Microsoft_DocumentDB_databaseAccounts_tableRoleDefinitions_databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000002.id
    principalId: '7456a61f-c865-43b5-8299-7f42f3ab90c9'
    scope: databaseAccounts_cdb_name_resource.id
  }
}

resource Microsoft_DocumentDB_databaseAccounts_tableRoleAssignments_databaseAccounts_cdb_name_df0cd689_a5e3_4de7_b487_639da3a64d5e 'Microsoft.DocumentDB/databaseAccounts/tableRoleAssignments@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: 'df0cd689-a5e3-4de7-b487-639da3a64d5e'
  properties: {
    roleDefinitionId: Microsoft_DocumentDB_databaseAccounts_tableRoleDefinitions_databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000002.id
    principalId: '7456a61f-c865-43b5-8299-7f42f3ab90c9'
    scope: databaseAccounts_cdb_name_resource.id
  }
}

