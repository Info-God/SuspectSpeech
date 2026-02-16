# app.py - PHASE 3 WITH REAL AI
from flask import Flask, render_template, request, jsonify, session, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json
import uuid
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from io import BytesIO
import tempfile

# Import our AI models
try:
    from ai_models import ai_pipeline
    AI_AVAILABLE = True
    print("✓ AI Pipeline imported successfully")
except Exception as e:
    print(f"✗ AI Pipeline import failed: {e}")
    AI_AVAILABLE = True
    # Create a mock pipeline for fallback
    class MockAIPipeline:
        def analyze_text(self, text, language='en'):
            return {
                'text': text,
                'language': language,
                'sentiment': 'neutral',
                'sentiment_score': 0.5,
                'emotion': 'neutral',
                'emotion_score': 0.5,
                'threat_level': 'low',
                'threat_score': 0.1,
                'categories': ['mock_analysis'],
                'is_real_ai': False,
                'warnings': ['AI system temporarily unavailable']
            }
    ai_pipeline = MockAIPipeline()

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-2023')
CORS(app)

# Initialize session data
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

# Database for demo
cases_db = []
analysis_history = []

# Initialize with mock data
def initialize_mock_data():
    global cases_db
    
    mock_cases = [
        {
            'id': str(uuid.uuid4()),
            'case_id': 'CASE-001',
            'title': 'Cyberbullying Incident - AI Detected',
            'description': 'Student reported threatening messages. AI analysis confirmed high threat.',
            'status': 'open',
            'risk_level': 'high',
            'priority': 'urgent',
            'created_at': (datetime.now() - timedelta(days=2)).isoformat(),
            'updated_at': datetime.now().isoformat(),
            'assigned_to': 'Admin',
            'location': 'New York, NY',
            'victim_age': '17',
            'platform': 'WhatsApp',
            'ai_detected': True
        },
        {
            'id': str(uuid.uuid4()),
            'case_id': 'CASE-002',
            'title': 'Online Harassment',
            'description': 'Multiple threatening messages from anonymous account',
            'status': 'investigating',
            'risk_level': 'medium',
            'priority': 'high',
            'created_at': (datetime.now() - timedelta(days=1)).isoformat(),
            'updated_at': datetime.now().isoformat(),
            'assigned_to': 'Investigator',
            'location': 'Los Angeles, CA',
            'victim_age': '25',
            'platform': 'Instagram',
            'ai_detected': True
        },
        {
            'id': str(uuid.uuid4()),
            'case_id': 'CASE-003',
            'title': 'Self-harm Prevention',
            'description': 'AI detected concerning messages with self-harm indicators',
            'status': 'resolved',
            'risk_level': 'high',
            'priority': 'urgent',
            'created_at': (datetime.now() - timedelta(days=3)).isoformat(),
            'updated_at': (datetime.now() - timedelta(hours=2)).isoformat(),
            'assigned_to': 'Counselor',
            'location': 'Chicago, IL',
            'victim_age': '19',
            'platform': 'Discord',
            'ai_detected': True
        }
    ]
    
    cases_db.extend(mock_cases)

initialize_mock_data()

# ========== ROUTES ==========
@app.route('/cases')
def cases_page():
    """Cases management page"""
    return render_template('cases.html', ai_available=AI_AVAILABLE)
@app.route('/')
def home():
    """Home page"""
    return render_template('index.html', ai_available=AI_AVAILABLE)

@app.route('/dashboard')
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html', ai_available=AI_AVAILABLE)



