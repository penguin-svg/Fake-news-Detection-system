# Fake-news-Detection-system
# 🛡️ Fake News Detection System

A multimodal AI-powered web application that combines machine learning and linguistic analysis to detect fake news and misinformation in real-time.
## 📋 Overview

This project implements a sophisticated fake news detection system that analyzes news articles using a dual-approach methodology:

1. **Machine Learning Model**: TF-IDF vectorization with trained classifier (60% weight)
2. **Heuristic Text Analysis**: Linguistic pattern detection for sensationalism, emotional manipulation, and stylistic anomalies (40% weight)

The system provides detailed risk assessments with confidence scores and flags suspicious content patterns.

## ✨ Features

- **Multimodal Detection**: Combines ML predictions with rule-based heuristics
- **Real-time Analysis**: Instant results through intuitive web interface
- **Detailed Metrics**: Comprehensive breakdown of detection factors
- **Risk Classification**: Three-tier system (Low/Moderate/High risk)
- **Responsive UI**: Modern Bootstrap-based interface
- **REST API**: JSON endpoints for programmatic access

## 🏗️ Architecture

```
┌─────────────────┐
│   User Input    │
└────────┬────────┘
         │
    ┌────▼────┐
    │  Flask  │
    │  API    │
    └────┬────┘
         │
    ┌────▼─────────────────────┐
    │   Preprocessing Layer    │
    └────┬─────────────────────┘
         │
    ┌────▼────────┬─────────────┐
    │             │             │
┌───▼───┐    ┌───▼────┐   ┌───▼─────┐
│TF-IDF │    │ ML     │   │Heuristic│
│Vector │───►│ Model  │   │Analyzer │
└───────┘    └───┬────┘   └────┬────┘
                 │             │
            ┌────▼─────────────▼───┐
            │  Weighted Combiner   │
            │   (60% ML, 40% HR)   │
            └──────────┬───────────┘
                       │
                ┌──────▼────────┐
                │ Risk Verdict  │
                └───────────────┘
```

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/fake-news-detection.git
cd fake-news-detection
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Ensure model files exist**

Place the following trained model files in the project root:
- `fake_news_model.pkl` - Trained classifier
- `tfidf_vectorizer.pkl` - TF-IDF vectorizer
- `model_metadata.pkl` - Model metadata

## 🚀 Usage

### Running the Web Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Using the Web Interface

1. Navigate to `http://localhost:5000`
2. Enter a news headline (required)
3. Optionally add article body text
4. Click "Analyze Content"
5. Review the detailed risk assessment

### API Endpoints

#### Analyze Content
```bash
POST /analyze
Content-Type: application/json

{
  "headline": "Your news headline here",
  "body": "Optional article body text"
}
```

**Response:**
```json
{
  "verdict": "HIGH RISK - Likely Fake News",
  "confidence": 87.5,
  "final_score": 0.875,
  "ml_score": 0.920,
  "heuristic_score": 0.806,
  "ml_confidence": {
    "fake": 92.0,
    "real": 8.0
  },
  "heuristic_details": {
    "sensational_score": 0.867,
    "punctuation_score": 0.600,
    "caps_score": 0.750,
    "length_score": 0.900,
    "emotional_score": 0.500,
    "flags": [
      "⚠️ Sensationalist language detected",
      "⚠️ Excessive punctuation"
    ]
  }
}
```

#### Health Check
```bash
GET /api/health
```

## 🔍 Detection Methodology

### Machine Learning Component (60%)
- **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Preprocessing**: Lowercasing, URL removal, special character filtering
- **Output**: Probability distribution over fake/real classes

### Heuristic Analysis Component (40%)

The system analyzes five key linguistic features:

| Feature | Weight | Detection Criteria |
|---------|--------|-------------------|
| Sensationalism | 30% | Keywords like "SHOCKING", "EXPOSED", "BANNED" |
| Punctuation | 20% | Excessive !!!, ???, ellipses |
| Capitalization | 20% | SHOUTING (>60% uppercase) |
| Content Length | 15% | Suspiciously short articles (<50 words) |
| Emotional Language | 15% | Fear, anger, outrage triggers |

### Risk Scoring

```
Final Score = (ML_Score × 0.6) + (Heuristic_Score × 0.4)

Risk Levels:
- Score > 0.7: HIGH RISK - Likely Fake News
- Score 0.4-0.7: MODERATE RISK - Verify Sources
- Score < 0.4: LOW RISK - Appears Legitimate
```

## 📁 Project Structure

```
fake-news-detection/
│
├── app.py                      # Flask web application
├── text_analyzer.py            # Heuristic analysis engine
├── fake_news_model.pkl         # Trained ML model
├── tfidf_vectorizer.pkl        # TF-IDF vectorizer
├── model_metadata.pkl          # Model metrics
├── requirements.txt            # Python dependencies
│
├── templates/
│   └── index.html              # Web interface
│
└── README.md                   # This file
```

## 🧪 Testing

### Test the Text Analyzer
```bash
python text_analyzer.py
```

This runs built-in test cases demonstrating the heuristic analysis.

### Example Test Cases

**High Risk Example:**
```python
headline = "SHOCKING!!! THE TRUTH EXPOSED!!!"
body = "You won't believe what happened!!!"
# Expected: HIGH RISK (score > 0.7)
```

**Low Risk Example:**
```python
headline = "New Study Shows Climate Impact on Coastal Regions"
body = "A comprehensive study published today in Nature Climate Change..."
# Expected: LOW RISK (score < 0.4)
```

## 📊 Model Performance

The trained model achieves:
- **Accuracy**: Displayed on startup and in UI
- **F1-Score**: Displayed on startup and in UI
- **Training Data**: Various news datasets (specify your dataset)

## 🛠️ Dependencies

```
Flask==2.3.0
numpy==1.24.0
scikit-learn==1.3.0
```

Full list in `requirements.txt`

## 🔒 Limitations

- Model performance depends on training data quality and diversity
- Heuristics may produce false positives for legitimate sensational news
- Does not verify factual accuracy or check sources
- Limited to English language content
- Requires model retraining for optimal performance over time

## 🚧 Future Enhancements

- [ ] Source credibility verification
- [ ] Multi-language support
- [ ] Deep learning models (BERT, GPT)
- [ ] Browser extension
- [ ] Fact-checking database integration
- [ ] User feedback mechanism
- [ ] Historical accuracy tracking

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


**⚠️ Disclaimer**: This tool is for educational and research purposes. Always verify information through multiple reliable sources before drawing conclusions about news authenticity.
