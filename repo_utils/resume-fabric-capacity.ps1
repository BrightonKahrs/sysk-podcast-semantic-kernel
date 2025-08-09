# === Fabric Configuration ===
$ResourceGroup = "ai-sysk-demo"
$FabricCapacityName = "fabricsyskai"

# === Run Deployment ===
az fabric capacity resume `
    --resource-group $ResourceGroup `
    --capacity-name $FabricCapacityName