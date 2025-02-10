# Running Locally
1. Install dependencies:

pip install -r requirements.txt

2. Start the Flask server:

python app.py

3. The API will be available at `http://127.0.0.1:5000/`

# Running with Docker
1. Build the Docker image:

docker build -t receipt-processor .

2. Run the container:

docker run -p 5000:5000 receipt-processor

3. The API will be available at `http://localhost:5000/`