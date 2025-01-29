# Input bindings are passed in via param block.
param($Timer)

# Get the current universal time in the default string format
$currentUTCtime = (Get-Date).ToUniversalTime()

# Check if the timer is past due
if ($Timer.IsPastDue) {
    Write-Host "PowerShell timer is running late!"
}

# Log the execution time
Write-Host "PowerShell timer trigger function ran! TIME: $currentUTCtime"

# Authenticate to Azure using managed identity
Connect-AzAccount -IdentityNAME

# Set Azure subscription context
Set-AzContext -SubscriptionId "<enter-string>"

# Define the page size for querying Azure Resource Graph
$pageSize = 700

# Initialize iteration count
$iteration = 0

# Define search parameters
$searchParams = @{
    Query = ""     # Update query as needed
    First = $pageSize
}

# Query loop to fetch all records
$results = do {
    $iteration += 1
    Write-Verbose "Iteration #$iteration" -Verbose

    # Execute the Azure Resource Graph query
    $pageResults = Search-AzGraph @searchParams

    # Update skip parameter for pagination
    $searchParams.Skip += $pageResults.Count

    # Output results
    $pageResults

} while ($pageResults.Count -eq $pageSize)

# Convert results to JSON format
$json_results = $results | ConvertTo-Json -Depth 100

# Define output file name
$fileName = "JSON.json"

# Save JSON results to a file
Out-File -FilePath $fileName -InputObject $json_results -Encoding UTF8NoBOM

# Normalize line endings in the JSON file
(Get-Content $fileName -Raw).Replace("`r`n", "`n") | Set-Content $fileName -Force

# Retrieve storage account key
$acctKey = (Get-AzStorageAccountKey -Name 'STORAGE-ACCOUNT' -ResourceGroupName 'RG-NAME').Value[0]

# Create storage context for blob upload
$storageContext = New-AzStorageContext -StorageAccountName "STORAGE-ACCOUNT" -StorageAccountKey $acctKey

# Upload the JSON file to Azure Storage Blob
Set-AzStorageBlobContent -File $fileName -Container "RG-CONTAINER" -BlobType "Block" -Context $storageContext -Verbose -Force
