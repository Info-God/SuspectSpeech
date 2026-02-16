# app_final.py - Working Phase 3
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime
import json

# Import our simple AI
from ai_simple import ai_engine

# Load environment
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'suspectspeech-2023')
CORS(app)

print("\n" + "="*60)
print("🚀 SUSPECTSPEECH - PHASE 3: REAL AI ANALYSIS")
print("="*60)
print("✅ AI Engine: ACTIVE")
print("🌐 Web Interface: http://localhost:5000")
print("="*60)

# Simple database
cases_db = []
analyses_db = []

# Add some sample cases
cases_db.append({
    'id': str(uuid.uuid4()),
    'case_id': 'CASE-001',
    'title': 'AI Detected High Threat',
    'description': 'Real AI analysis identified dangerous content',
    'status': 'open',
    'risk_level': 'high',
    'priority': 'urgent',
    'created_at': datetime.now().isoformat(),
    'platform': 'WhatsApp',
    'ai_detected': True
})

cases_db.append({
    'id': str(uuid.uuid4()),
    'case_id': 'CASE-002',
    'title': 'Suspicious Messages',
    'description': 'Multiple threatening messages detected',
    'status': 'investigating',
    'risk_level': 'medium',
    'priority': 'high',
    'created_at': datetime.now().isoformat(),
    'platform': 'Facebook',
    'ai_detected': True
})

# Routes
@app.route('/')
def home():
    return render_template('index.html', ai_available=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', ai_available=True)

@app.route('/cases')
def cases():
    return render_template('cases.html', ai_available=True)

@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    """Analyze text with real AI"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        text = data.get('text', '').strip()
        language = data.get('language', 'en')
        
        if not text:
            return jsonify({'success': False, 'error': 'Please enter text to analyze'}), 400
        
        print(f"\n📝 Analyzing: {text[:80]}...")
        
        # Use AI engine
        result = ai_engine.analyze(text, language)
        
        # Store in history
        analyses_db.append(result)
        if len(analyses_db) > 100:
            analyses_db.pop(0)
        
        return jsonify({
            'success': True,
            'analysis': result,
            'message': 'AI analysis completed successfully!'
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze_legacy():
    """Legacy endpoint"""
    return analyze_text()

@app.route('/api/cases', methods=['GET', 'POST'])
def handle_cases():
    """Case management API"""
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'cases': cases_db,
            'total': len(cases_db)
        })
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            new_case = {
                'id': str(uuid.uuid4()),
                'case_id': f"CASE-{len(cases_db) + 1:03d}",
                'title': data.get('title', 'New Case'),
                'description': data.get('description', ''),
                'status': 'open',
                'risk_level': data.get('risk_level', 'medium'),
                'priority': data.get('priority', 'medium'),
                'created_at': datetime.now().isoformat(),
                'assigned_to': data.get('assigned_to', 'Unassigned'),
                'platform': data.get('platform', 'Unknown')
            }
            
            cases_db.append(new_case)
            
            return jsonify({
                'success': True,
                'case': new_case,
                'message': 'Case created successfully'
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/cases/<case_id>', methods=['PUT', 'DELETE'])
def handle_single_case(case_id):
    """Update or delete case"""
    # Simplified version - find and update case
    for i, case in enumerate(cases_db):
        if case['id'] == case_id:
            if request.method == 'PUT':
                data = request.get_json()
                cases_db[i].update(data)
                return jsonify({'success': True, 'case': cases_db[i]})
            elif request.method == 'DELETE':
                deleted = cases_db.pop(i)
                return jsonify({'success': True, 'deleted_case': deleted})
    
    return jsonify({'success': False, 'error': 'Case not found'}), 404

@app.route('/statistics')
def statistics():
    """Get system stats"""
    high_risk = len([c for c in cases_db if c['risk_level'] == 'high'])
    medium_risk = len([c for c in cases_db if c['risk_level'] == 'medium'])
    low_risk = len([c for c in cases_db if c['risk_level'] == 'low'])
    
    high_threat = len([a for a in analyses_db if a.get('threat_level') == 'high'])
    medium_threat = len([a for a in analyses_db if a.get('threat_level') == 'medium'])
    low_threat = len([a for a in analyses_db if a.get('threat_level') == 'low'])
    
    return jsonify({
        'success': True,
        'statistics': {
            'total_cases': len(cases_db),
            'high_risk_cases': high_risk,
            'medium_risk_cases': medium_risk,
            'low_risk_cases': low_risk,
            'total_analyses': len(analyses_db),
            'high_threat_analyses': high_threat,
            'medium_threat_analyses': medium_threat,
            'low_threat_analyses': low_threat,
            'system_status': 'operational',
            'ai_status': 'active',
            'version': '3.0.0'
        }
    })

@app.route('/analyses/recent')
def recent_analyses():
    """Get recent analyses"""
    limit = min(int(request.args.get('limit', 10)), 50)
    recent = analyses_db[-limit:] if analyses_db else []
    
    return jsonify({
        'success': True,
        'analyses': recent,
        'count': len(recent)
    })

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai': 'active',
        'version': '3.0.0'
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 STARTING SUSPECTSPEECH SERVER...")
    print("="*60)
    print("💡 Try these test phrases in Dashboard:")
    print("   • 'I need help immediately!'")
    print("   • 'I want to end my life'")
    print("   • 'Everything is wonderful today!'")
    print("   • 'I will find you and hurt you'")
    print("="*60)
    print("🌐 Open: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000, use_reloader=False)