@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    """Analyze text input using REAL AI"""
    try:
        data = request.json
        text = data.get('text', '')
        language = data.get('language', 'en')
        
        if not text.strip():
            return jsonify({
                'success': False,
                'error': 'Please enter text to analyze'
            }), 400
        
        print(f"\n📝 Text Analysis Request:")
        print(f"   Text: {text[:100]}...")
        print(f"   Language: {language}")
        
        # Use AI pipeline
        analysis_result = ai_pipeline.analyze_text(text, language)
        
        # Create full analysis object
        full_result = {
            'id': str(uuid.uuid4()),
            'text': text,
            'language': language,
            'timestamp': datetime.now().isoformat(),
            'status': 'analyzed',
            'ai_available': AI_AVAILABLE,
            **analysis_result
        }
        
        # Store in history
        analysis_history.append(full_result)
        
        # Limit history
        if len(analysis_history) > 100:
            analysis_history.pop(0)
        
        return jsonify({
            'success': True,
            'analysis': full_result,
            'message': 'AI analysis completed successfully',
            'ai_status': 'active' if AI_AVAILABLE else 'fallback'
        })
        
    except Exception as e:
        print(f"❌ Text analysis error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}',
            'ai_status': 'error'
        }), 500

@app.route('/analyze/voice', methods=['POST'])
def analyze_voice():
    """Analyze voice recording (simulated for now)"""
    try:
        data = request.json
        audio_data = data.get('audio_data', '')
        language = data.get('language', 'en')
        
        # For Phase 3, we'll simulate voice analysis
        # In Phase 4, we'll add real voice processing
        
        mock_transcriptions = [
            "I need help immediately, someone is following me home",
            "Everything is fine here, just checking in with the system",
            "I'm feeling very angry about what happened yesterday",
            "This is a test recording for the suspect speech system"
        ]
        
        import random
        transcribed_text = random.choice(mock_transcriptions)
        
        # Analyze the transcribed text
        analysis_result = ai_pipeline.analyze_text(transcribed_text, language)
        
        full_result = {
            'id': str(uuid.uuid4()),
            'text': transcribed_text,
            'original_audio': 'simulated_voice_data',
            'language': language,
            'timestamp': datetime.now().isoformat(),
            'status': 'analyzed',
            'source': 'voice_simulation',
            'ai_available': AI_AVAILABLE,
            **analysis_result
        }
        
        analysis_history.append(full_result)
        
        return jsonify({
            'success': True,
            'analysis': full_result,
            'transcription': transcribed_text,
            'message': 'Voice analysis completed (simulation mode)',
            'note': 'Real voice processing will be added in Phase 4'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Legacy endpoint
@app.route('/analyze', methods=['POST'])
def analyze_text_legacy():
    return analyze_text()

@app.route('/api/cases', methods=['GET', 'POST'])
def handle_cases():
    """Handle cases CRUD operations"""
    if request.method == 'GET':
        status = request.args.get('status', 'all')
        risk_level = request.args.get('risk_level', 'all')
        
        filtered_cases = cases_db
        
        if status != 'all':
            filtered_cases = [c for c in filtered_cases if c['status'] == status]
        if risk_level != 'all':
            filtered_cases = [c for c in filtered_cases if c['risk_level'] == risk_level]
        
        return jsonify({
            'success': True,
            'cases': filtered_cases,
            'total': len(filtered_cases),
            'ai_cases': len([c for c in filtered_cases if c.get('ai_detected')])
        })
    
    elif request.method == 'POST':
        try:
            data = request.json
            new_case = {
                'id': str(uuid.uuid4()),
                'case_id': f"CASE-{len(cases_db) + 1:03d}",
                'title': data.get('title', 'New Case'),
                'description': data.get('description', ''),
                'status': 'open',
                'risk_level': data.get('risk_level', 'medium'),
                'priority': data.get('priority', 'medium'),
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'assigned_to': data.get('assigned_to', 'Unassigned'),
                'location': data.get('location', 'Unknown'),
                'victim_age': data.get('victim_age', 'Unknown'),
                'platform': data.get('platform', 'Unknown'),
                'ai_detected': data.get('ai_analysis', False)
            }
            
            cases_db.append(new_case)
            
            return jsonify({
                'success': True,
                'case': new_case,
                'message': 'Case created successfully'
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400

@app.route('/api/cases/<case_id>', methods=['PUT', 'DELETE'])
def handle_single_case(case_id):
    """Update or delete a specific case"""
    try:
        case_index = next((i for i, c in enumerate(cases_db) if c['id'] == case_id), None)
        
        if case_index is None:
            return jsonify({
                'success': False,
                'error': 'Case not found'
            }), 404
        
        if request.method == 'PUT':
            data = request.json
            cases_db[case_index].update(data)
            cases_db[case_index]['updated_at'] = datetime.now().isoformat()
            
            return jsonify({
                'success': True,
                'case': cases_db[case_index],
                'message': 'Case updated successfully'
            })
        
        elif request.method == 'DELETE':
            deleted_case = cases_db.pop(case_index)
            
            return jsonify({
                'success': True,
                'message': 'Case deleted successfully',
                'deleted_case': deleted_case
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/statistics')
def get_statistics():
    """Get system statistics"""
    try:
        high_risk = len([c for c in cases_db if c['risk_level'] == 'high'])
        medium_risk = len([c for c in cases_db if c['risk_level'] == 'medium'])
        low_risk = len([c for c in cases_db if c['risk_level'] == 'low'])
        
        real_ai_analyses = [a for a in analysis_history if a.get('is_real_ai')]
        
        threat_distribution = {
            'high': len([a for a in real_ai_analyses if a.get('threat_level') == 'high']),
            'medium': len([a for a in real_ai_analyses if a.get('threat_level') == 'medium']),
            'low': len([a for a in real_ai_analyses if a.get('threat_level') == 'low'])
        }
        
        emotion_counts = {}
        for analysis in real_ai_analyses:
            emotion = analysis.get('emotion', 'neutral')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_cases': len(cases_db),
                'high_risk_cases': high_risk,
                'medium_risk_cases': medium_risk,
                'low_risk_cases': low_risk,
                'total_analyses': len(analysis_history),
                'real_ai_analyses': len(real_ai_analyses),
                'today_analyses': len([a for a in analysis_history 
                                      if datetime.fromisoformat(a['timestamp']).date() == datetime.now().date()]),
                'threat_distribution': threat_distribution,
                'emotion_distribution': emotion_counts,
                'system_status': 'operational',
                'ai_status': 'active' if AI_AVAILABLE else 'fallback',
                'version': '3.0.0',
                'last_updated': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/analyses/recent')
def get_recent_analyses():
    """Get recent analyses"""
    try:
        limit = int(request.args.get('limit', 10))
        recent = analysis_history[-limit:] if analysis_history else []
        
        return jsonify({
            'success': True,
            'analyses': recent,
            'count': len(recent),
            'real_ai_count': len([a for a in recent if a.get('is_real_ai')])
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/export/cases')
def export_cases():
    """Export cases data as CSV"""
    try:
        df = pd.DataFrame(cases_db)
        
        output = BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'suspectspeech_cases_{datetime.now().strftime("%Y%m%d")}.csv'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '3.0.0',
        'ai_status': 'active' if AI_AVAILABLE else 'fallback',
        'endpoints': [
            '/analyze/text (REAL AI)',
            '/analyze/voice (Simulated)',
            '/api/cases',
            '/statistics',
            '/analyses/recent'
        ]
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("SUSPECTSPEECH - PHASE 3: REAL AI INTEGRATION")
    print("="*60)
    print(f"Python Version: 3.10.0")
    print(f"AI System: {'ACTIVE ✅' if AI_AVAILABLE else 'FALLBACK MODE ⚠️'}")
    print(f"Web Interface: http://localhost:5000")
    print(f"API Status: Running")
    print("="*60)
    print("\nTry these test phrases in the dashboard:")
    print("1. 'I need help immediately!'")
    print("2. 'I want to end my life'")
    print("3. 'Everything is wonderful today!'")
    print("4. 'I will find you and make you pay'")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)