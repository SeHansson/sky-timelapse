# Sky-Timelapse Icons

This directory contains icons for the sky-timelapse application.

## Icon Files

### Main Icons
- **icon.svg** - Animated full-featured icon (512x512)
  - Use for: GitHub social preview, documentation, presentations
  - Features: Animated sun, clouds, recording indicator, timelapse arrows
  
- **icon-simple.svg** - Simplified static icon (512x512)
  - Use for: Docker Hub, app stores, printing
  - Cleaner design without animations

- **favicon.svg** - Small icon for browser tabs (32x32)
  - Already embedded in the web interface
  - Shows mini version of the logo

## Usage

### GitHub Repository
1. Upload `icon.svg` or `icon-simple.svg` to your repository root
2. Go to repository Settings → General
3. Under "Social preview" click "Edit"
4. Upload the icon

### Docker Hub
1. Go to your repository: https://hub.docker.com/r/sehansson/sky-timelapse
2. Click "Manage Repository"
3. Upload `icon-simple.svg` as the repository icon

### Unraid Template
The Unraid template already references:
```
https://raw.githubusercontent.com/sehansson/sky-timelapse/main/icon.svg
```

Just make sure `icon.svg` is in your repository root.

### Web Interface
The favicon is already embedded in `templates/index.html` as inline SVG data.

## Converting to PNG (Optional)

If you need PNG versions:

### Online Converters
- https://svgtopng.com/
- https://cloudconvert.com/svg-to-png

### Command Line (if you have ImageMagick/Inkscape)
```bash
# Using Inkscape
inkscape icon.svg -w 512 -h 512 -o icon.png

# Using ImageMagick with rsvg
convert icon.svg -resize 512x512 icon.png

# Using cairosvg (Python)
pip install cairosvg
cairosvg icon.svg -o icon.png -W 512 -H 512
```

### Common Sizes
- 512x512 - Docker Hub, GitHub
- 256x256 - Medium thumbnails
- 128x128 - Small thumbnails
- 64x64 - Tiny icons
- 32x32 - Favicon
- 16x16 - Browser favicon fallback

## Design Details

### Colors
- **Background**: #0a0e14 (dark)
- **Sky**: #00d4ff → #0077b6 (cyan gradient)
- **Accent**: #00ff9f → #00d4ff (green-cyan gradient)
- **Sun**: #ffd60a (yellow)
- **Recording**: #ff006e (pink/magenta)

### Elements
- Sky with sun and clouds (representing timelapse subject)
- Camera icon (representing RTSP capture)
- Recording indicator (red dot)
- Speed arrows (representing timelapse effect)
- Circular frame (representing continuous operation)

## License
These icons are part of the sky-timelapse project and follow the same MIT license.
