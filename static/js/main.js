// static/js/main.js - Main JavaScript for SuspectSpeech

// Global variables
let voiceRecorder = null;
let audioChunks = [];
let isRecording = false;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    checkPageSpecificFeatures();
});

// Initialize all event listeners
function initializeEventListeners() {
    // Navigation active state
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
    
    // Voice recording simulation
    const recordBtn = document.getElementById('recordBtn');
    const stopBtn = document.getElementById('stopBtn');
    const analyzeVoiceBtn = document.getElementById('analyzeVoiceBtn');
    
    if (recordBtn) {
        recordBtn.addEventListener('click', startRecordingSimulation);
    }
    
    if (stopBtn) {
        stopBtn.addEventListener('click', stopRecordingSimulation);
    }
    
    if (analyzeVoiceBtn) {
        analyzeVoiceBtn.addEventListener('click', analyzeVoice);
    }
    
    // File upload handling
    const audioFileInput = document.getElementById('audioFile');
    if (audioFileInput) {
        audioFileInput.addEventListener('change', handleAudioUpload);
    }
    
    const batchFilesInput = document.getElementById('batchFiles');
    if (batchFilesInput) {
        batchFilesInput.addEventListener('change', handleBatchUpload);
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Check and initialize page-specific features
function checkPageSpecificFeatures() {
    // Dashboard page features
    if (document.getElementById('analysisText')) {
        initializeDashboard();
    }
    
    // Cases page features
    if (document.getElementById('casesTableBody')) {
        // Cases page JavaScript is in the template
    }
}

// Dashboard initialization
function initializeDashboard() {
    // Load dashboard data if on dashboard
    if (typeof loadDashboardData === 'function') {
        loadDashboardData();
    }
    
    // Real-time clock update
    updateClock();
    setInterval(updateClock, 60000);
}

// Update clock in dashboard
function updateClock() {
    const clockElement = document.getElementById('currentTime');
    if (clockElement) {
        const now = new Date();
        clockElement.textContent = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });
    }
}

// Voice recording simulation (mock - will be real in Phase 3)
function startRecordingSimulation() {
    const recordBtn = document.getElementById('recordBtn');
    const stopBtn = document.getElementById('stopBtn');
    const statusDiv = document.getElementById('recordingStatus');
    const analyzeBtn = document.getElementById('analyzeVoiceBtn');
    
    isRecording = true;
    
    // Update UI
    recordBtn.disabled = true;
    recordBtn.classList.add('recording');
    stopBtn.disabled = false;
    analyzeBtn.disabled = true;
    
    statusDiv.innerHTML = `
        <div class="alert alert-danger">
            <i class="fas fa-microphone"></i> Recording... (Simulation Mode)
        </div>
    `;
    
    // Simulate recording for 5 seconds
    setTimeout(() => {
        if (isRecording) {
            statusDiv.innerHTML = `
                <div class="alert alert-success">
                    <i class="fas fa-check-circle"></i> Recording complete! Ready to analyze.
                </div>
            `;
            analyzeBtn.disabled = false;
        }
    }, 5000);
}

function stopRecordingSimulation() {
    const recordBtn = document.getElementById('recordBtn');
    const stopBtn = document.getElementById('stopBtn');
    const statusDiv = document.getElementById('recordingStatus');
    const analyzeBtn = document.getElementById('analyzeVoiceBtn');
    
    isRecording = false;
    
    // Update UI
    recordBtn.disabled = false;
    recordBtn.classList.remove('recording');
    stopBtn.disabled = true;
    analyzeBtn.disabled = false;
    
    statusDiv.innerHTML = `
        <div class="alert alert-info">
            <i class="fas fa-info-circle"></i> Recording stopped. Click "Analyze Voice" to process.
        </div>
    `;
}

// Handle audio file upload
function handleAudioUpload(event) {
    const file = event.target.files[0];
    const analyzeBtn = document.getElementById('analyzeVoiceBtn');
    
    if (file) {
        if (file.type.startsWith('audio/')) {
            analyzeBtn.disabled = false;
            showNotification('Audio file loaded: ' + file.name, 'success');
        } else {
            showNotification('Please upload an audio file', 'error');
            analyzeBtn.disabled = true;
        }
    }
}

// Handle batch file upload
function handleBatchUpload(event) {
    const files = event.target.files;
    const analyzeBtn = document.getElementById('analyzeBatchBtn');
    
    if (files.length > 0) {
        analyzeBtn.disabled = false;
        showNotification(`Loaded ${files.length} file(s) for batch analysis`, 'info');
    }
}

// Analyze voice (mock)
async function analyzeVoice() {
    try {
        // Show loading
        const resultsArea = document.getElementById('resultsArea');
        resultsArea.innerHTML = `
            <div class="spinner-container">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Processing audio...</span>
                </div>
                <p class="mt-2">Processing audio recording...</p>
            </div>
        `;
        
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Call mock voice analysis API
        const response = await fetch('/analyze/voice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                audio_data: 'mock_audio_data',
                language: 'en'
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display results using dashboard's display function
            if (typeof displayAnalysisResult === 'function') {
                displayAnalysisResult(data.analysis);
            } else {
                // Fallback display
                resultsArea.innerHTML = `
                    <div class="alert alert-success">
                        <h5><i class="fas fa-check-circle"></i> Voice Analysis Complete</h5>
                        <p><strong>Transcription:</strong> ${data.transcription}</p>
                        <p><strong>Threat Level:</strong> ${data.analysis.threat_level}</p>
                    </div>
                `;
            }
            
            showNotification('Voice analysis completed successfully!', 'success');
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showNotification('Error analyzing voice: ' + error.message, 'error');
        console.error('Voice analysis error:', error);
    }
}

// Notification system
function showNotification(message, type = 'info') {
    // Check if notification container exists
    let container = document.getElementById('notification-container');
    
    if (!container) {
        container = document.createElement('div');
        container.id = 'notification-container';
        container.style.position = 'fixed';
        container.style.top = '20px';
        container.style.right = '20px';
        container.style.zIndex = '9999';
        document.body.appendChild(container);
    }
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.style.minWidth = '300px';
    notification.style.marginBottom = '10px';
    notification.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
    
    notification.innerHTML = `
        <strong>${type === 'success' ? 'Success' : type === 'error' ? 'Error' : 'Info'}</strong>
        <span>${message}</span>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function getThreatColor(level) {
    switch(level) {
        case 'high': return 'danger';
        case 'medium': return 'warning';
        case 'low': return 'success';
        default: return 'secondary';
    }
}

function getEmotionColor(emotion) {
    const colors = {
        'anger': 'danger',
        'fear': 'info',
        'joy': 'success',
        'sadness': 'secondary',
        'surprise': 'warning',
        'neutral': 'light',
        'disgust': 'dark'
    };
    return colors[emotion] || 'secondary';
}

// Export utility functions to global scope
window.showNotification = showNotification;
window.formatDate = formatDate;
window.getThreatColor = getThreatColor;
window.getEmotionColor = getEmotionColor;