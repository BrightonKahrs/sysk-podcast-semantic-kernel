# === For dev environment use ONLY - gives localauth and public internet access to cosmos db account ===

# === Configuration ===
$ResourceGroup = "ai-sysk-demo-dev"
$DatabaseAccountName = "ai-sysk-demo-dev-cdb"

# === Run Deployment ===
az deployment group create `
  --resource-group $ResourceGroup `
  --template-file "update-cosmos.bicep" `
  --parameters databaseAccounts_ai_sysk_demo_dev_cdb_name=$DatabaseAccountName
