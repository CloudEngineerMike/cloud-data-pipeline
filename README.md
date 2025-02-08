# Blob Questor  

**Seamlessly Query & Transport Your Azure Data** 🚀  

Blob Questor is an Azure-native **query function app** designed to **fetch, aggregate, and store** all Azure data across your tenant into a structured **Blob file**—ready for analytics, compliance, and cross-cloud portability!  

![Image](https://github.com/user-attachments/assets/46e7e7e0-099c-4402-877b-b2598f87a47b)  
<sub><a href="https://www.vecteezy.com/free-vector/blobfish">Blobfish Vectors by Vecteezy</a></sub>  



## The Problem  
Struggling to track **all** your Azure resources? Still relying on **outdated spreadsheets** for inventory and analytics? Managing cross-cloud data can be a nightmare without automation.  

### Enter **Blob Questor**  
Blob Questor takes the hassle out of tracking **your entire Azure environment** by **automating** data collection and storing it in a Blob file—**no manual effort required!**  

**Bonus Feature:** It’s **cloud-agnostic**! Blob Questor seamlessly transports your data between **Azure & AWS**, keeping your insights centralized across platforms.  



## Architecture  

Blob Questor integrates **Azure & AWS services** to fetch, store, and transfer your data securely.  

![Image](https://github.com/user-attachments/assets/dbfea1fb-2791-4ed5-989c-a17bcd84d415)

### **Azure Components**  
**Azure Function App** – Powers the scheduled query execution  
**Blob Storage Service** – Stores the extracted JSON data  
**Resource Graph** – Queries Big Data from Tenant

### **AWS Components**  
**CloudWatch Events** – Triggers automated executions  
**Secrets Manager** – Securely stores Azure credentials  
**Lambda Functions** – Facilitates data retrieval & transfer  
**S3 Buckets** – Stores Blob files for easy access  

### **Languages**  
- **PowerShell**
- **Python**

---

## How It Works  

Blob Questor runs on a **set schedule** to pull data from Azure and transport it securely to AWS:  

1️⃣ **Azure Function App** runs **hourly**, executing a PowerShell script that queries Azure's resources and saves the results in a Blob file.  
2️⃣ **CloudWatch Events** triggers an AWS Lambda function **twice a day** to initiate data transfer.  
3️⃣ **Lambda** authenticates with **Secrets Manager** to retrieve the Azure Storage Account Key.  
4️⃣ Using the retrieved key, **Lambda gains access** to the Azure Blob storage container.  
5️⃣ **Lambda temporarily stores** the Blob file in **/tmp**, then **uploads it to S3**—securing it for further processing.  

**Why It’s Awesome**  
✔ **Fully Automated** – No manual intervention needed  
✔ **Multi-Cloud Ready** – Works across Azure & AWS  
✔ **Secure & Scalable** – Uses encrypted credentials and cloud-native services  

---

## 🚀 Get Started  

**Step 1:** Clone the repo  
**Step 2:** Configure your Azure & AWS credentials  
**Step 3:** Deploy the function and schedule your queries  
**Step 4:** Let Blob Questor do the work!  

---

## 📌 Conclusion  

With **Blob Questor**, managing **large-scale Azure data** has never been easier. Say goodbye to **manual queries** and **scattered cloud data**—and hello to **automated insights** at your fingertips!  

**Try it today & simplify your cloud data management!** 
