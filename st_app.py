import streamlit as st
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="🌸 Multi-Flower AI Classifier", page_icon="🌸", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .main {
        background-color: #0f0f1e;
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ===================== ML MODEL SETUP =====================
@st.cache_resource
def load_and_train_model():
    iris = load_iris()
    X_iris = iris.data
    y_iris = iris.target
    class_names = list(iris.target_names)

    # --- Add New Flowers (Synthetic) ---
    def generate_flower_data(low, high, label, count=100):
        return np.random.uniform(low, high, (count, 4)), np.full(count, label)

    extra_flowers = {
        'rose': [6.0, 9.0, 3.0, 5.0, 4.0, 7.0, 1.5, 3.0],      # Large & wide petals
        'sunflower': [8.0, 15.0, 4.0, 8.0, 10.0, 20.0, 5.0, 10.0], # Huge flowers
        'jasmine': [3.0, 5.0, 2.0, 4.0, 1.0, 2.0, 0.5, 1.5],  # Small & delicate
        'daisy': [4.0, 6.0, 2.5, 4.5, 2.0, 4.0, 1.0, 2.0],   # Medium classic
        'blue pea': [3.5, 5.5, 2.0, 3.5, 2.5, 4.5, 0.8, 1.8] # Small vibrant
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
        class_names.append(name)

    X = np.vstack([X_iris] + X_extra)
    y = np.concatenate([y_iris] + y_extra)

    # Train Model
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=15)
    model.fit(X_train, y_train)
    
    return model, scaler, class_names, iris.feature_names

# Load Model
model, scaler, class_names, feature_names = load_and_train_model()

# ===================== UI LAYOUT =====================
st.title("🌸 Multi-Flower AI Prediction Engine")
st.markdown("Enter measurements below to classify the flower species.")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("🎯 Input Measurements")
    with st.container():
        sepal_length = st.slider("Sepal Length (cm)", 2.0, 15.0, 5.8)
        sepal_width = st.slider("Sepal Width (cm)", 1.0, 8.0, 3.0)
        petal_length = st.slider("Petal Length (cm)", 1.0, 20.0, 4.3)
        petal_width = st.slider("Petal Width (cm)", 0.1, 10.0, 1.3)
        
        if st.button("🚀 Predict Flower Species"):
            input_data = scaler.transform([[sepal_length, sepal_width, petal_length, petal_width]])
            prediction = model.predict(input_data)[0]
            probs = model.predict_proba(input_data)[0]
            
            # Prediction Results
            st.session_state.prediction = class_names[prediction]
            st.session_state.probs = dict(zip(class_names, probs))
            st.session_state.timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

with col2:
    if 'prediction' in st.session_state:
        st.subheader("✨ Results")
        
        flower_icons = {
            'setosa': '🌸', 'versicolor': '🌺', 'virginica': '🌻',
            'rose': '🌹', 'sunflower': '🌻', 'jasmine': '🌼', 'daisy': '🌼', 'blue pea': '🫐'
        }
        
        icon = flower_icons.get(st.session_state.prediction, '🌸')
        st.write(f"### Predicted: {icon} {st.session_state.prediction.upper()}")
        st.info(f"Classified at: {st.session_state.timestamp}")
        
        # Proba Chart
        df_probs = pd.DataFrame(list(st.session_state.probs.items()), columns=['Species', 'Confidence'])
        fig = px.bar(df_probs, x='Confidence', y='Species', orientation='h', 
                     color='Confidence', color_continuous_scale='Plasma',
                     title="Confidence Distribution")
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Adjust the sliders and click Predict to see results!")

# ===================== ANALYTICS TAB =====================
st.divider()
st.subheader("📊 Model Insights")
tab1, tab2 = st.tabs(["⭐ Feature Importance", "🔍 About the Dataset"])

with tab1:
    importance = dict(zip(feature_names, model.feature_importances_))
    df_importance = pd.DataFrame(list(importance.items()), columns=['Feature', 'Score'])
    fig_imp = px.pie(df_importance, values='Score', names='Feature', hole=.3,
                     title="Which Feature Matters Most?")
    st.plotly_chart(fig_imp, use_container_width=True)

with tab2:
    st.write("This model classifies 8 species of flowers based on morphological measurements:")
    st.write("- **Standard Species**: Setosa, Versicolor, Virginica (Iris Dataset)")
    st.write("- **Added Species**: Rose, Sunflower, Jasmine, Daisy, Blue Pea Flower")
    st.markdown("**Core Tech**: Scikit-Learn | Random Forest Classifier (100 Trees)")
