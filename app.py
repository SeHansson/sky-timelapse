#!/usr/bin/env python3
"""
RTSP Timelapse Application
Main backend server with Flask API
"""

from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS
import cv2
import os
import json
import threading
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging

app = Flask(__name__)
CORS(app)

# Configuration
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'
FRAMES_DIR = DATA_DIR / 'frames'
TIMELAPSES_DIR = DATA_DIR / 'timelapses'
CONFIG_FILE = DATA_DIR / 'config.json'

# Create necessary directories
for dir_path in [DATA_DIR, FRAMES_DIR, TIMELAPSES_DIR]:
    dir_path.mkdir(exist_ok=True)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    'rtsp_url': '',
    'capture_time': '12:00',
    'capture_start_time': '06:00',  # Start capturing at 6 AM
    'capture_stop_time': '20:00',   # Stop capturing at 8 PM
    'capture_schedule_enabled': False,  # Enable/disable time-based capture
    'fps': 30,
    'frame_interval': 300,  # seconds between frames (5 minutes)
    'output_resolution': [1920, 1080],
    'enabled': False,
    'last_capture': None,
    'total_frames_captured': 0
}

# Global state
current_config = DEFAULT_CONFIG.copy()
capture_thread = None
is_capturing = False
scheduler_thread = None


def load_config():
    """Load configuration from file"""
    global current_config
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                loaded = json.load(f)
                current_config.update(loaded)
                logger.info("Configuration loaded")
        except Exception as e:
            logger.error(f"Error loading config: {e}")
    return current_config


def save_config():
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(current_config, f, indent=2)
        logger.info("Configuration saved")
    except Exception as e:
        logger.error(f"Error saving config: {e}")


