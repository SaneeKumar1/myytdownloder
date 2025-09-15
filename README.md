# YouTube Video Downloader 📹

A simple and user-friendly YouTube video downloader built with Python and Streamlit.

## Features

- 🎥 Download YouTube videos in multiple qualities (1080p, 720p, 480p)
- 🎵 Download audio-only files as MP3 (192kbps)
- 📺 Preview video information before downloading
- 🎨 Modern and intuitive user interface
- 📁 Automatic file organization in Downloads folder
- ⚡ Fast and reliable downloads using yt-dlp

## Installation

1. **Clone or download this repository**

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

3. **Paste a YouTube URL** in the input field

4. **Preview the video** (optional) by clicking "Preview Video Info"

5. **Choose your preferences:**
   - Download type: Video or Audio Only
   - Quality: Best (1080p), Medium (720p), or Low (480p)

6. **Click Download** and wait for the process to complete

## Download Location

Downloaded files are saved to:
```
{Your Home Directory}/Downloads/YouTube_Downloads/
```

## Requirements

- Python 3.7+
- Streamlit
- yt-dlp
- Internet connection

## Important Notes

- ⚠️ Please respect copyright laws and YouTube's Terms of Service
- 🔒 This tool is for personal use only
- 📱 Some videos may not be available for download due to restrictions
- 🌐 Requires stable internet connection for downloads

## Troubleshooting

**Download fails:**
- Check if the URL is valid and accessible
- Ensure stable internet connection
- Try different quality settings
- Some videos may have download restrictions

**App won't start:**
- Make sure all dependencies are installed
- Check Python version compatibility
- Verify Streamlit installation

## 🚀 Deployment to Streamlit Cloud

Want to make your app accessible from anywhere? Deploy it to Streamlit Cloud for free!

### Quick Deployment Steps:

1. **Create GitHub Repository**
   - Go to [github.com](https://github.com) → New repository
   - Name: `youtube-video-downloader` (make it public)
   - Upload all project files

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub → New app
   - Select your repository → Set main file: `app.py`
   - Click Deploy!

3. **Get Your Public URL**
   - Your app will be live at: `https://[username]-youtube-video-downloader-app-[hash].streamlit.app`
   - Share this URL with anyone worldwide!

### 📱 Benefits of Cloud Deployment:
- ✅ **Global Access**: Use from any device, anywhere
- ✅ **Mobile Optimized**: Perfect mobile experience
- ✅ **No Installation**: No need to install Python/dependencies
- ✅ **Auto-Updates**: Updates when you change GitHub files
- ✅ **Free Hosting**: Completely free for public repositories

📋 **Detailed Instructions**: See `DEPLOYMENT.md` for complete step-by-step guide.

## License

This project is for educational purposes. Please respect YouTube's Terms of Service and copyright laws.
