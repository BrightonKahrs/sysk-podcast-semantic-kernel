# === Gives the provided principal id access to read cosmos data ===

# === Configuration ===
$ResourceGroup   = ""
$AccountName     = ""
$SubscriptionId = ""
$PrincipalId     = ""
$RoleDefinitionId = "/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroup/providers/Microsoft.DocumentDB/databaseAccounts/$AccountName/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002"
$Scope           = "/subscriptions/$SubscriptionId/resourceGroups/$ResourceGroup/providers/Microsoft.DocumentDB/databaseAccounts/$AccountName"

# === Role Assignment Command ===
az cosmosdb sql role assignment create `
    --resource-group $ResourceGroup `
    --account-name $AccountName `
    --role-definition-id $RoleDefinitionId `
    --principal-id $PrincipalId `
    --scope $Scope