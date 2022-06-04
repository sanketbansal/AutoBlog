# Azure Functions profile.ps1
#
# This profile.ps1 will get executed every "cold start" of your Function App.
# "cold start" occurs when:
#
# * A Function App starts up for the very first time
# * A Function App starts up after being de-allocated due to inactivity
#
# You can define helper functions, run commands, or specify environment variables
# NOTE: any variables defined that are not environment variables will get reset after the first execution

# Authenticate with Azure PowerShell using MSI.
# Remove this if you are not planning on using MSI or Azure PowerShell.
Write-Host "PowerShell Executing profile.ps1"
if ($env:MSI_SECRET) {
    Disable-AzContextAutosave -Scope Process | Out-Null
    Connect-AzAccount -Identity
}

# Uncomment the next line to enable legacy AzureRm alias in Azure PowerShell.
# Enable-AzureRmAlias

# You can also define functions or aliases that can be referenced in any of your PowerShell functions.

if ($env:MSI_SECRET -and (Get-Module -ListAvailable Az.Accounts)) {
    Connect-AzAccount -Identity
}

function Get-AccessToken($tenantId) {
    $azureRmProfile = [Microsoft.Azure.Commands.Common.Authentication.Abstractions.AzureRmProfileProvider]::Instance.Profile;
    $profileClient = New-Object Microsoft.Azure.Commands.ResourceManager.Common.RMProfileClient($azureRmProfile);
    $profileClient.AcquireAccessToken($tenantId).AccessToken;
}

function Send-ContainerGroupCommand($resourceGroupName, $containerGroupName, $command) {
    $azContext = Get-AzContext
    $subscriptionId = $azContext.Subscription.Id
    $commandUri = "https://management.azure.com/subscriptions/$subscriptionId/resourceGroups/$resourceGroupName/providers/Microsoft.ContainerInstance/containerGroups/$containerGroupName/$command" + "?api-version=2018-10-01"
    $accessToken = Get-AccessToken $azContext.Tenant.TenantId
    $response = Invoke-RestMethod -Method Post -Uri $commandUri -Headers @{ Authorization="Bearer $accessToken" }
    $response
}

function Stop-ContainerGroup($resourceGroupName, $containerGroupName) {
    Send-ContainerGroupCommand $resourceGroupName $containerGroupName  "stop"
}

function Start-ContainerGroup($resourceGroupName, $containerGroupName) {
    Send-ContainerGroupCommand $resourceGroupName $containerGroupName "start"
}

function Restart-ContainerGroup($resourceGroupName, $containerGroupName) {
    Send-ContainerGroupCommand $resourceGroupName $containerGroupName "restart"
}