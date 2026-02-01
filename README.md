# TIMESHIFT - RTSP Timelapse Studio

A complete web application for creating automated timelapses from RTSP camera streams. Features a modern web interface with real-time monitoring and configurable capture settings.

![TIMESHIFT Interface](https://img.shields.io/badge/Status-Production%20Ready-00ff9f?style=for-the-badge)

## Features

### Core Functionality
- 📹 **RTSP Stream Support** - Connect to any RTSP camera stream
- ⏰ **Scheduled Captures** - Automatically capture frames at set intervals
- 🎬 **Automatic Timelapse Creation** - Generate timelapse videos daily with H.264 encoding
- 🖥️ **Modern Web Interface** - Sleek, responsive dashboard
- 📊 **Real-time Statistics** - Monitor frame count, storage, and status
- ⚙️ **Configurable Settings** - Adjust FPS, intervals, resolution, and timing

### Web Interface Features
- Live configuration management
- Stream connectivity testing
- Manual frame capture
- On-demand timelapse creation
- File browsing and downloads
- Storage management

## Prerequisites

- Python 3.8 or higher
- OpenCV compatible system
- RTSP camera or stream source
- Minimum 1GB free disk space (more for longer timelapses)

## Installation

### Option 1: Docker (Recommended)

**Using Docker Run:**
```bash
docker run -d \
  --name sky-timelapse \
  -p 5000:5000 \
  -v /path/to/data:/app/data \
  -e TZ=Europe/Berlin \
  sehansson/sky-timelapse:latest
```

**Using Docker Compose:**
```yaml
version: '3.8'
services:
  sky-timelapse:
    image: sehansson/sky-timelapse:latest
    container_name: sky-timelapse
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
    environment:
      - TZ=Europe/Berlin
    restart: unless-stopped
```

Then access at `http://localhost:5000`

### Option 2: Python Direct Install

### 1. Clone or Download the Application

```bash
# Clone from GitHub
git clone https://github.com/sehansson/sky-timelapse.git
cd sky-timelapse
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install Flask==3.0.0 flask-cors==4.0.0 numpy<2.0.0 opencv-python==4.8.1.78 schedule==1.2.0
```

### 3. Verify Installation

```bash
python app.py
```

You should see output indicating the server has started:
```
RTSP Timelapse Application started
Data directory: /path/to/data
 * Running on http://0.0.0.0:5000
```

## Usage

### Starting the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Web Interface

Open your browser and navigate to:
```
http://localhost:5000
```

Or from another device on your network:
```
http://YOUR_IP_ADDRESS:5000
```

### Configuration

1. **RTSP Stream URL**
   - Format: `rtsp://username:password@ip:port/stream`
   - Example: `rtsp://admin:password123@192.168.1.100:554/stream1`

2. **Daily Timelapse Time**
   - Set the time when the daily timelapse video should be created
   - Format: 24-hour (HH:MM)
   - Example: `18:00` creates timelapse at 6 PM

3. **Frame Interval**
   - Seconds between each frame capture
   - 300 seconds = 5 minutes (recommended)
   - Lower values = more frames = smoother timelapse
   - Higher values = fewer frames = more time coverage

4. **Capture Time Window** (Optional)
   - Enable to only capture frames during specific hours
   - Perfect for daylight-only capture (e.g., 06:00 to 20:00)
   - **Start Time**: When to begin capturing (e.g., sunrise)
   - **Stop Time**: When to stop capturing (e.g., sunset)
   - Supports windows that cross midnight (e.g., 20:00 to 06:00)

5. **Timelapse FPS**
   - Frames per second in the output video
   - 30 FPS = smooth playback (recommended)
   - 24 FPS = cinematic look
   - 60 FPS = very smooth

6. **Enable Capture**
   - Toggle to start/stop automatic capturing
   - Must be enabled for scheduled captures

### Workflow

#### Basic Setup
1. Enter your RTSP stream URL
2. Click "Test Stream" to verify connectivity
3. Configure capture interval and timelapse time
4. Set desired FPS for output videos
5. Enable capture
6. Click "Save Settings"

#### Manual Operations
- **Capture Frame Now**: Immediately capture a single frame
- **Create Timelapse Now**: Generate a timelapse from all captured frames
- **View Frames**: Browse all captured still frames
- **View Timelapses**: Browse all generated timelapse videos
- **Delete All Frames**: Clear all captured frames (frees storage)

### File Structure

```
rtsp-timelapse/
├── app.py                  # Main application
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Web interface
└── data/                  # Created on first run
    ├── config.json        # Saved settings
    ├── frames/            # Captured frames
    │   └── frame_YYYYMMDD_HHMMSS.jpg
    └── timelapses/        # Generated videos
        └── timelapse_YYYYMMDD_HHMMSS.mp4
```

## Configuration Examples

### Example 1: Sky Timelapse (Daylight Only)
- **Frame Interval**: 300 seconds (5 minutes)
- **Capture Window**: 06:00 to 20:00 (enabled)
- **Daily Time**: 20:30 (8:30 PM)
- **FPS**: 30
- **Result**: Daylight hours only, ~2-3 minute video per day

### Example 2: Construction Site (Daily Overview)
- **Frame Interval**: 600 seconds (10 minutes)
- **Daily Time**: 17:00 (5 PM)
- **FPS**: 30
- **Result**: Full day condensed into ~1-2 minute video

### Example 3: Plant Growth (Weekly Timelapse)
- **Frame Interval**: 3600 seconds (1 hour)
- **Daily Time**: 20:00 (8 PM)
- **FPS**: 24
- **Result**: Week of growth in ~2-3 minute video

### Example 4: Traffic Monitoring (High Detail)
- **Frame Interval**: 60 seconds (1 minute)
- **Daily Time**: 23:00 (11 PM)
- **FPS**: 60
- **Result**: Full day in ~5-10 minute smooth video

## API Endpoints

The application exposes a REST API:

### Configuration
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration

### Operations
- `POST /api/test-stream` - Test RTSP connectivity
- `POST /api/capture-now` - Capture frame immediately
- `POST /api/create-timelapse` - Generate timelapse now
- `POST /api/delete-frames` - Delete all frames

### Data
- `GET /api/stats` - Get statistics
- `GET /api/frames` - List captured frames
- `GET /api/timelapses` - List timelapse videos
- `GET /api/download/<filename>` - Download file

## Troubleshooting

### Cannot Connect to RTSP Stream
- Verify the RTSP URL is correct
- Check username and password
- Ensure camera is accessible from server
- Try accessing stream with VLC media player first
- Check firewall settings

### Frames Not Being Captured
- Ensure "Enable Capture" is toggled on
- Verify RTSP URL is configured
- Check server logs for errors
- Test stream connectivity

### Timelapse Video Issues
- Ensure at least 2 frames are captured
- Check available disk space
- Verify FFmpeg codecs are installed
- Review frame interval settings

### High Storage Usage
- Use "Delete All Frames" after creating timelapses
- Increase frame interval
- Lower output resolution
- Regular cleanup of old timelapses

## Advanced Configuration

### Custom Resolution
Edit the configuration in the web interface or directly in `data/config.json`:

```json
{
  "output_resolution": [1280, 720]  // 720p
}
```

Common resolutions:
- `[1920, 1080]` - 1080p (default)
- `[1280, 720]` - 720p
- `[3840, 2160]` - 4K

### Running as a Service (Linux)

Create a systemd service file `/etc/systemd/system/timeshift.service`:

```ini
[Unit]
Description=TIMESHIFT RTSP Timelapse Service
After=network.target

[Service]
Type=simple
User=yourusername
WorkingDirectory=/path/to/rtsp-timelapse
ExecStart=/usr/bin/python3 /path/to/rtsp-timelapse/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable timeshift
sudo systemctl start timeshift
```

### Remote Access

To access from outside your network:
1. Configure port forwarding on your router (port 5000)
2. Use a dynamic DNS service
3. Consider using HTTPS/reverse proxy for security

## Performance Considerations

- **Frame Interval**: 300-600 seconds is optimal for most use cases
- **Storage**: ~500KB per frame, plan for 288 frames/day at 5-min intervals
- **Video Codec**: H.264 (avc1) for optimal quality/size ratio; automatic fallback to MPEG-4
- **CPU Usage**: Minimal when not capturing; brief spike during capture/encoding
- **Memory**: ~200-500MB typical usage

## Video Output

- **Format**: MP4 container
- **Codec**: H.264 (primary), with automatic fallback to MPEG-4 if H.264 unavailable
- **Resolution**: Configurable (default 1920x1080)
- **Frame Rate**: Configurable 24-60 FPS (default 30 FPS)
- **Quality**: High quality, optimized compression

## Security Notes

- The application has no built-in authentication
- Use firewall rules to restrict access
- Store RTSP credentials securely
- Consider running behind a reverse proxy with authentication
- Regularly update dependencies

## License

This application is provided as-is for personal and commercial use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review server logs
3. Test RTSP stream independently
4. Verify all dependencies are installed

## Version History

- **v1.0.0** - Initial release
  - RTSP stream capture
  - Scheduled timelapse creation
  - Web interface
  - File management
  - Statistics tracking
