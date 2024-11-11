# Input bindings are passed in via param block.

param($Timer)

 

# Get the current universal time in the default string format

$currentUTCtime = (Get-Date).ToUniversalTime()

 

# The 'IsPastDue' porperty is 'true' when the current function invocation is later than scheduled.

if ($Timer.IsPastDue) {

    Write-Host "PowerShell timer is running late!"

}

 

# Write an information log with the current time.

Write-Host "PowerShell timer trigger function ran! TIME: $currentUTCtime"

 

Connect-AzAccount -Identity

 

Set-AzContext -SubscriptionId "<enter-string>"

 

$pageSize = 700


#iteration count initialized to 0

$iteration = 0

$searchParams = @{

    #update query as needed

    Query = ""

    First = $pageSize

}


#loop until all records are queried

$results = do {

    $iteration += 1

    Write-Verbose "Iteration #$iteration" -Verbose

    #query Azure Graph

    $pageResults = Search-AzGraph @searchParams

    $searchParams.Skip += $pageResults.Count

    $pageResults

    #Out-File -FilePath .\test_$iteration.txt -InputObject $pageResults -Encoding ASCII -Width 200

} while ($pageResults.Count -eq $pageSize)

 

$json_results = $results | ConvertTo-Json -Depth 100

 

$fileName = "SavedFileJSON.json"


Out-File -FilePath $fileName -InputObject $json_results -Encoding UTF8NoBOM

 

(Get-Content $fileName -Raw).Replace("`r`n","`n") | Set-Content $fileName -Force

 

#Get key to storage account

$acctKey = (Get-AzStorageAccountKey -Name 'resourcegraphstorage' -ResourceGroupName resourcegraph).Value[0]

 

#Map to the reports BLOB context

$storageContext = New-AzStorageContext -StorageAccountName "resourcegraphstorage" -StorageAccountKey $acctKey

 

#Copy the file to the storage account

Set-AzStorageBlobContent -File $fileName -Container "resourcegraphcontainer" -BlobType "Block" -Context $storageContext -Verbose -Force
