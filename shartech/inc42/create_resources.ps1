$env:resourceprefix = "inc42"
$env:AZ_RESOURCE_GROUP = "shartech"
$env:AZ_ACR_REGISTRY = "${env:AZ_RESOURCE_GROUP}"
$env:AZ_KEY_VAULT = "${env:AZ_RESOURCE_GROUP}-kv"
$env:AZ_UAMI = "${env:AZ_RESOURCE_GROUP}-UAMI"

az login

# Write-Output "Create Service Bus Queues"
# $env:QUEUE = "${env:resourceprefix}-pages"
# Write-Output "Queue Name: ${env:QUEUE}"
# az servicebus queue create --resource-group $env:AZ_RESOURCE_GROUP --namespace-name "${env:AZ_RESOURCE_GROUP}-svc-bus-namespace" --name $env:QUEUE

# $env:QUEUE = "${env:resourceprefix}-articles"
# Write-Output "Queue Name: ${env:QUEUE}"
# az servicebus queue create --resource-group $env:AZ_RESOURCE_GROUP --namespace-name "${env:AZ_RESOURCE_GROUP}-svc-bus-namespace" --name $env:QUEUE

# $env:QUEUE = "${env:resourceprefix}-seo"
# Write-Output "Queue Name: ${env:QUEUE}"
# az servicebus queue create --resource-group $env:AZ_RESOURCE_GROUP --namespace-name "${env:AZ_RESOURCE_GROUP}-svc-bus-namespace" --name $env:QUEUE


# Get resource ID & SP ID of the user-assigned identity
Write-Output "Get resource ID & SP ID of the user-assigned identity"
$env:UAMI_resourceID = $(az identity show --resource-group $env:AZ_RESOURCE_GROUP --name $env:AZ_UAMI --query id --output tsv)
$env:UAMI_SP_ID = $(az identity show --resource-group $env:AZ_RESOURCE_GROUP --name $env:AZ_UAMI --query principalId --output tsv)

# Get Registry Username & Password from keyvault
Write-Output "Get Registry Username & Password from keyvault"
$env:ACR_USERNAME = $(az keyvault secret show --vault-name $env:AZ_KEY_VAULT -n "${env:AZ_ACR_REGISTRY}-pull-usr" --query value -o tsv)
$env:ACR_PASSWORD = $(az keyvault secret show --vault-name $env:AZ_KEY_VAULT -n "${env:AZ_ACR_REGISTRY}-pull-pwd" --query value -o tsv)

Write-Output "Create Container Instances"
$env:CONTAINER_INSTANCE = "${env:resourceprefix}-pages"
Write-Output "Conatainer Instance Name: ${env:CONTAINER_INSTANCE}"
az container create --name $env:CONTAINER_INSTANCE --resource-group $env:AZ_RESOURCE_GROUP --image "${env:AZ_RESOURCE_GROUP}.azurecr.io/${env:resourceprefix}-pages" --registry-login-server "${env:AZ_RESOURCE_GROUP}.azurecr.io" --registry-username $env:ACR_USERNAME --registry-password $env:ACR_PASSWORD --cpu 1 --memory 1 --assign-identity $env:UAMI_resourceID
# --dns-name-label $env:CONTAINER_INSTANCE-$RANDOM --query ipAddress.fqdn

$env:CONTAINER_INSTANCE = "${env:resourceprefix}-articles"
Write-Output "Conatainer Instance Name: ${env:CONTAINER_INSTANCE}"
az container create --name $env:CONTAINER_INSTANCE --resource-group $env:AZ_RESOURCE_GROUP --image "${env:AZ_RESOURCE_GROUP}.azurecr.io/${env:resourceprefix}-articles" --registry-login-server "${env:AZ_RESOURCE_GROUP}.azurecr.io" --registry-username $env:ACR_USERNAME --registry-password $env:ACR_PASSWORD --cpu 1 --memory 1 --assign-identity $env:UAMI_resourceID

$env:CONTAINER_INSTANCE = "${env:resourceprefix}-seo"
Write-Output "Conatainer Instance Name: ${env:CONTAINER_INSTANCE}"
az container create --name $env:CONTAINER_INSTANCE --resource-group $env:AZ_RESOURCE_GROUP --image "${env:AZ_RESOURCE_GROUP}.azurecr.io/${env:resourceprefix}-seo" --registry-login-server "${env:AZ_RESOURCE_GROUP}.azurecr.io" --registry-username $env:ACR_USERNAME --registry-password $env:ACR_PASSWORD --cpu 1 --memory 1 --assign-identity $env:UAMI_resourceID

# Write-Output "Initialize Functions Folder"
# Set-Location ..
# func init "${env:AZ_RESOURCE_GROUP}-funcs" --powershell
# Set-Location ./func-config
# Copy-Item ./profile.ps1 "../${env:AZ_RESOURCE_GROUP}-funcs/" -Force
# Copy-Item ./requirements.psd1 "../${env:AZ_RESOURCE_GROUP}-funcs/" -Force
# Set-Location ..

# Write-Output "Create Functions"

# Set-Location "${env:AZ_RESOURCE_GROUP}-funcs"
# func new --name "${env:resourceprefix}-pages" --template "Timer trigger" --language "PowerShell"
# Set-Location ..
# Set-Location ./func-config
# Set-Location ./pages
# Copy-Item ./run.ps1 "../../${env:AZ_RESOURCE_GROUP}-funcs/${env:resourceprefix}-pages/" -Force
# Copy-Item ./function.json "../../${env:AZ_RESOURCE_GROUP}-funcs/${env:resourceprefix}-pages/" -Force
# Set-Location ../../

# Set-Location "${env:AZ_RESOURCE_GROUP}-funcs"
# func new --name "${env:resourceprefix}-articles" --template "Timer trigger" --language "PowerShell"
# Set-Location ..
# Set-Location ./func-config
# Set-Location ./articles
# Copy-Item ./run.ps1 "../../${env:AZ_RESOURCE_GROUP}-funcs/${env:resourceprefix}-articles/" -Force
# Copy-Item ./function.json "../../${env:AZ_RESOURCE_GROUP}-funcs/${env:resourceprefix}-articles/" -Force
# Set-Location ../../

# Set-Location "${env:AZ_RESOURCE_GROUP}-funcs"
# func new --name "${env:resourceprefix}-seo" --template "Timer trigger" --language "PowerShell"
# Set-Location ..
# Set-Location ./func-config
# Set-Location ./seo
# Copy-Item ./run.ps1 "../../${env:AZ_RESOURCE_GROUP}-funcs/${env:resourceprefix}-seo/" -Force
# Copy-Item ./function.json "../../${env:AZ_RESOURCE_GROUP}-funcs/${env:resourceprefix}-seo/" -Force
# Set-Location ../../

# Set-Location "${env:AZ_RESOURCE_GROUP}-funcs"
# func new --name "${env:resourceprefix}-seo-stop" --template "Timer trigger" --language "PowerShell"
# Set-Location ..
# Set-Location ./func-config
# Set-Location ./seo-stop
# Copy-Item ./run.ps1 "../../${env:AZ_RESOURCE_GROUP}-funcs/${env:resourceprefix}-seo-stop/" -Force
# Copy-Item ./function.json "../../${env:AZ_RESOURCE_GROUP}-funcs/${env:resourceprefix}-seo-stop/" -Force
# Set-Location ../../


# Write-Output "Deploy Azure Functions"
# Set-Location "${env:AZ_RESOURCE_GROUP}-funcs"
# func azure functionapp publish "${env:AZ_RESOURCE_GROUP}-func-app"