# ai_simple.py - Simple AI for Phase 3
import nltk
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import uuid
from datetime import datetime

# Download NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('sentiment/vader_lexicon')
except:
    nltk.download('punkt', quiet=True)
    nltk.download('vader_lexicon', quiet=True)

class SimpleAI:
    def __init__(self):
        print("🔧 Initializing Simple AI Engine...")
        self.vader = SentimentIntensityAnalyzer()
        print("✅ AI Engine Ready!")
    
    def analyze(self, text, language='en'):
        """Analyze text for sentiment, emotion, and threat"""
        if not text or not text.strip():
            return self._get_empty_result()
        
        text_lower = text.lower()
        
        # 1. Sentiment Analysis
        sentiment = self._get_sentiment(text)
        
        # 2. Emotion Detection
        emotion = self._get_emotion(text_lower)
        
        # 3. Threat Analysis
        threat = self._get_threat(text_lower, sentiment['type'])
        
        # 4. Create result
        result = {
            'analysis_id': f"AI-{uuid.uuid4().hex[:8].upper()}",
            'text': text,
            'language': language,
            'sentiment': sentiment['type'],
            'sentiment_score': sentiment['score'],
            'sentiment_details': {
                'polarity': sentiment['polarity'],
                'subjectivity': sentiment['subjectivity'],
                'vader_score': sentiment['vader']
            },
            'emotion': emotion['type'],
            'emotion_score': emotion['score'],
            'threat_level': threat['level'],
            'threat_score': threat['score'],
            'categories': threat['categories'],
            'keywords_found': threat['keywords'],
            'warnings': threat['warnings'],
            'timestamp': datetime.now().isoformat(),
            'model': 'simple_ai_v1',
            'is_real_ai': True
        }
        
        print(f"📊 Analysis: {threat['level'].upper()} threat | {sentiment['type']} | {emotion['type']}")
        return result
    
    def _get_sentiment(self, text):
        """Get sentiment using TextBlob and VADER"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        vader_score = self.vader.polarity_scores(text)['compound']
        
        # Determine sentiment type
        if polarity > 0.3:
            sentiment_type = "positive"
            score = (polarity + 0.5) / 2
        elif polarity < -0.3:
            sentiment_type = "negative"
            score = (abs(polarity) + 0.5) / 2
        else:
            sentiment_type = "neutral"
            score = 0.5
        
        return {
            'type': sentiment_type,
            'score': round(score, 3),
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'vader': round(vader_score, 3)
        }
    
    def _get_emotion(self, text_lower):
        """Detect emotion based on keywords"""
        emotions = {
            'anger': ['angry', 'mad', 'hate', 'rage', 'furious', 'kill', 'murder'],
            'fear': ['scared', 'afraid', 'fear', 'terrified', 'panic', 'help', 'danger'],
            'joy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'love', 'good'],
            'sadness': ['sad', 'depressed', 'cry', 'unhappy', 'lonely', 'alone'],
            'neutral': ['ok', 'fine', 'normal', 'alright', 'hello', 'hi']
        }
        
        scores = {}
        for emotion, keywords in emotions.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            scores[emotion] = count * 0.2
        
        # Get dominant emotion
        dominant = max(scores.items(), key=lambda x: x[1])
        
        if dominant[1] > 0:
            return {
                'type': dominant[0],
                'score': round(min(dominant[1], 0.9), 3)
            }
        else:
            return {
                'type': 'neutral',
                'score': 0.5
            }
    
    def _get_threat(self, text_lower, sentiment_type):
        """Analyze threat level"""
        threat_score = 0.0
        categories = []
        keywords = []
        warnings = []
        
        # High threat keywords
        high_threat = ['kill', 'murder', 'suicide', 'bomb', 'shoot', 'attack', 'rape', 'terrorist']
        for word in high_threat:
            if word in text_lower:
                threat_score += 0.15
                keywords.append(word)
        
        # Medium threat keywords
        medium_threat = ['hurt', 'harm', 'beat', 'fight', 'destroy', 'revenge', 'threat']
        for word in medium_threat:
            if word in text_lower:
                threat_score += 0.1
                keywords.append(word)
        
        # Emergency phrases
        if any(phrase in text_lower for phrase in ['help me', 'emergency', '911', 'save me']):
            threat_score += 0.3
            categories.append('emergency')
            warnings.append('🚨 EMERGENCY DETECTED')
        
        # Self-harm indicators
        if any(phrase in text_lower for phrase in ['end my life', 'kill myself', 'want to die']):
            threat_score += 0.4
            categories.append('self_harm')
            warnings.append('⚠️ SELF-HARM INDICATORS')
        
        # Violence indicators
        if any(phrase in text_lower for phrase in ['kill you', 'hurt you', 'attack you']):
            threat_score += 0.35
            categories.append('violence')
            warnings.append('⚠️ VIOLENT INTENT')
        
        # Sentiment effect
        if sentiment_type == 'negative':
            threat_score += 0.2
        
        # Cap score
        threat_score = min(threat_score, 1.0)
        
        # Determine level
        if threat_score >= 0.7:
            level = 'high'
            if not warnings:
                warnings.append('⚠️ HIGH THREAT DETECTED')
        elif threat_score >= 0.4:
            level = 'medium'
            if not warnings:
                warnings.append('⚠️ MEDIUM THREAT LEVEL')
        else:
            level = 'low'
            if not warnings:
                warnings.append('✅ LOW THREAT LEVEL')
        
        # Add category if none
        if not categories:
            categories.append('normal' if level == 'low' else 'suspicious')
        
        return {
            'level': level,
            'score': round(threat_score, 3),
            'categories': categories,
            'keywords': keywords,
            'warnings': warnings
        }
    
    def _get_empty_result(self):
        """Return empty analysis result"""
        return {
            'analysis_id': f"AI-{uuid.uuid4().hex[:8].upper()}",
            'text': '',
            'sentiment': 'neutral',
            'sentiment_score': 0.5,
            'emotion': 'neutral',
            'emotion_score': 0.5,
            'threat_level': 'low',
            'threat_score': 0.1,
            'categories': ['no_input'],
            'warnings': ['No text provided'],
            'is_real_ai': True,
            'timestamp': datetime.now().isoformat()
        }

# Create global instance
ai_engine = SimpleAI()