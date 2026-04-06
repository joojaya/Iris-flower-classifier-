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
X = iris.data
y = iris.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
model.fit(X_train_scaled, y_train)

# Model metrics
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

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
        'model_type': 'Random Forest Classifier',
        'accuracy': float(accuracy),
        'features': list(iris.feature_names),
        'classes': list(iris.target_names),
        'test_samples': len(X_test),
        'feature_importance': feature_importance,
        'confusion_matrix': conf_matrix.tolist(),
        'n_estimators': 100,
        'max_depth': 10
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
            'prediction': iris.target_names[prediction],
            'confidence': float(max(probabilities) * 100),
            'probabilities': {
                iris.target_names[i]: float(prob * 100)
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
        'classes': list(iris.target_names),
        'feature_importance': feature_importance,
        'model_accuracy': float(accuracy)
    })

@app.route('/api/dataset-stats')
def dataset_stats():
    """Get dataset statistics"""
    stats = {}
    for i, feature in enumerate(iris.feature_names):
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
            'predicted': iris.target_names[pred],
            'actual': iris.target_names[actual],
            'correct': pred == actual
        })
    
    return jsonify(samples)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
