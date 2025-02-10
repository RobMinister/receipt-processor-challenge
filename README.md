# Receipt Processor API

A web service that processes receipts and calculates reward points based on predefined rules.

## **Requirements**
- Docker installed on your system.
- Git Bash (Recommended for Windows users to run `curl` commands).

## **Running the Application with Docker**

### **1. Clone the Repository**
Open Git Bash and run:
```sh
git clone https://github.com/RobMinister/receipt-processor-challenge.git
cd receipt-processor
```

### **2. Build the Docker Image**
Run the following command:
```sh
docker build -t receipt-processor .
```

### **3. Run the Docker Container**
Start the container using:
```sh
docker run -p 5000:5000 receipt-processor
```

---

## **Executing API Requests**
After running the `docker run` command, **open a new Git Bash terminal** and use `curl` commands in the new terminal.

---

## **Testing the API with `curl` (Run in the New Bash Terminal)**

### **Submit a Receipt (Valid Request)**
```sh
curl -X POST "http://127.0.0.1:5000/receipts/process" -H "Content-Type: application/json" -d '{
"retailer": "M&M Corner Market",
"purchaseDate": "2022-03-20",
"purchaseTime": "14:33",
"items": [
{
"shortDescription": "Gatorade",
"price": "2.25"
},{
"shortDescription": "Gatorade",
"price": "2.25"
},{
"shortDescription": "Gatorade",
"price": "2.25"
},{
"shortDescription": "Gatorade",
"price": "2.25"
}
],
"total": "9.00"
}'
```
Expected response:
```json
{"id": "generated-id"}
```

### **Retrieve Points for a Receipt (Valid Request)**
Replace `generated-id` with the actual ID from the previous request:
```sh
curl -X GET "http://localhost:5000/receipts/generated-id/points"
```
Expected response:
```json
{"points": 109}
```

---

## **Testing Invalid Cases**

### **Submit a Receipt (Missing Required Fields - Invalid Request)**
```sh
curl -X POST "http://127.0.0.1:5000/receipts/process" -H "Content-Type: application/json" -d '{
"retailer": "Target",
"purchaseTime": "13:01",
"items": [
{
"shortDescription": "Mountain Dew 12PK",
"price": "6.49"
}
],
"total": "6.49"
}'
```
Expected response:
```json
"The receipt is invalid."
```

### **Retrieve Points for a Non-Existent Receipt ID (Invalid Request)**
```sh
curl -X GET "http://127.0.0.1:5000/receipts/121212121212jsnasjnajs/points"
```
Expected response:
```json
"No receipt found for that ID."
```

---

## **Stopping & Removing the Docker Container**
To stop and remove the running container, **use the same second Git Bash terminal** where you ran the curl commands or **a new Git Bash terminal** to run the below commands:
```sh
docker ps  # Get running container ID
docker stop <container_id>
docker rm <container_id>
```

---

Now you're all set! 🚀 Use **one Git Bash terminal** for running Docker and **a second Git Bash terminal** for sending `curl` requests and stopping Docker.
