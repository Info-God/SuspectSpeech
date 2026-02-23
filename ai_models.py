# ai_models.py - IMPROVED THREAT DETECTION
import nltk
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import uuid
from datetime import datetime
import re

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('sentiment/vader_lexicon')
except:
    nltk.download('punkt', quiet=True)
    nltk.download('vader_lexicon', quiet=True)

class SimpleAIPipeline:
    def __init__(self):
        print("🔧 Initializing Simple AI Engine...")
        self.vader = SentimentIntensityAnalyzer()
        
        # EXPANDED THREAT KEYWORDS
        self.threat_patterns = {
            'critical': [
                r'kill.*you', r'murder.*you', r'kill.*u', r'murder.*u',
                r'shoot.*you', r'stab.*you', r'bomb.*you', r'die.*now',
                r'going to kill', r'will kill', r'gonna kill', r'want.*kill',
                r'kill.*yourself', r'kill.*myself', r'suicide'
            ],
            'high': [
                r'kill', r'murder', r'die', r'dead', r'death',
                r'hurt.*you', r'harm.*you', r'attack.*you',
                r'beat.*you', r'fight.*you', r'destroy.*you',
                r'threat', r'danger', r'violent'
            ],
            'medium': [
                r'hate', r'angry', r'mad', r'furious', r'rage',
                r'scared', r'afraid', r'fear', r'terrified',
                r'help', r'emergency', r'dangerous'
            ]
        }
        
        # EMOTION KEYWORDS (expanded)
        self.emotion_patterns = {
            'anger': ['angry', 'mad', 'hate', 'furious', 'rage', 'pissed', 'annoyed', 'frustrated'],
            'fear': ['scared', 'afraid', 'terrified', 'fear', 'panic', 'worried', 'anxious', 'nervous'],
            'sadness': ['sad', 'depressed', 'unhappy', 'crying', 'lonely', 'heartbroken', 'miserable'],
            'joy': ['happy', 'excited', 'great', 'wonderful', 'awesome', 'amazing', 'fantastic', 'love'],
            'neutral': ['ok', 'fine', 'alright', 'maybe', 'perhaps', 'well']
        }
        
        print("✅ AI Engine Ready!")
    
    def analyze_text(self, text, language='en'):
        """Analyze text for sentiment, emotion, and threat"""
        if not text or not text.strip():
            return self._get_empty_result()
        
        text_lower = text.lower().strip()
        
        # 1. Threat Analysis (do this first)
        threat_result = self._analyze_threat(text_lower)
        
        # 2. Sentiment Analysis
        sentiment_result = self._analyze_sentiment(text)
        
        # 3. Emotion Detection
        emotion_result = self._analyze_emotion(text_lower)
        
        # 4. Override sentiment based on threat if needed
        if threat_result['level'] in ['high', 'critical']:
            sentiment_result['type'] = 'negative'
            sentiment_result['score'] = max(sentiment_result['score'], 0.8)
        
        # Create result
        result = {
            'id': f"AI-{uuid.uuid4().hex[:8].upper()}",
            'text': text,
            'language': language,
            'sentiment': sentiment_result['type'],
            'sentiment_score': round(sentiment_result['score'], 3),
            'emotion': emotion_result['type'],
            'emotion_score': round(emotion_result['score'], 3),
            'threat_level': threat_result['level'],
            'threat_score': round(threat_result['score'], 3),
            'categories': threat_result['categories'],
            'keywords_found': threat_result['keywords'],
            'warnings': threat_result['warnings'],
            'timestamp': datetime.now().isoformat(),
            'model': 'improved_ai_v2',
            'is_real_ai': True
        }
        
        print(f"📊 Analysis: {threat_result['level'].upper()} threat | {sentiment_result['type']} | {emotion_result['type']}")
        return result
    
    def _analyze_threat(self, text):
        """Enhanced threat analysis with pattern matching"""
        threat_score = 0.0
        keywords = []
        categories = []
        warnings = []
        
        # Check for critical patterns first (highest weight)
        for pattern in self.threat_patterns['critical']:
            if re.search(pattern, text):
                threat_score += 0.5
                keywords.append(pattern.replace(r'\W', ''))
                categories.append('critical_threat')
                warnings.append('🚨 CRITICAL THREAT DETECTED')
                break
        
        # Check high threat patterns
        for pattern in self.threat_patterns['high']:
            if re.search(pattern, text):
                threat_score += 0.3
                keywords.append(pattern.replace(r'\W', ''))
                categories.append('high_threat')
                if not warnings:
                    warnings.append('⚠️ HIGH THREAT DETECTED')
                break
        
        # Check medium threat patterns
        for pattern in self.threat_patterns['medium']:
            if re.search(pattern, text):
                threat_score += 0.2
                keywords.append(pattern.replace(r'\W', ''))
                categories.append('medium_threat')
                if not warnings and threat_score < 0.5:
                    warnings.append('⚠️ MEDIUM THREAT LEVEL')
                break
        
        # Check for specific dangerous phrases
        dangerous_phrases = [
            ('kill you', 0.4), ('kill u', 0.4), ('murder you', 0.4),
            ('shoot you', 0.4), ('stab you', 0.4), ('die now', 0.3),
            ('going to kill', 0.4), ('will kill', 0.4), ('gonna kill', 0.4),
            ('end your life', 0.4), ('end my life', 0.4), ('want to die', 0.3),
            ('help me', 0.2), ('save me', 0.2), ('emergency', 0.2)
        ]
        
        for phrase, weight in dangerous_phrases:
            if phrase in text:
                threat_score += weight
                keywords.append(phrase)
                categories.append('dangerous_phrase')
        
        # Check for violence indicators
        violence_words = ['kill', 'murder', 'shoot', 'stab', 'beat', 'hurt', 'attack', 'destroy']
        violence_count = sum(1 for word in violence_words if word in text)
        if violence_count > 0:
            threat_score += violence_count * 0.1
            categories.append('violence')
        
        # Cap threat score at 1.0
        threat_score = min(threat_score, 1.0)
        
        # Determine threat level
        if threat_score >= 0.7:
            level = 'high'
            if not warnings:
                warnings.append('⚠️ HIGH THREAT DETECTED')
        elif threat_score >= 0.4:
            level = 'medium'
            if not warnings:
                warnings.append('⚠️ MEDIUM THREAT DETECTED')
        else:
            level = 'low'
            if not warnings:
                warnings.append('✅ LOW THREAT LEVEL')
        
        # Ensure "kill you" is always at least medium-high
        if 'kill' in text and ('you' in text or 'u' in text):
            if threat_score < 0.5:
                threat_score = 0.6
                level = 'medium'
                categories.append('direct_threat')
                warnings = ['⚠️ DIRECT THREAT DETECTED']
        
        # Remove duplicates from categories
        categories = list(set(categories))
        if not categories:
            categories.append('normal')
        
        return {
            'level': level,
            'score': threat_score,
            'categories': categories[:3],  # Limit to top 3 categories
            'keywords': list(set(keywords))[:5],  # Limit to top 5 keywords
            'warnings': warnings
        }
    
    def _analyze_sentiment(self, text):
        """Enhanced sentiment analysis"""
        # VADER sentiment
        vader_scores = self.vader.polarity_scores(text)
        compound = vader_scores['compound']
        
        # TextBlob sentiment
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        # Combine both for better accuracy
        combined_score = (compound + polarity) / 2
        
        # Determine sentiment type
        if combined_score > 0.3:
            sentiment_type = 'positive'
            score = combined_score
        elif combined_score < -0.3:
            sentiment_type = 'negative'
            score = abs(combined_score)
        else:
            sentiment_type = 'neutral'
            score = 0.5
        
        return {
            'type': sentiment_type,
            'score': min(score, 1.0),
            'vader': vader_scores,
            'polarity': polarity
        }
    
    def _analyze_emotion(self, text):
        """Enhanced emotion detection"""
        emotion_scores = {}
        
        # Calculate scores for each emotion
        for emotion, keywords in self.emotion_patterns.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    # Weight based on keyword length and position
                    score += 0.2
                    # Bonus for exact matches
                    if re.search(r'\b' + re.escape(keyword) + r'\b', text):
                        score += 0.1
            emotion_scores[emotion] = min(score, 1.0)
        
        # Get dominant emotion
        dominant = max(emotion_scores.items(), key=lambda x: x[1])
        
        # Override for threat-related text
        if 'kill' in text or 'murder' in text:
            if 'you' in text or 'u' in text:
                return {'type': 'anger', 'score': 0.9}
        
        if dominant[1] > 0:
            return {
                'type': dominant[0],
                'score': min(dominant[1] + 0.2, 1.0)  # Boost dominant emotion
            }
        else:
            return {'type': 'neutral', 'score': 0.5}
    
    def _get_empty_result(self):
        """Return empty analysis result"""
        return {
            'id': f"AI-{uuid.uuid4().hex[:8].upper()}",
            'text': '',
            'sentiment': 'neutral',
            'sentiment_score': 0.5,
            'emotion': 'neutral',
            'emotion_score': 0.5,
            'threat_level': 'low',
            'threat_score': 0.1,
            'categories': ['no_input'],
            'keywords_found': [],
            'warnings': ['No text provided'],
            'is_real_ai': True,
            'timestamp': datetime.now().isoformat()
        }

# Create global instance
ai_pipeline = SimpleAIPipeline()