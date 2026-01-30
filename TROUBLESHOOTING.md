# TIMESHIFT Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Error: "No module named 'cv2'"
**Problem:** OpenCV not properly installed

**Solution:**
```bash
pip install opencv-python --break-system-packages
# or
pip3 install opencv-python --break-system-packages
```

#### Error: "ImportError: libGL.so.1"
**Problem:** Missing OpenCV system dependencies (Linux)

**Solution (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install libgl1-mesa-glx libglib2.0-0
```

**Solution (Fedora/RHEL):**
```bash
sudo dnf install mesa-libGL
```

---

### RTSP Connection Issues

#### Error: "Cannot access stream"
**Possible Causes:**
1. Incorrect RTSP URL
2. Wrong credentials
3. Camera not accessible
4. Firewall blocking connection
5. Wrong port

**Debugging Steps:**

1. **Test with VLC Media Player**
   - Open VLC
   - Media → Open Network Stream
   - Enter your RTSP URL
   - If VLC can't connect, the issue is with the stream, not TIMESHIFT

2. **Verify RTSP URL Format**
   ```
   Correct:   rtsp://admin:password123@192.168.1.100:554/stream1
   Incorrect: rtsp://192.168.1.100  (missing port and credentials)
   Incorrect: http://192.168.1.100  (wrong protocol)
   ```

3. **Check Camera Settings**
   - Verify RTSP is enabled on camera
   - Check correct port (usually 554 or 8554)
   - Verify username and password
   - Some cameras require main/sub stream specification

4. **Network Testing**
   ```bash
   # Check if camera is reachable
   ping 192.168.1.100
   
   # Check if RTSP port is open
   telnet 192.168.1.100 554
   ```

5. **Common RTSP URL Formats by Brand**
   - **Hikvision**: `rtsp://admin:password@IP:554/Streaming/Channels/101`
   - **Dahua**: `rtsp://admin:password@IP:554/cam/realmonitor?channel=1&subtype=0`
   - **Amcrest**: `rtsp://admin:password@IP:554/cam/realmonitor?channel=1&subtype=1`
   - **Axis**: `rtsp://admin:password@IP:554/axis-media/media.amp`
   - **Foscam**: `rtsp://admin:password@IP:554/videoMain`
   - **TP-Link**: `rtsp://admin:password@IP:554/stream1`
   - **Generic**: `rtsp://admin:password@IP:554/stream1`

---

### Capture Issues

#### Frames Not Being Captured

**Check 1: Is Capture Enabled?**
- Web Interface → Configuration → Enable Capture toggle must be ON
- Status should show "Active"

**Check 2: Valid RTSP URL**
- Use "Test Stream" button to verify connectivity
- Must show "Stream accessible"

**Check 3: Check Logs**
```bash
# Run app with verbose output
python3 app.py
```
Look for errors in the console

**Check 4: Verify Scheduler**
- Frame interval must be reasonable (60-3600 seconds typical)
- Check system time is correct
- Restart application after changing settings

#### "Failed to capture frame from RTSP"

**Causes:**
1. Stream temporarily unavailable
2. Network interruption
3. Camera rebooted
4. Codec compatibility issues

**Solutions:**
- Restart the camera
- Restart TIMESHIFT
- Try different resolution settings
- Check camera's stream settings (H.264 recommended)

---

### Timelapse Creation Issues

#### "Not enough frames to create timelapse"

**Problem:** Need at least 2 frames to create a video

**Solution:**
- Capture more frames manually using "Capture Frame Now"
- Wait for scheduled captures to accumulate frames
- Lower frame interval to capture more frequently

#### Timelapse Video Won't Play

**Causes:**
1. Incomplete encoding
2. Codec compatibility
3. Corrupted frames

**Solutions:**
- Try different media player (VLC recommended)
- Re-create timelapse with "Create Timelapse Now"
- Check if all frames are valid images
- Verify sufficient disk space

#### Poor Video Quality

**Improve Quality:**
1. Increase output resolution in settings
2. Use higher quality RTSP stream (main stream vs sub stream)
3. Adjust camera bitrate settings
4. Use higher FPS (30-60)

---

### Web Interface Issues

#### Cannot Access Web Interface

**Check 1: Is Server Running?**
```bash
# Check if process is running
ps aux | grep app.py

# Check if port 5000 is in use
netstat -tuln | grep 5000
# or
lsof -i :5000
```

**Check 2: Correct URL**
- Local: `http://localhost:5000`
- Same network: `http://YOUR_IP:5000`
- NOT `https://` (unless you configured SSL)

**Check 3: Firewall**
```bash
# Allow port 5000 (Linux)
sudo ufw allow 5000
# or
sudo firewall-cmd --add-port=5000/tcp --permanent
sudo firewall-cmd --reload
```

#### Settings Not Saving

**Solutions:**
1. Check write permissions on `data/` directory
2. Look for errors in console when clicking "Save Settings"
3. Manually edit `data/config.json` if needed
4. Ensure disk space available

---

### Storage Issues

#### Disk Space Running Out

**Quick Fix:**
1. Use "Delete All Frames" to clear captured frames
2. Manually delete old timelapses from `data/timelapses/`
3. Increase frame interval to capture less frequently

**Long-term Solutions:**
1. Set up automatic cleanup script
2. Use external storage
3. Reduce output resolution
4. Archive timelapses to external drive

**Automatic Cleanup Script** (`cleanup.sh`):
```bash
#!/bin/bash
# Delete frames older than 7 days
find /path/to/data/frames/ -name "*.jpg" -mtime +7 -delete

# Delete timelapses older than 30 days
find /path/to/data/timelapses/ -name "*.mp4" -mtime +30 -delete
```

---

### Performance Issues

#### High CPU Usage

**Causes:**
- Capturing very frequently
- Very high resolution
- Multiple simultaneous operations

**Solutions:**
- Increase frame interval
- Lower output resolution
- Stagger capture times if using multiple cameras

#### Application Crashes

**Debug Steps:**
1. Check system logs
2. Monitor memory usage: `top` or `htop`
3. Verify all dependencies installed correctly
4. Check for Python version compatibility
5. Run with debug logging:
   ```python
   # Add to app.py
   logging.basicConfig(level=logging.DEBUG)
   ```

---

## Docker-Specific Issues

#### Container Won't Start

```bash
# Check container logs
docker logs timeshift

# Check if port is already in use
docker ps -a
```

#### Cannot Access from Host

**Solution:**
Ensure port mapping is correct in docker-compose.yml:
```yaml
ports:
  - "5000:5000"  # host:container
```

#### Data Not Persisting

**Solution:**
Verify volume mount in docker-compose.yml:
```yaml
volumes:
  - ./data:/app/data
```

---

## Testing Checklist

### Complete System Test

1. **Installation**
   - [ ] All dependencies installed
   - [ ] No error messages on startup
   - [ ] Web interface accessible

2. **Configuration**
   - [ ] RTSP URL format is correct
   - [ ] Test Stream shows "Stream accessible"
   - [ ] Settings save without errors

3. **Manual Capture**
   - [ ] "Capture Frame Now" works
   - [ ] Frame appears in frames list
   - [ ] Frame count increments

4. **Automatic Capture**
   - [ ] Enable Capture toggle is ON
   - [ ] Status shows "Active"
   - [ ] Wait one interval period
   - [ ] New frame captured automatically

5. **Timelapse Creation**
   - [ ] At least 2 frames captured
   - [ ] "Create Timelapse Now" succeeds
   - [ ] Video appears in timelapses list
   - [ ] Video downloads and plays correctly

---

## Getting Help

### Information to Provide When Seeking Help

1. **System Information**
   - Operating System and version
   - Python version: `python3 --version`
   - Installed packages: `pip3 list`

2. **Error Details**
   - Complete error message
   - When the error occurs
   - Steps to reproduce

3. **Configuration**
   - RTSP URL format (remove credentials)
   - Current settings
   - Contents of `data/config.json` (remove sensitive data)

4. **Logs**
   - Console output when running `python3 app.py`
   - Any error messages from browser console (F12)

### Useful Diagnostic Commands

```bash
# Check Python and pip versions
python3 --version
pip3 --version

# List installed packages
pip3 list

# Test RTSP with ffmpeg
ffmpeg -i "rtsp://user:pass@ip:port/stream" -frames:v 1 test.jpg

# Check OpenCV installation
python3 -c "import cv2; print(cv2.__version__)"

# Check Flask installation
python3 -c "import flask; print(flask.__version__)"

# Monitor system resources
top
# or
htop

# Check disk space
df -h

# Check network connectivity to camera
ping CAMERA_IP
telnet CAMERA_IP 554
```

---

## Advanced Troubleshooting

### Enable Debug Mode

Modify `app.py`:

```python
# Change this line at the bottom
app.run(host='0.0.0.0', port=5000, debug=True)  # Set debug=True
```

This provides detailed error pages and auto-reload on code changes.

### Manual Frame Capture Test

Test OpenCV directly:

```python
import cv2

rtsp_url = "rtsp://your_url_here"
cap = cv2.VideoCapture(rtsp_url)
ret, frame = cap.read()

if ret:
    cv2.imwrite("test_frame.jpg", frame)
    print("Success! Frame saved as test_frame.jpg")
else:
    print("Failed to capture frame")

cap.release()
```

### Reset Everything

If all else fails:

```bash
# Stop the application
# Delete data directory
rm -rf data/

# Reinstall dependencies
pip3 install -r requirements.txt --force-reinstall

# Restart application
python3 app.py
```

---

## Frequently Asked Questions

**Q: Can I use multiple cameras?**
A: Currently, one instance supports one camera. Run multiple instances on different ports for multiple cameras.

**Q: How much storage do I need?**
A: Approximately 500KB per frame. At 5-minute intervals, that's ~140MB per day. Plan accordingly.

**Q: Can I change the video codec?**
A: Edit `app.py` and change the `fourcc` codec in the `create_timelapse()` function.

**Q: Does this work with ONVIF cameras?**
A: Yes, if they support RTSP streaming. Use the RTSP URL, not the ONVIF URL.

**Q: Can I run this 24/7?**
A: Yes, it's designed for continuous operation. Consider running as a system service.

**Q: What's the maximum frame interval?**
A: Technically unlimited, but practical maximum is 3600 seconds (1 hour) for daily timelapses.

**Q: Can I customize the web interface?**
A: Yes, edit `templates/index.html` to modify the design.
