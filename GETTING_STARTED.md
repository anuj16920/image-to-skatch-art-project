# Getting Started with AI Art Animator

Welcome to AI Art Animator! This guide will get you up and running quickly.

## 🚀 Quick Start (5 minutes)

### 1. Install

```bash
pip install -r requirements.txt
```

### 2. Run GUI

```bash
python run_gui.py
```

### 3. Create Your First Animation

1. Click "Upload Image"
2. Select an image
3. Click "Generate Art"
4. Click "Create Animation"
5. Click "Export MP4"

Done! Your animation is saved.

## 📖 What You Need to Know

### Project Structure

This is now a **professional-grade package** with:

```
src/art_animator/     # Main package (new structure)
├── core/             # Animation engine
├── gui/              # GUI application
├── utils/            # Utilities
├── config/           # Configuration
└── cli.py            # Command-line interface

Old files (main.py, animator.py, etc.) still work but redirect to new structure.
```

### Two Ways to Run

**Option 1: Old Way (Still Works)**
```bash
python main.py
```

**Option 2: New Way (Recommended)**
```bash
python run_gui.py
# or after installing: art-animator-gui
```

### Command-Line Interface

```bash
# Basic usage
python run_cli.py animate input.jpg -o output.mp4

# With options
python run_cli.py animate input.jpg \
  --style "Pencil Sketch" \
  --speed 70 \
  --detail 80 \
  --fps 30
```

## 🎯 Common Tasks

### Change Art Style

GUI: Use the "Art Style" dropdown
CLI: `--style "Watercolor"`

### Adjust Animation Speed

GUI: Use the "Drawing Speed" slider
CLI: `--speed 70` (1-100)

### Change Resolution

GUI: Use the "Output Resolution" dropdown
CLI: `--resolution 1920x1080`

### Export as GIF

GUI: Check "Also Export GIF"
CLI: `--gif`

## 🔧 Configuration

Create `config/my_settings.yaml`:

```yaml
style:
  name: "Pencil Sketch"
  shading_intensity: 0.7

animation:
  speed: 60
  detail_level: 85
  fps: 30
  resolution: [1920, 1080]
```

## 📚 Learn More

- **User Guide**: `docs/user-guide.md` - Complete feature documentation
- **API Reference**: `docs/api-reference.md` - Programmatic usage
- **Examples**: `examples/` - Working code examples
- **Architecture**: `docs/architecture.md` - System design

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "FFmpeg not found"
Install FFmpeg:
- Windows: `choco install ffmpeg`
- Mac: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`

### Animation too slow
- Lower detail level (50-60)
- Use 720p resolution
- Enable time-lapse mode

### Not enough detail
- Increase detail level (85-95)
- Try "Advanced Sketch" style
- Use higher resolution

## 💡 Tips

1. **Start Simple**: Use default settings first
2. **Experiment**: Try different styles on same image
3. **Performance**: Lower detail for faster processing
4. **Quality**: Higher detail + slower speed = better results
5. **Styles**: Each style works better with different subjects

## 🎨 Style Guide

- **Portraits**: Pencil Sketch or Charcoal
- **Landscapes**: Watercolor or Oil Painting
- **Architecture**: Advanced Sketch
- **Anime Art**: Anime / Manga style
- **Dramatic**: Charcoal with high shading

## 🚀 Next Steps

1. ✅ Run your first animation
2. 📖 Read the user guide
3. 🎨 Try different styles
4. ⚙️ Experiment with parameters
5. 🔧 Create custom configurations
6. 💻 Try the CLI interface
7. 🐍 Use the Python API
8. 🤝 Contribute improvements

## 📞 Get Help

- **Documentation**: Check `docs/` directory
- **Examples**: See `examples/` for code samples
- **Issues**: Report bugs on GitHub
- **Discussions**: Ask questions in GitHub Discussions

## 🎉 You're Ready!

You now have a professional-grade animation system. Start creating!

```bash
python run_gui.py
```

Happy animating! 🎨✨