def capture_frame_from_rtsp(rtsp_url, output_path):
    """Capture a single frame from RTSP stream"""
    try:
        cap = cv2.VideoCapture(rtsp_url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # Try to read a frame
        ret, frame = cap.read()
        if ret:
            # Resize if needed
            target_width, target_height = current_config['output_resolution']
            frame = cv2.resize(frame, (target_width, target_height))
            
            # Save frame
            cv2.imwrite(str(output_path), frame)
            cap.release()
            return True
        else:
            cap.release()
            logger.error("Failed to capture frame from RTSP")
            return False
    except Exception as e:
        logger.error(f"Error capturing frame: {e}")
        return False


def create_timelapse():
    """Create timelapse video from captured frames"""
    try:
        frame_files = sorted(FRAMES_DIR.glob('frame_*.jpg'))
        
        if len(frame_files) < 2:
            logger.warning("Not enough frames to create timelapse")
            return None
        
        # Get frame dimensions
        first_frame = cv2.imread(str(frame_files[0]))
        height, width, _ = first_frame.shape
        
        # Create output filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = TIMELAPSES_DIR / f'timelapse_{timestamp}.mp4'
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = current_config['fps']
        out = cv2.VideoWriter(str(output_file), fourcc, fps, (width, height))
        
        # Write frames to video
        for frame_file in frame_files:
            frame = cv2.imread(str(frame_file))
            out.write(frame)
        
        out.release()
        logger.info(f"Timelapse created: {output_file}")
        
        return str(output_file.name)
    except Exception as e:
        logger.error(f"Error creating timelapse: {e}")
        return None


def scheduled_capture():
    """Scheduled task to capture frames"""
    global current_config
    
    if not current_config['enabled'] or not current_config['rtsp_url']:
        return
    
    # Check if we're within the capture time window
    if current_config.get('capture_schedule_enabled', False):
        now = datetime.now().time()
        start_time = datetime.strptime(current_config.get('capture_start_time', '00:00'), '%H:%M').time()
        stop_time = datetime.strptime(current_config.get('capture_stop_time', '23:59'), '%H:%M').time()
        
        # Handle time windows that cross midnight
        if start_time <= stop_time:
            # Normal case: 06:00 to 20:00
            if not (start_time <= now <= stop_time):
                logger.info(f"Outside capture window ({current_config['capture_start_time']} - {current_config['capture_stop_time']}), skipping capture")
                return
        else:
            # Crosses midnight: 20:00 to 06:00
            if not (now >= start_time or now <= stop_time):
                logger.info(f"Outside capture window ({current_config['capture_start_time']} - {current_config['capture_stop_time']}), skipping capture")
                return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    frame_path = FRAMES_DIR / f'frame_{timestamp}.jpg'
    
    logger.info(f"Capturing frame at {timestamp}")
    
    if capture_frame_from_rtsp(current_config['rtsp_url'], frame_path):
        current_config['last_capture'] = timestamp
        current_config['total_frames_captured'] += 1
        save_config()
        logger.info(f"Frame captured successfully: {frame_path}")
    else:
        logger.error("Frame capture failed")


def run_scheduler():
    """Run the scheduler in a separate thread"""
    while True:
        schedule.run_pending()
        time.sleep(1)


def setup_schedule():
    """Setup the scheduled capture"""
    schedule.clear()
    
    if current_config['enabled']:
        # Schedule daily timelapse creation
        schedule.every().day.at(current_config['capture_time']).do(
            lambda: create_timelapse()
        )
        
        # Schedule frame capture at intervals
        interval = current_config['frame_interval']
        schedule.every(interval).seconds.do(scheduled_capture)
        
        logger.info(f"Scheduled: Timelapse at {current_config['capture_time']}, "
                   f"frames every {interval} seconds")


# API Routes
@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    return jsonify(current_config)


@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration"""
    global current_config
    
    data = request.json
    
    # Update config
    for key in ['rtsp_url', 'capture_time', 'capture_start_time', 'capture_stop_time', 
                'capture_schedule_enabled', 'fps', 'frame_interval', 
                'output_resolution', 'enabled']:
        if key in data:
            current_config[key] = data[key]
    
    save_config()
    setup_schedule()
    
    return jsonify({
        'success': True,
        'config': current_config
    })


@app.route('/api/test-stream', methods=['POST'])
def test_stream():
    """Test RTSP stream connection"""
    data = request.json
    rtsp_url = data.get('rtsp_url', '')
    
    try:
        cap = cv2.VideoCapture(rtsp_url)
        ret, _ = cap.read()
        cap.release()
        
        return jsonify({
            'success': ret,
            'message': 'Stream accessible' if ret else 'Cannot access stream'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })


@app.route('/api/capture-now', methods=['POST'])
def capture_now():
    """Manually capture a frame immediately"""
    if not current_config['rtsp_url']:
        return jsonify({
            'success': False,
            'message': 'No RTSP URL configured'
        }), 400
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    frame_path = FRAMES_DIR / f'frame_{timestamp}.jpg'
    
    success = capture_frame_from_rtsp(current_config['rtsp_url'], frame_path)
    
    if success:
        current_config['last_capture'] = timestamp
        current_config['total_frames_captured'] += 1
        save_config()
    
    return jsonify({
        'success': success,
        'message': 'Frame captured' if success else 'Capture failed',
        'frame_count': current_config['total_frames_captured']
    })


@app.route('/api/create-timelapse', methods=['POST'])
def create_timelapse_now():
    """Manually create timelapse from existing frames"""
    filename = create_timelapse()
    
    if filename:
        return jsonify({
            'success': True,
            'message': 'Timelapse created',
            'filename': filename
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to create timelapse'
        }), 400


@app.route('/api/frames', methods=['GET'])
def get_frames():
    """Get list of captured frames"""
    frames = []
    for frame_file in sorted(FRAMES_DIR.glob('frame_*.jpg'), reverse=True):
        stat = frame_file.stat()
        frames.append({
            'filename': frame_file.name,
            'timestamp': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'size': stat.st_size
        })
    
    return jsonify({
        'frames': frames,
        'total': len(frames)
    })


@app.route('/api/timelapses', methods=['GET'])
def get_timelapses():
    """Get list of created timelapses"""
    timelapses = []
    for video_file in sorted(TIMELAPSES_DIR.glob('timelapse_*.mp4'), reverse=True):
        stat = video_file.stat()
        timelapses.append({
            'filename': video_file.name,
            'timestamp': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'size': stat.st_size
        })
    
    return jsonify({
        'timelapses': timelapses,
        'total': len(timelapses)
    })


@app.route('/api/download/<path:filename>', methods=['GET'])
def download_file(filename):
    """Download a timelapse or frame"""
    # Check in timelapses directory
    file_path = TIMELAPSES_DIR / filename
    if file_path.exists():
        return send_file(file_path, as_attachment=True)
    
    # Check in frames directory
    file_path = FRAMES_DIR / filename
    if file_path.exists():
        return send_file(file_path, as_attachment=True)
    
    return jsonify({'error': 'File not found'}), 404


@app.route('/api/delete-frames', methods=['POST'])
def delete_frames():
    """Delete all captured frames"""
    count = 0
    for frame_file in FRAMES_DIR.glob('frame_*.jpg'):
        frame_file.unlink()
        count += 1
    
    current_config['total_frames_captured'] = 0
    save_config()
    
    return jsonify({
        'success': True,
        'message': f'Deleted {count} frames'
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get application statistics"""
    frame_count = len(list(FRAMES_DIR.glob('frame_*.jpg')))
    timelapse_count = len(list(TIMELAPSES_DIR.glob('timelapse_*.mp4')))
    
    # Calculate total storage used
    total_size = 0
    for f in FRAMES_DIR.glob('frame_*.jpg'):
        total_size += f.stat().st_size
    for f in TIMELAPSES_DIR.glob('timelapse_*.mp4'):
        total_size += f.stat().st_size
    
    return jsonify({
        'frame_count': frame_count,
        'timelapse_count': timelapse_count,
        'total_storage_mb': round(total_size / (1024 * 1024), 2),
        'last_capture': current_config.get('last_capture'),
        'enabled': current_config['enabled']
    })


if __name__ == '__main__':
    # Load configuration
    load_config()
    
    # Setup scheduler
    setup_schedule()
    
    # Start scheduler thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    logger.info("RTSP Timelapse Application started")
    logger.info(f"Data directory: {DATA_DIR}")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
