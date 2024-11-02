from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained model
with open('sales_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    # Parse input JSON data
    data = request.get_json()
    # Convert input data to DataFrame
    df = pd.DataFrame([data])
    
    # Make prediction
    prediction = model.predict(df[['product_id', 'amount', 'quantity']])[0]
    
    return jsonify({'predicted_sales_volume': prediction})

if __name__ == '__main__':
    app.run(debug=True)
