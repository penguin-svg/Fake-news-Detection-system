# ============================================================================
# FLASK WEB APPLICATION - Fake News Detection System
# ============================================================================
# Deploy trained model on localhost with web interface
# File: app.py

from flask import Flask, render_template, request, jsonify
import pickle
import re
import numpy as np
from text_analyzer import TextAnalyzer
import os
from pathlib import Path

app = Flask(__name__)

# ============================================================================
# LOAD TRAINED MODEL AND VECTORIZER
# ============================================================================

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent

print("Loading trained model and vectorizer...")

try:
    model_path = BASE_DIR / 'fake_news_model.pkl'
    vectorizer_path = BASE_DIR / 'tfidf_vectorizer.pkl'
    metadata_path = BASE_DIR / 'model_metadata.pkl'
    
    # Verify files exist
    for file_path, file_name in [(model_path, 'fake_news_model.pkl'), 
                                   (vectorizer_path, 'tfidf_vectorizer.pkl'),
                                   (metadata_path, 'model_metadata.pkl')]:
        if not file_path.exists():
            raise FileNotFoundError(f"{file_name} not found at {file_path}")
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    with open(vectorizer_path, 'rb') as f:
        vectorizer = pickle.load(f)
    
    with open(metadata_path, 'rb') as f:
        metadata = pickle.load(f)
    
    print(f"✓ Model loaded: {metadata['model_name']}")
    print(f"✓ Accuracy: {metadata['accuracy']:.4f}")
    print(f"✓ F1-Score: {metadata['f1_score']:.4f}")
    
except FileNotFoundError as e:
    print(f"ERROR: {e}")
    exit(1)
except Exception as e:
    print(f"ERROR: Failed to load model files: {e}")
    exit(1)

# Initialize text analyzer with error handling
try:
    text_analyzer = TextAnalyzer()
except ImportError:
    print("ERROR: text_analyzer.py not found in project directory")
    exit(1)
except Exception as e:
    print(f"ERROR: Failed to initialize TextAnalyzer: {e}")
    exit(1)

# ============================================================================
# PREPROCESSING FUNCTION
# ============================================================================

def preprocess_text(text):
    """Same preprocessing as training"""
    if not text:
        return ""
    
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s\.\,\!\?]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# ============================================================================
# PREDICTION FUNCTION
# ============================================================================

def predict_news(headline, body=""):
    """
    Multimodal prediction combining ML model and heuristic analysis
    """
    # Combine headline and body
    content = f"{headline} {body}".strip()
    
    if not content:
        return {
            'error': 'Please provide some text to analyze'
        }
    
    # Preprocess
    cleaned = preprocess_text(content)
    
    # ML Model prediction
    vectorized = vectorizer.transform([cleaned])
    ml_probability = model.predict_proba(vectorized)[0]
    ml_prediction = model.predict(vectorized)[0]
    
    # ML score (probability of being fake)
    ml_fake_score = ml_probability[0]  # Probability of class 0 (fake)
    
    # Heuristic text analysis
    heuristic_score, heuristic_details = text_analyzer.analyze(headline, body)
    
    # Combined score (weighted average as per synopsis)
    # Weight: 60% ML model, 40% heuristic
    final_score = (ml_fake_score * 0.6) + (heuristic_score * 0.4)
    
    # Determine verdict
    if final_score > 0.7:
        verdict = "HIGH RISK - Likely Fake News"
        color = "danger"
        confidence = final_score * 100
    elif final_score > 0.4:
        verdict = "MODERATE RISK - Verify Sources"
        color = "warning"
        confidence = final_score * 100
    else:
        verdict = "LOW RISK - Appears Legitimate"
        color = "success"
        confidence = (1 - final_score) * 100
    
    result = {
        'verdict': verdict,
        'color': color,
        'confidence': round(confidence, 2),
        'final_score': round(final_score, 3),
        'ml_score': round(ml_fake_score, 3),
        'heuristic_score': round(heuristic_score, 3),
        'ml_confidence': {
            'fake': round(ml_probability[0] * 100, 2),
            'real': round(ml_probability[1] * 100, 2)
        },
        'heuristic_details': heuristic_details,
        'model_name': metadata['model_name']
    }
    
    return result

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def home():
    return render_template('index.html', metadata=metadata)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        headline = data.get('headline', '').strip()
        body = data.get('body', '').strip()
        
        if not headline:
            return jsonify({'error': 'Headline is required'}), 400
        
        result = predict_news(headline, body)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'online',
        'model': metadata['model_name'],
        'accuracy': metadata['accuracy'],
        'f1_score': metadata['f1_score']
    })

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 FAKE NEWS DETECTION SYSTEM")
    print("="*60)
    print(f"Model: {metadata['model_name']}")
    print(f"Training Accuracy: {metadata['accuracy']:.2%}")
    print(f"F1-Score: {metadata['f1_score']:.4f}")
    print("="*60)
    print("\n✓ Server starting on http://localhost:5000")
    print("✓ Press CTRL+C to stop\n")
    

if __name__ == "__main__":
    app.run()
