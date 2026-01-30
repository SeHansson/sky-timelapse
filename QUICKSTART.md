# 🚀 TIMESHIFT Quick Start Guide

Welcome to TIMESHIFT - your RTSP timelapse studio! This guide will get you up and running in minutes.

## Installation (Choose One Method)

### Method 1: Direct Python (Recommended for most users)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```
   
   Or use the quick start script:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

3. **Open your browser:**
   ```
   http://localhost:5000
   ```

### Method 2: Docker (Easiest for experienced users)

1. **Build and run:**
   ```bash
   docker-compose up -d
   ```

2. **Access the interface:**
   ```
   http://localhost:5000
   ```

## First Time Setup

1. **Enter RTSP URL**
   - Format: `rtsp://username:password@camera-ip:port/stream`
   - Example: `rtsp://admin:password123@192.168.1.100:554/stream1`

2. **Click "Test Stream"**
   - Should show "Stream accessible"
   - If not, check your camera settings and URL

3. **Configure Settings**
   - **Daily Timelapse Time**: When to create the video (e.g., 18:00)
   - **Frame Interval**: Seconds between captures (300 = 5 minutes)
   - **Timelapse FPS**: Video smoothness (30 recommended)

4. **Enable Capture**
   - Toggle the "Enable Capture" switch
   - Status should change to "Active"

5. **Save Settings**
   - Click "💾 Save Settings"

## Usage

### Automatic Mode
- Frames capture automatically at your set interval
- Timelapse video creates daily at your set time
- Monitor progress on the dashboard

### Manual Controls
- **📸 Capture Frame Now**: Get a frame immediately
- **🎬 Create Timelapse Now**: Generate video from existing frames
- **🖼️ View Frames**: Browse captured images
- **🎥 View Timelapses**: Download your videos

## What You'll See

```
┌─────────────────────────────────────┐
│  TIMESHIFT                          │
│  RTSP Timelapse Studio              │
├─────────────────────────────────────┤
│  Configuration      │  Status       │
│  ✓ RTSP URL         │  ● Active     │
│  ✓ Time: 18:00      │  42 Frames    │
│  ✓ Interval: 5min   │  3 Videos     │
│  ✓ FPS: 30          │  125 MB Used  │
├─────────────────────────────────────┤
│  Actions                            │
│  [Capture Now] [Create Timelapse]   │
│  [View Frames] [View Videos]        │
└─────────────────────────────────────┘
```

## File Locations

```
data/
├── config.json          # Your saved settings
├── frames/              # Captured images
│   └── frame_*.jpg
└── timelapses/          # Generated videos
    └── timelapse_*.mp4
```

## Common RTSP URLs by Camera Brand

- **Hikvision**: `rtsp://admin:pass@IP:554/Streaming/Channels/101`
- **Dahua**: `rtsp://admin:pass@IP:554/cam/realmonitor?channel=1&subtype=0`
- **Amcrest**: `rtsp://admin:pass@IP:554/cam/realmonitor?channel=1&subtype=1`
- **TP-Link**: `rtsp://admin:pass@IP:554/stream1`
- **Generic**: `rtsp://admin:pass@IP:554/stream1`

## Need Help?

- **Can't connect?** → See TROUBLESHOOTING.md
- **Questions?** → Check README.md
- **Test your stream** → Use VLC Media Player first

## Pro Tips

💡 **Start with these settings for best results:**
- Frame Interval: 300 seconds (5 minutes)
- FPS: 30
- Capture Time: Evening (after sun sets)

💡 **Storage Management:**
- ~500KB per frame
- Delete old frames after creating timelapses
- Use "Delete All Frames" to free space

💡 **Quality:**
- Use camera's main stream (not sub stream)
- Keep output at 1920x1080
- Ensure stable network connection

## That's It!

You're ready to create amazing timelapses! 🎬

For detailed information, see:
- **README.md** - Complete documentation
- **TROUBLESHOOTING.md** - Problem solving
- **config.example.json** - Configuration reference
