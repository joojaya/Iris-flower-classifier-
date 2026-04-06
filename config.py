"""
Configuration settings for Iris ML Classifier
"""

import os
from datetime import timedelta

# Flask Configuration
DEBUG = os.getenv('DEBUG', True)
TESTING = os.getenv('TESTING', False)
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# Server Configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# ML Model Configuration
MODEL_TYPE = 'RandomForest'
N_ESTIMATORS = 100
MAX_DEPTH = 10
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Session Configuration
PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# CORS Configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
