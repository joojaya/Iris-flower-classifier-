from flask import Flask, render_template, request, jsonify
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import numpy as np
import json
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# ===================== ML MODEL SETUP =====================
# Load and train the model
iris = load_iris()
X_iris = iris.data
y_iris = iris.target
class_names = list(iris.target_names)

# --- Extend Dataset with Synthetic Flower Data ---
def generate_flower_data(low, high, label, count=50):
    return np.random.uniform(low, high, (count, 4)), np.full(count, label)

# Specific data ranges for new flowers (simulated)
# Features: [sepal_length, sepal_width, petal_length, petal_width]
extra_flowers = {
    'Rose': [6.0, 9.0, 3.0, 5.0, 4.0, 7.0, 1.5, 3.0],      # Large & wide petals
    'Sunflower': [8.0, 15.0, 4.0, 8.0, 10.0, 20.0, 5.0, 10.0], # Huge flowers
    'Jasmine': [3.0, 5.0, 2.0, 4.0, 1.0, 2.0, 0.5, 1.5],  # Small & delicate
    'Daisy': [4.0, 6.0, 2.5, 4.5, 2.0, 4.0, 1.0, 2.0],   # Medium classic
    'Blue Pea': [3.5, 5.5, 2.0, 3.5, 2.5, 4.5, 0.8, 1.8] # Small vibrant
}

X_extra, y_extra = [], []
for i, (name, ranges) in enumerate(extra_flowers.items()):
    X_f, y_f = generate_flower_data(
        [ranges[0], ranges[2], ranges[4], ranges[6]], 
        [ranges[1], ranges[3], ranges[5], ranges[7]], 
        len(class_names) + i
    )
    X_extra.append(X_f)
    y_extra.append(y_f)
    class_names.append(name.lower())

X = np.vstack([X_iris] + X_extra)
y = np.concatenate([y_iris] + y_extra)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest model - deeper trees for more classes
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=15)
model.fit(X_train_scaled, y_train)

# Model metrics
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Updated feature names for response
feature_names = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

# Feature importance
feature_importance = dict(zip(iris.feature_names, model.feature_importances_))
feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))

# ===================== ROUTES =====================

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/api/model-info')
def model_info():
    """Get model information"""
    return jsonify({
        'model_type': 'Multi-Flower Classifier',
        'accuracy': float(accuracy),
        'features': feature_names,
        'classes': class_names,
        'test_samples': len(X_test),
        'feature_importance': feature_importance,
        'confusion_matrix': conf_matrix.tolist(),
        'n_estimators': 100,
        'max_depth': 15
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Make prediction on new data"""
    try:
        data = request.json
        
        # Extract features
        features = [
            float(data.get('sepal_length', 0)),
            float(data.get('sepal_width', 0)),
            float(data.get('petal_length', 0)),
            float(data.get('petal_width', 0))
        ]
        
        # Validate input
        if any(f <= 0 for f in features):
            return jsonify({'error': 'All values must be positive'}), 400
        
        # Scale features
        features_scaled = scaler.transform([features])
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        return jsonify({
            'prediction': class_names[prediction],
            'confidence': float(max(probabilities) * 100),
            'probabilities': {
                class_names[i]: float(prob * 100)
                for i, prob in enumerate(probabilities)
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/visualizations')
def visualizations():
    """Get data for visualizations"""
    return jsonify({
        'confusion_matrix': conf_matrix.tolist(),
        'classes': class_names,
        'feature_importance': feature_importance,
        'model_accuracy': float(accuracy)
    })

@app.route('/api/dataset-stats')
def dataset_stats():
    """Get dataset statistics"""
    stats = {}
    for i, feature in enumerate(feature_names):
        stats[feature] = {
            'min': float(np.min(X[:, i])),
            'max': float(np.max(X[:, i])),
            'mean': float(np.mean(X[:, i])),
            'std': float(np.std(X[:, i]))
        }
    return jsonify(stats)

@app.route('/api/sample-predictions')
def sample_predictions():
    """Get sample predictions from test set"""
    samples = []
    indices = np.random.choice(len(X_test), min(5, len(X_test)), replace=False)
    
    for idx in indices:
        sample = X_test[idx]
        sample_scaled = scaler.transform([sample])[0]
        pred = model.predict([sample_scaled])[0]
        actual = y_test[idx]
        
        samples.append({
            'features': {
                'sepal_length': float(sample[0]),
                'sepal_width': float(sample[1]),
                'petal_length': float(sample[2]),
                'petal_width': float(sample[3])
            },
            'predicted': class_names[pred],
            'actual': class_names[actual],
            'correct': bool(pred == actual)
        })
    
    return jsonify(samples)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
