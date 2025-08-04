# === Gives the provided principal id access to read cosmos data ===

# === Configuration ===
$ResourceGroup   = "ai-sysk-demo-dev"
$AccountName     = "ai-sysk-demo-dev-cdb"
$SubscriptionId = "51030c00-82ca-4d55-86ed-b1d7ef829b64"
$RoleDefinitionId = "/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroup/providers/Microsoft.DocumentDB/databaseAccounts/$AccountName/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002"
$PrincipalId     = "7456a61f-c865-43b5-8299-7f42f3ab90c9"
$Scope           = "/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroup/providers/Microsoft.DocumentDB/databaseAccounts/$AccountName"

# === Role Assignment Command ===
az cosmosdb sql role assignment create `
    --resource-group $ResourceGroup `
    --account-name $AccountName `
    --role-definition-id $RoleDefinitionId `
    --principal-id $PrincipalId `
    --scope $Scope