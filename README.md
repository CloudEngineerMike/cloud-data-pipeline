# Blob Questor

Azure native query function app. Outputs a blob file of all Azure data within the tenant.

![vecteezy_ugly-blobfish-logo-design_8214047](https://github.com/user-attachments/assets/d3afe596-905c-4668-830f-a83a0e01a83e)
<a href="https://www.vecteezy.com/free-vector/blobfish">Blobfish Vectors by Vecteezy</a>

## The Problem
Ever wanted to track analytics for all the resources in your Azure tenant? Say goodbye to guesswork and outdated inventory spreadsheets. Let Query Quest, query your entire tenant and provide detailed insights at your fingertips.

## The Solution
Query Quest is a service that provides an automated mechanism for querying all of Azure's data and pulling the JSON into a blob file. **Bonus**: Query Quest can now transport data between cloud platforms! Keep all your data in one place has never been easier.

## Architecture

![image003](https://github.com/user-attachments/assets/ec53a710-f557-42aa-b727-42c6708553f1)

#### Azure

1. Function Web App
1. Blob Service

#### AWS

1. CloudWatch Events
1. Secrets Manager
1. Lambda
1. S3

## Order of Operations

1. The Function Web App, is scheduled to run at the top of every hour. In it contains a PowerShell script that queries all of Azure's data, saving the results to a Blob file
1. CloudWatch Events schedules Lambda to run the script, twice a day
1. Lambda then authenticates with Secrets Manager to retrieve the Azure Account Key
1. With the Account Key, Lambda is then permitted to access the storage container in Azure (which contains the Blob)
1. During each invocation, Lambda temporarily saves the Blob file into its /tmp directory, followed by an immediate upload to S3. Placing the Blob within an S3 Bucket
