# === Gives the provided principal id access to read cosmos data ===

# === Configuration ===
$ResourceGroup   = ""

# === Resource Deployment Create ===
az deployment group create `
    --resource-group $ResourceGroup `
    --template-file update_cosmos.bicep