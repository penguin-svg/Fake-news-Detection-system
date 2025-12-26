# ============================================================================
# TEXT ANALYZER MODULE - Linguistic Analysis Engine
# ============================================================================
# Based on the heuristic approach described in the synopsis
# File: text_analyzer.py

import re
from typing import Dict, Tuple

class TextAnalyzer:
    """
    Heuristic-based text analyzer that detects sensationalist patterns
    and stylistic anomalies commonly found in fake news.
    """
    
    def __init__(self):
        # Sensationalist keywords (heavily weighted)
        self.sensational_keywords = [
            'shocking', 'banned', 'exposed', 'truth', 'breaking',
            'urgent', 'alert', 'scandal', 'secret', 'revealed',
            'unbelievable', 'miracle', 'warning', 'danger', 'crisis',
            'leaked', 'exclusive', 'bombshell', 'proof', 'evidence'
        ]
        
        # Emotional trigger words
        self.emotional_words = [
            'fear', 'angry', 'hate', 'love', 'terrifying',
            'amazing', 'horrible', 'disgusting', 'outrageous'
        ]
    
    def analyze(self, headline: str, body: str = "") -> Tuple[float, Dict]:
        """
        Analyze text content and return risk score with detailed breakdown.
        
        Args:
            headline: Article headline/title
            body: Article body text (optional)
        
        Returns:
            Tuple of (risk_score, details_dict)
            - risk_score: Float between 0.0 (safe) and 1.0 (high risk)
            - details_dict: Dictionary with individual metric scores
        """
        text = f"{headline} {body}".strip()
        
        if not text:
            return 0.0, {"error": "Empty text"}
        
        # Calculate individual metrics
        sensational_score = self._check_sensationalism(text)
        punctuation_score = self._check_punctuation(text)
        caps_score = self._check_capitalization(text)
        length_score = self._check_length(text, headline)
        emotional_score = self._check_emotional_content(text)
        
        # Weighted combination (as per synopsis logic)
        weights = {
            'sensational': 0.30,
            'punctuation': 0.20,
            'caps': 0.20,
            'length': 0.15,
            'emotional': 0.15
        }
        
        risk_score = (
            sensational_score * weights['sensational'] +
            punctuation_score * weights['punctuation'] +
            caps_score * weights['caps'] +
            length_score * weights['length'] +
            emotional_score * weights['emotional']
        )
        
        # Clamp to [0, 1]
        risk_score = max(0.0, min(1.0, risk_score))
        
        details = {
            'sensational_score': round(sensational_score, 3),
            'punctuation_score': round(punctuation_score, 3),
            'caps_score': round(caps_score, 3),
            'length_score': round(length_score, 3),
            'emotional_score': round(emotional_score, 3),
            'overall_risk': round(risk_score, 3),
            'flags': self._generate_flags(sensational_score, punctuation_score, 
                                         caps_score, length_score)
        }
        
        return risk_score, details
    
    def _check_sensationalism(self, text: str) -> float:
        """Check for sensationalist keywords"""
        text_lower = text.lower()
        count = sum(1 for word in self.sensational_keywords if word in text_lower)
        
        # Normalize: more than 3 sensational words = high risk
        score = min(count / 3.0, 1.0)
        return score
    
    def _check_punctuation(self, text: str) -> float:
        """Check for excessive or unusual punctuation"""
        exclamations = text.count('!')
        questions = text.count('?')
        interrobangs = text.count('?!')
        ellipses = len(re.findall(r'\.{3,}', text))
        
        # Multiple exclamation marks
        multiple_exclaim = len(re.findall(r'!{2,}', text))
        
        total_anomalies = (exclamations / 3) + (questions / 3) + \
                         (interrobangs * 2) + (ellipses * 1.5) + \
                         (multiple_exclaim * 3)
        
        score = min(total_anomalies / 5.0, 1.0)
        return score
    
    def _check_capitalization(self, text: str) -> float:
        """Check for excessive capitalization (shouting)"""
        if not text:
            return 0.0
        
        letters = [c for c in text if c.isalpha()]
        if not letters:
            return 0.0
        
        caps_ratio = sum(1 for c in letters if c.isupper()) / len(letters)
        
        # As per synopsis: caps_ratio > 0.6 is high risk
        if caps_ratio > 0.6:
            score = 1.0
        elif caps_ratio > 0.4:
            score = 0.7
        elif caps_ratio > 0.2:
            score = 0.4
        else:
            score = caps_ratio * 2  # Normal capitalization
        
        return score
    
    def _check_length(self, text: str, headline: str) -> float:
        """Check if content is suspiciously short"""
        word_count = len(text.split())
        
        # As per synopsis: < 50 words is suspicious
        if word_count < 50:
            score = 1.0 - (word_count / 50.0)
        elif word_count < 100:
            score = 0.3
        else:
            score = 0.0
        
        return score
    
    def _check_emotional_content(self, text: str) -> float:
        """Check for emotional manipulation"""
        text_lower = text.lower()
        count = sum(1 for word in self.emotional_words if word in text_lower)
        
        score = min(count / 4.0, 1.0)
        return score
    
    def _generate_flags(self, sensational: float, punctuation: float, 
                       caps: float, length: float) -> list:
        """Generate human-readable warning flags"""
        flags = []
        
        if sensational > 0.5:
            flags.append("⚠️ Sensationalist language detected")
        if punctuation > 0.6:
            flags.append("⚠️ Excessive punctuation")
        if caps > 0.6:
            flags.append("⚠️ Excessive capitalization (shouting)")
        if length > 0.7:
            flags.append("⚠️ Suspiciously short content")
        
        return flags
    
    def get_verdict(self, risk_score: float) -> str:
        """Convert risk score to human-readable verdict"""
        if risk_score > 0.7:
            return "HIGH RISK"
        elif risk_score > 0.4:
            return "MODERATE RISK"
        else:
            return "LOW RISK"


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    analyzer = TextAnalyzer()
    
    # Test cases
    test_cases = [
        {
            'headline': 'SHOCKING!!! THE TRUTH EXPOSED!!!',
            'body': 'You won\'t believe what happened!!!'
        },
        {
            'headline': 'New Study Shows Climate Impact on Coastal Regions',
            'body': 'A comprehensive study published today in Nature Climate Change examines the long-term effects of rising sea levels on coastal ecosystems.'
        },
        {
            'headline': 'BREAKING: BANNED substance found!!!',
            'body': 'URGENT ALERT!'
        }
    ]
    
    print("="*60)
    print("TEXT ANALYZER - TEST RESULTS")
    print("="*60)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Headline: {case['headline']}")
        
        risk_score, details = analyzer.analyze(case['headline'], case['body'])
        
        print(f"\nRisk Score: {risk_score:.3f} ({analyzer.get_verdict(risk_score)})")
        print(f"Details: {details}")
        print("-"*60)