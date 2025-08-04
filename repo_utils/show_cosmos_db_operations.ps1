# Fetch operations JSON as a string
$jsonString = az provider operation show --namespace Microsoft.DocumentDB

# Save raw JSON string to a file
$jsonString | Out-File -FilePath "./cosmos_operations.json" -Encoding utf8

# # Convert to object
# $operations = $jsonString | ConvertFrom-Json

# # Filter for resourceType "databaseAccounts"
# $databaseAccountsOps = $operations.resourceTypes | Where-Object { $_.resourceType -eq 'databaseAccounts' }
# $databaseAccountsOps
