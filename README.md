# 🌸 Iris ML Classifier - Machine Learning Web Application

A modern, production-ready machine learning web application built with Python Flask and advanced ML algorithms. This project demonstrates a complete ML pipeline with model training, prediction, and beautiful data visualization.

## ✨ Features

- **Machine Learning**: Random Forest Classifier trained on Iris dataset
- **Modern UI**: Beautiful gradient-based dark theme with animations
- **Real-time Predictions**: Make instant flower classification predictions
- **Model Analytics**: View accuracy, confusion matrix, and feature importance
- **Data Visualization**: Interactive charts with Chart.js
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **RESTful API**: Clean API endpoints for all functionality

## 📊 Project Structure

```
iris-ml-project/
├── app.py                      # Main Flask application
├── templates/
│   └── index.html             # Modern UI template
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone/Download the project**
```bash
cd iris-ml-project
```

2. **Create a virtual environment (optional but recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
```
http://localhost:5000
```

## 🎯 How to Use

### Making Predictions

1. Enter the flower measurements:
   - **Sepal Length**: Length of the sepal in cm
   - **Sepal Width**: Width of the sepal in cm
   - **Petal Length**: Length of the petal in cm
   - **Petal Width**: Width of the petal in cm

2. Click **"🚀 Predict Flower"** button

3. View instant predictions with confidence scores and probability distributions

### Viewing Model Information

- **Model Stats**: Accuracy, test samples, features
- **Feature Importance**: Which features matter most
- **Confusion Matrix**: Model performance visualization
- **Dataset Statistics**: Min, max, mean, std for each feature
- **Sample Predictions**: Real predictions from test data

## 🤖 ML Model Details

### Algorithm: Random Forest Classifier
- **Estimators**: 100 decision trees
- **Max Depth**: 10 levels
- **Accuracy**: ~98% on test set
- **Cross-validation**: Train/test split (80/20)

### Features
1. Sepal Length (cm)
2. Sepal Width (cm)
3. Petal Length (cm)
4. Petal Width (cm)

### Classes (Output)
- Setosa
- Versicolor
- Virginica

## 📡 API Endpoints

### GET `/`
Returns the main HTML page with the web interface.

### GET `/api/model-info`
Returns model information and statistics.

**Response:**
```json
{
  "model_type": "Random Forest Classifier",
  "accuracy": 0.983,
  "features": ["sepal length", "sepal width", "petal length", "petal width"],
  "classes": ["setosa", "versicolor", "virginica"],
  "test_samples": 30,
  "feature_importance": {
    "petal width (cm)": 0.45,
    "petal length (cm)": 0.42,
    "sepal length (cm)": 0.08,
    "sepal width (cm)": 0.05
  }
}
```

### POST `/api/predict`
Make a prediction for new flower data.

**Request:**
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Response:**
```json
{
  "prediction": "setosa",
  "confidence": 95.2,
  "probabilities": {
    "setosa": 95.2,
    "versicolor": 4.5,
    "virginica": 0.3
  },
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### GET `/api/visualizations`
Returns data for confusion matrix and visualizations.

### GET `/api/dataset-stats`
Returns statistics for each feature.

### GET `/api/sample-predictions`
Returns sample predictions from test set.

## 🎨 UI Features

### Design Highlights
- **Color Scheme**: Modern purple and pink gradient theme
- **Typography**: Clean, modern font stack
- **Animations**: Smooth transitions and hover effects
- **Responsiveness**: Mobile-first design approach
- **Dark Mode**: Eye-friendly dark theme throughout

### Components
- **Input Form**: Smooth number inputs with validation
- **Result Cards**: Beautiful result display with animations
- **Charts**: Interactive Chart.js visualizations
- **Statistics**: Clean stat boxes with icons
- **Tabs**: Organized information in tabbed sections

## 🔧 Customization

### Change Model Parameters

Edit `app.py`:
```python
model = RandomForestClassifier(
    n_estimators=150,      # Increase number of trees
    random_state=42,
    max_depth=15           # Increase depth
)
```

### Change Color Scheme

Edit CSS variables in `templates/index.html`:
```css
:root {
    --primary: #667eea;        /* Primary color */
    --secondary: #764ba2;      /* Secondary color */
    --accent: #f093fb;         /* Accent color */
    /* ... more colors ... */
}
```

## 📈 Performance Metrics

### Model Accuracy
The Random Forest model achieves approximately **98% accuracy** on the test set.

### Inference Speed
Predictions are made in < 10ms per request.

### Memory Usage
Model size: ~1-2 MB
Application footprint: ~50 MB (including dependencies)

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is busy, change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### CORS Issues
The app is configured to handle CORS. If you encounter issues, uncomment in `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

## 📚 Dataset Information

### Iris Dataset
- **Total Samples**: 150
- **Training Samples**: 120 (80%)
- **Test Samples**: 30 (20%)
- **Features**: 4
- **Classes**: 3

## 🌐 Deployment

### Deploy to Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Deploy to PythonAnywhere
1. Upload files to PythonAnywhere
2. Set up virtual environment
3. Configure web app settings
4. Reload

### Deploy to AWS/GCP
Use containerization:
```bash
docker build -t iris-ml .
docker run -p 5000:5000 iris-ml
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Improve documentation

## 📧 Contact

For questions or feedback, please reach out!

---

**Built with ❤️ using Flask, Scikit-learn, and modern web technologies**

Happy predicting! 🌸🚀
