param databaseAccounts_cdb_name string = 'ai-sysk-demo-cdb'

resource databaseAccounts_cdb_name_resource 'Microsoft.DocumentDB/databaseAccounts@2025-05-01-preview' = {
  name: databaseAccounts_cdb_name
  location: 'Central US'
  tags: {
    'hidden-workload-type': 'Production'
    defaultExperience: 'Core (SQL)'
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
        isZoneRedundant: true
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

resource databaseAccounts_cdb_name_ai_state_db 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: 'ai_state_db'
  properties: {
    resource: {
      id: 'ai_state_db'
    }
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

resource databaseAccounts_cdb_name_ai_state_db_state_store_user 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_ai_state_db
  name: 'state_store_user'
  properties: {
    resource: {
      id: 'state_store_user'
      indexingPolicy: {
        indexingMode: 'consistent'
        automatic: true
        includedPaths: [
          {
            path: '/*'
          }
        ]
        excludedPaths: [
          {
            path: '/"_etag"/?'
          }
        ]
      }
      partitionKey: {
        paths: [
          '/tenant_id'
          '/user_id'
          '/id'
        ]
        kind: 'MultiHash'
        version: 2
      }
      uniqueKeyPolicy: {
        uniqueKeys: []
      }
      conflictResolutionPolicy: {
        mode: 'LastWriterWins'
        conflictResolutionPath: '/_ts'
      }
      computedProperties: []
    }
  }
  dependsOn: [
    databaseAccounts_cdb_name_resource
  ]
}

resource databaseAccounts_cdb_name_09f8cd4e_d75e_5acf_ae91_dbec0c280e52 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '09f8cd4e-d75e-5acf-ae91-dbec0c280e52'
  properties: {
    roleDefinitionId: databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000001.id
    principalId: '7456a61f-c865-43b5-8299-7f42f3ab90c9'
    scope: databaseAccounts_cdb_name_resource.id
  }
}

resource databaseAccounts_cdb_name_9a03f9cf_e31f_4494_8349_f71a9963b6de 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '9a03f9cf-e31f-4494-8349-f71a9963b6de'
  properties: {
    roleDefinitionId: databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000002.id
    principalId: '7456a61f-c865-43b5-8299-7f42f3ab90c9'
    scope: databaseAccounts_cdb_name_resource.id
  }
}

resource databaseAccounts_cdb_name_befb9d71_37e3_4e9d_aa2b_fa58f706b771 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: 'befb9d71-37e3-4e9d-aa2b-fa58f706b771'
  properties: {
    roleDefinitionId: databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000002.id
    principalId: '51030c00-82ca-4d55-86ed-b1d7ef829b64'
    scope: databaseAccounts_cdb_name_resource.id
  }
}

resource Microsoft_DocumentDB_databaseAccounts_tableRoleAssignments_databaseAccounts_cdb_name_09f8cd4e_d75e_5acf_ae91_dbec0c280e52 'Microsoft.DocumentDB/databaseAccounts/tableRoleAssignments@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '09f8cd4e-d75e-5acf-ae91-dbec0c280e52'
  properties: {
    roleDefinitionId: Microsoft_DocumentDB_databaseAccounts_tableRoleDefinitions_databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000001.id
    principalId: '7456a61f-c865-43b5-8299-7f42f3ab90c9'
    scope: databaseAccounts_cdb_name_resource.id
  }
}

resource Microsoft_DocumentDB_databaseAccounts_tableRoleAssignments_databaseAccounts_cdb_name_9a03f9cf_e31f_4494_8349_f71a9963b6de 'Microsoft.DocumentDB/databaseAccounts/tableRoleAssignments@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: '9a03f9cf-e31f-4494-8349-f71a9963b6de'
  properties: {
    roleDefinitionId: Microsoft_DocumentDB_databaseAccounts_tableRoleDefinitions_databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000002.id
    principalId: '7456a61f-c865-43b5-8299-7f42f3ab90c9'
    scope: databaseAccounts_cdb_name_resource.id
  }
}

resource Microsoft_DocumentDB_databaseAccounts_tableRoleAssignments_databaseAccounts_cdb_name_befb9d71_37e3_4e9d_aa2b_fa58f706b771 'Microsoft.DocumentDB/databaseAccounts/tableRoleAssignments@2025-05-01-preview' = {
  parent: databaseAccounts_cdb_name_resource
  name: 'befb9d71-37e3-4e9d-aa2b-fa58f706b771'
  properties: {
    roleDefinitionId: Microsoft_DocumentDB_databaseAccounts_tableRoleDefinitions_databaseAccounts_cdb_name_00000000_0000_0000_0000_000000000002.id
    principalId: '51030c00-82ca-4d55-86ed-b1d7ef829b64'
    scope: databaseAccounts_cdb_name_resource.id
  }
}
