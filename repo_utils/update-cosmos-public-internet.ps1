# === Dev Configuration ===
$ResourceGroup = "ai-sysk-demo-dev"
$TemplateFile = "C:\Users\brigh\Projects\Work\sysk-podcast-semantic-kernel\repo_utils\update-dev-cosmos.bicep"
$DatabaseAccountName = "ai-sysk-demo-dev-cdb"

# === Run Deployment ===
az deployment group create `
  --resource-group $ResourceGroup `
  --template-file $TemplateFile `
  --parameters databaseAccounts_cdb_name=$DatabaseAccountName


# === Test Configuration ===
$ResourceGroup = "ai-sysk-demo-test"
$TemplateFile = "C:\Users\brigh\Projects\Work\sysk-podcast-semantic-kernel\repo_utils\update-test-cosmos.bicep"
$DatabaseAccountName = "ai-sysk-demo-test-cdb"

# === Run Deployment ===
az deployment group create `
  --resource-group $ResourceGroup `
  --template-file $TemplateFile `
  --parameters databaseAccounts_cdb_name=$DatabaseAccountName


# === Prod Configuration ===
$ResourceGroup = "ai-sysk-demo"
$TemplateFile = "C:\Users\brigh\Projects\Work\sysk-podcast-semantic-kernel\repo_utils\update-prod-cosmos.bicep"
$DatabaseAccountName = "ai-sysk-demo-cdb"

# === Run Deployment ===
az deployment group create `
  --resource-group $ResourceGroup `
  --template-file $TemplateFile `
  --parameters databaseAccounts_cdb_name=$DatabaseAccountName