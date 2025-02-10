from flask import Flask, request, jsonify
import uuid
import re
from datetime import datetime

app = Flask(__name__)

# Stores receipts in memory
receipts = {}

def is_valid_receipt(receipt):
    """ Validates receipt structure before processing """
    required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
    if not all(field in receipt for field in required_fields):
        return False
    
    if not isinstance(receipt["retailer"], str) or not receipt["retailer"].strip():
        return False

    try:
        datetime.strptime(receipt["purchaseDate"], "%Y-%m-%d")
        datetime.strptime(receipt["purchaseTime"], "%H:%M")
    except ValueError:
        return False

    if not isinstance(receipt["items"], list) or len(receipt["items"]) == 0:
        return False

    for item in receipt["items"]:
        if "shortDescription" not in item or "price" not in item:
            return False
        if not isinstance(item["shortDescription"], str) or not item["shortDescription"].strip():
            return False
        try:
            float(item["price"])
        except ValueError:
            return False

    try:
        float(receipt["total"])
    except ValueError:
        return False

    return True

def calculate_points(receipt):
    points = 0

    # 1. 1 point for every alphanumeric character in the retailer name
    retailer_name = receipt.get("retailer", "")
    points += sum(c.isalnum() for c in retailer_name)

    # 2. 50 points if the total is a round dollar amount with no cents
    total_amount = float(receipt.get("total", 0))
    if total_amount.is_integer():
        points += 50

    # 3. 25 points if the total is a multiple of 0.25
    if total_amount % 0.25 == 0:
        points += 25

    # 4. 5 points for every two items on the receipt
    items = receipt.get("items", [])
    points += (len(items) // 2) * 5

    # 5. If the trimmed length of the item description is a multiple of 3, 
    # multiply the price by 0.2 and round up to the nearest integer.
    # The result is the number of points earned
    for item in items:
        desc = item.get("shortDescription", "").strip()
        price = float(item.get("price", 0))
        if len(desc) % 3 == 0:
            points += int(price * 0.2 + 0.999)

    # 6. 6 points if the day in the purchase date is odd
    purchase_date = datetime.strptime(receipt.get("purchaseDate", ""), "%Y-%m-%d")
    if purchase_date.day % 2 == 1:
        points += 6

    # 7. 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = datetime.strptime(receipt.get("purchaseTime", ""), "%H:%M")
    if 14 <= purchase_time.hour < 16:
        points += 10

    return points

@app.route("/receipts/process", methods=["POST"])
def process_receipt():
    receipt = request.json

    # Validate the receipt
    if not is_valid_receipt(receipt):
        return "The receipt is invalid.\n", 400 # BadRequest Response

    # Generate a unique ID
    receipt_id = str(uuid.uuid4())

    # Store points in memory
    receipts[receipt_id] = calculate_points(receipt)

    return jsonify({"id": receipt_id})

@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def get_points(receipt_id):
    if receipt_id in receipts:
        return jsonify({"points": receipts[receipt_id]})
    
    return "No receipt found for that ID.\n", 404  # NotFound Response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
