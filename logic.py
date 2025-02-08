from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# Dictionary mapping soil types to numerical values
SOIL_TYPE_MAP = {
    'clay': 0,
    'loamy': 1,
    'sandy': 2,
    'black': 3
}

# Simple crop recommendation logic
def predict_crop(temperature, humidity, rainfall, soil_type):
    crops = []
    
    # Temperature-based recommendations
    if 20 <= temperature <= 30:
        if soil_type == 'clay':
            crops.extend(['Rice', 'Wheat'])
        elif soil_type == 'loamy':
            crops.extend(['Cotton', 'Maize', 'Vegetables'])
        elif soil_type == 'sandy':
            crops.extend(['Groundnut', 'Potato'])
        elif soil_type == 'black':
            crops.extend(['Cotton', 'Sugarcane'])
    
    # Rainfall-based recommendations
    if rainfall > 200:
        crops.extend(['Rice', 'Sugarcane'])
    elif 100 <= rainfall <= 200:
        crops.extend(['Wheat', 'Maize'])
    else:
        crops.extend(['Millet', 'Groundnut'])
    
    # Humidity-based filtering
    if humidity > 80:
        crops = [crop for crop in crops if crop in ['Rice', 'Sugarcane']]
    elif 60 <= humidity <= 80:
        crops = [crop for crop in crops if crop in ['Cotton', 'Maize', 'Vegetables']]
    
    # Remove duplicates and return unique recommendations
    return list(set(crops))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        rainfall = float(data['rainfall'])
        soil_type = data['soilType']
        
        # Input validation
        if not (0 <= humidity <= 100):
            return jsonify({'error': 'Humidity must be between 0 and 100'}), 400
        if temperature < -20 or temperature > 50:
            return jsonify({'error': 'Temperature must be between -20°C and 50°C'}), 400
        if rainfall < 0:
            return jsonify({'error': 'Rainfall cannot be negative'}), 400
        
        recommended_crops = predict_crop(temperature, humidity, rainfall, soil_type)
        
        return jsonify({
            'success': True,
            'crops': recommended_crops,
            'message': 'Based on the provided conditions, the following crops are recommended:'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
