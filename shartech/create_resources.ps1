$env:AZ_RESSOURCE_GROUP = 'shartech'
$env:SUBS_ID = '64ac692e-19e2-427e-bc88-db0b8a3868e0'

# az login
$exist = az group exists -n $env:AZ_RESSOURCE_GROUP
if($exist -ne $true) {
  az group create --name $env:AZ_RESSOURCE_GROUP --location eastus
} else {
  Write-Output "${env:AZ_RESSOURCE_GROUP} exists"
}

Write-Output "Create User Assigned Managed Identity"
$env:AZ_UAMI = "${env:AZ_RESSOURCE_GROUP}-UAMI"
az identity create --resource-group $env:AZ_RESSOURCE_GROUP --name $env:AZ_UAMI

# Get service principal ID of the user-assigned identity
$env:SVC_ID = $(az identity show --resource-group $env:AZ_RESSOURCE_GROUP --name $env:AZ_UAMI --query principalId --output tsv)

# az keyvault create -h
# Write-Output "List Soft Delete KeyVault"
# az keyvault list-deleted --subscription $env:SUBS_ID --resource-type vault

# Write-Output "Purge KeyVault"
# az keyvault purge --subscription $env:SUBS_ID -n "${env:AZ_RESSOURCE_GROUP}-kv"

# Write-Output "Recover KeyVault"
# az keyvault recover --subscription $env:SUBS_ID -n "${env:AZ_RESSOURCE_GROUP}-kv"

Write-Output "Creating KeyVault"
$env:AZ_KEY_VAULT = "${env:AZ_RESSOURCE_GROUP}-kv"
az keyvault create -g $env:AZ_RESSOURCE_GROUP -n $env:AZ_KEY_VAULT --enable-soft-delete false --enabled-for-deployment true

# Grant user-assigned identity access to the key vault
Write-Output "Grant user-assigned identity access to the key vault"
az keyvault set-policy --name $env:AZ_KEY_VAULT --resource-group $env:AZ_RESSOURCE_GROUP --object-id $env:SVC_ID --secret-permissions get

Write-Output "Creating Container Registry"
$env:AZ_ACR_REGISTRY = "$env:AZ_RESSOURCE_GROUP"
Write-Output "Container Registry Name: ${env:AZ_ACR_REGISTRY}"
# az acr create -h
$env:AZ_ACR_REGISTRY_ID = az acr create --resource-group $env:AZ_RESSOURCE_GROUP --name $env:AZ_ACR_REGISTRY --sku Basic --location eastus --query id --output tsv

# Grant the identity a role assignment
Write-Output "Grant the identity a role assignment for Container Registry"
az role assignment create --assignee $env:SVC_ID --scope $env:AZ_ACR_REGISTRY_ID --role acrpull

Write-Output "Create container registry service principal"
$env:SP_ID = az ad sp create-for-rbac --name "http://${env:AZ_ACR_REGISTRY}-pull" --scopes $(az acr show --name $env:AZ_ACR_REGISTRY --query id --output tsv) --role acrpull --query appId --output tsv
$env:SP_PWD =  az ad sp create-for-rbac --name "http://${env:AZ_ACR_REGISTRY}-pull" --scopes $(az acr show --name $env:AZ_ACR_REGISTRY --query id --output tsv) --role acrpull --query password --output tsv

Write-Output "Store the registry *password* in the vault"
az keyvault secret set --vault-name "${env:AZ_RESSOURCE_GROUP}-kv" --name "${env:AZ_ACR_REGISTRY}-pull-pwd" --value $env:SP_PWD
Write-Output "Store service principal ID in vault (the registry *username*)"
az keyvault secret set --vault-name "${env:AZ_RESSOURCE_GROUP}-kv" --name "${env:AZ_ACR_REGISTRY}-pull-usr" --value $env:SP_ID


Write-Output "Creating Storage Account"
# az storage account create -h
$env:AZ_STORAGE_ACCOUNT = "${env:AZ_RESSOURCE_GROUP}storage"
Write-Output "Storage Account: ${env:AZ_STORAGE_ACCOUNT}"
az storage account create -n "$env:AZ_STORAGE_ACCOUNT" -g $env:AZ_RESSOURCE_GROUP -l eastus --sku Standard_LRS

Write-Output "Creating Function App"
# az functionapp create -h
$env:AZ_FUNC_APP = "${env:AZ_RESSOURCE_GROUP}-func-app"
Write-Output "Function App: ${env:AZ_FUNC_APP}"
az functionapp create --consumption-plan-location eastus --name $env:AZ_FUNC_APP --os-type Windows --resource-group $env:AZ_RESSOURCE_GROUP --runtime powershell --storage-account $env:AZ_STORAGE_ACCOUNT --functions-version 3

Write-Output "Creating Service Bus Namespace"
$env:AZ_SERVICE_BUS_NAMESPACE = "${env:AZ_RESSOURCE_GROUP}-svc-bus-namespace"
# az servicebus namespace create -h
Write-Output "Service Bus Namespace: ${env:AZ_SERVICE_BUS_NAMESPACE}"
az servicebus namespace create --resource-group $env:AZ_RESSOURCE_GROUP --name $env:AZ_SERVICE_BUS_NAMESPACE --location eastus

Write-Output "Set Service Bus Connection String to keyvault"
$env:CONNECTION_STRING = az servicebus namespace authorization-rule keys list --resource-group $env:AZ_RESSOURCE_GROUP --namespace-name $env:AZ_SERVICE_BUS_NAMESPACE --name RootManageSharedAccessKey --query secondaryConnectionString --output tsv
az keyvault secret set --vault-name "${env:AZ_RESSOURCE_GROUP}-kv" --name "${env:AZ_SERVICE_BUS_NAMESPACE}-cnc-string" --value $env:CONNECTION_STRING


Set-Location ./inc42
.\create_resources.ps1
Set-Location ..