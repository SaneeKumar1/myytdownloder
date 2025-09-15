import streamlit as st
import yt_dlp
import os
import tempfile
from pathlib import Path
import time

# Set page config
st.set_page_config(
    page_title="YouTube Video Downloader",
    page_icon="📹",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-responsive styling
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .main-header {
        text-align: center;
        color: #FF0000;
        font-size: clamp(1.5rem, 5vw, 3rem);
        font-weight: bold;
        margin-bottom: 1rem;
        padding: 0 1rem;
    }
    
    .download-section {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        width: 100%;
        box-sizing: border-box;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        word-wrap: break-word;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
        word-wrap: break-word;
    }
    
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }
        
        .download-section {
            padding: 0.8rem;
            margin: 0.3rem 0;
        }
        
        .stButton > button {
            width: 100% !important;
            margin: 0.5rem 0 !important;
            padding: 0.75rem 1rem !important;
            font-size: 1rem !important;
        }
        
        .stSelectbox > div > div {
            font-size: 0.9rem !important;
        }
        
        .stTextInput > div > div > input {
            font-size: 1rem !important;
            padding: 0.75rem !important;
        }
        
        /* Make columns stack on mobile */
        .row-widget.stHorizontal {
            flex-direction: column !important;
        }
        
        .row-widget.stHorizontal > div {
            width: 100% !important;
            margin-bottom: 1rem !important;
        }
    }
    
    /* Tablet optimizations */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main-header {
            font-size: 2.2rem;
        }
        
        .download-section {
            padding: 1.5rem;
        }
    }
    
    /* Desktop optimizations */
    @media (min-width: 1025px) {
        .main-header {
            font-size: 3rem;
            margin-bottom: 2rem;
        }
        
        .download-section {
            padding: 2rem;
            margin: 1rem 0;
        }
    }
    
    /* General mobile improvements */
    .stApp {
        padding-top: 1rem !important;
    }
    
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Touch-friendly buttons */
    .stButton > button {
        min-height: 44px !important;
        touch-action: manipulation;
    }
    
    /* Improve text readability on mobile */
    p, div, span {
        line-height: 1.5 !important;
    }
    
    /* Make images responsive */
    img {
        max-width: 100% !important;
        height: auto !important;
    }
</style>
""", unsafe_allow_html=True)

def get_video_info(url):
    """Get video information without downloading"""
    try:
        if not url or not url.startswith(('https://www.youtube.com/', 'https://youtu.be/')):
            st.error("Please enter a valid YouTube URL")
            return None
            
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # Only extract metadata
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'upload_date': info.get('upload_date', 'Unknown'),
                'thumbnail': info.get('thumbnail', None)
            }
    except Exception as e:
        st.error(f"Error getting video info: {str(e)}")
        return None

def download_video(url, quality='best', audio_only=False):
    """Download video from YouTube"""
    try:
        # Create temporary directory for cloud deployment
        import tempfile
        downloads_dir = Path(tempfile.gettempdir()) / "YouTube_Downloads"
        downloads_dir.mkdir(parents=True, exist_ok=True)
        
        if audio_only:
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
                'outtmpl': str(downloads_dir / '%(title)s.%(ext)s'),
            }
        else:
            if quality == 'best':
                format_selector = 'best[ext=mp4][height<=1080]/best[height<=1080]/best'
            elif quality == 'medium':
                format_selector = 'best[ext=mp4][height<=720]/best[height<=720]/best'
            else:  # low
                format_selector = 'best[ext=mp4][height<=480]/best[height<=480]/best'
                
            ydl_opts = {
                'format': format_selector,
                'outtmpl': str(downloads_dir / '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
            }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        return True, str(downloads_dir)
    except Exception as e:
        return False, str(e)

def format_duration(seconds):
    """Convert seconds to readable format"""
    if seconds:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    return "Unknown"

def format_views(views):
    """Format view count"""
    if views:
        if views >= 1000000:
            return f"{views/1000000:.1f}M views"
        elif views >= 1000:
            return f"{views/1000:.1f}K views"
        else:
            return f"{views} views"
    return "Unknown views"

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">📹 YouTube Video Downloader</h1>', unsafe_allow_html=True)
    
    # Description
    st.markdown("""
    <div style="text-align: center; margin-bottom: 1rem; padding: 0 1rem;">
        <p style="font-size: clamp(0.9rem, 3vw, 1.2rem); color: #666; line-height: 1.4;">
            Download YouTube videos and audio with ease! Simply paste the URL and choose your preferred format.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # URL input section
    st.markdown('<div class="download-section">', unsafe_allow_html=True)
    
    url = st.text_input(
        "🔗 Enter YouTube URL:",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste the YouTube video URL here"
    )
    
    # Use responsive columns that stack on mobile
    col1, col2 = st.columns([1, 1])
    
    with col1:
        download_type = st.selectbox(
            "📁 Download Type:",
            ["Video", "Audio Only"],
            help="Choose whether to download video or audio only"
        )
    
    with col2:
        if download_type == "Video":
            quality = st.selectbox(
                "🎥 Video Quality:",
                ["best", "medium", "low"],
                help="Select video quality (best=1080p, medium=720p, low=480p)"
            )
        else:
            quality = "best"
            st.selectbox(
                "🎵 Audio Quality:",
                ["Best Available (M4A/WebM)"],
                disabled=True,
                help="Audio will be downloaded in best available format (M4A or WebM)"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Video preview section
    if url:
        if st.button("🔍 Preview Video Info", use_container_width=True):
            with st.spinner("Fetching video information..."):
                video_info = get_video_info(url)
                
                if video_info:
                    st.success("✅ Video found!")
                    
                    # Display video info - responsive layout
                    # On mobile, stack vertically; on desktop, side by side
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        if video_info['thumbnail']:
                            st.image(video_info['thumbnail'], use_column_width=True)
                    
                    with col2:
                        st.markdown(f"**📺 Title:** {video_info['title']}")
                        st.markdown(f"**👤 Channel:** {video_info['uploader']}")
                        st.markdown(f"**⏱️ Duration:** {format_duration(video_info['duration'])}")
                        st.markdown(f"**👁️ Views:** {format_views(video_info['view_count'])}")
                        
                        if video_info['upload_date'] != 'Unknown':
                            try:
                                date_str = video_info['upload_date']
                                formatted_date = f"{date_str[6:8]}/{date_str[4:6]}/{date_str[0:4]}"
                                st.markdown(f"**📅 Upload Date:** {formatted_date}")
                            except:
                                pass
                else:
                    st.error("❌ Could not fetch video information. Please check the URL.")
    
    # Download section
    if url:
        st.markdown("---")
        
        if st.button("⬬ Download", use_container_width=True, type="primary"):
            if not url.strip():
                st.error("Please enter a valid YouTube URL.")
                return
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔄 Starting download...")
            progress_bar.progress(25)
            
            # Download the video
            audio_only = download_type == "Audio Only"
            success, result = download_video(url, quality, audio_only)
            
            progress_bar.progress(100)
            
            if success:
                status_text.empty()
                progress_bar.empty()
                
                st.markdown(f"""
                <div class="success-message">
                    <h3>🎉 Download Completed!</h3>
                    <p><strong>📁 Downloaded to:</strong> {result}</p>
                    <p><strong>💡 Note:</strong> On Streamlit Cloud, files are temporarily stored. For permanent storage, consider running locally.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Add balloons animation
                st.balloons()
                
            else:
                status_text.empty()
                progress_bar.empty()
                
                st.markdown(f"""
                <div class="error-message">
                    <h3>❌ Download Failed</h3>
                    <p><strong>Error:</strong> {result}</p>
                    <p><strong>💡 Suggestions:</strong></p>
                    <ul>
                        <li>Check if the URL is valid and accessible</li>
                        <li>Make sure you have a stable internet connection</li>
                        <li>Try a different video quality setting</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 1rem; padding: 0 1rem;">
        <p style="font-size: clamp(0.8rem, 2.5vw, 1rem); margin-bottom: 0.5rem;">
            🚀 Built with Streamlit and yt-dlp | 
            <a href="https://github.com/yt-dlp/yt-dlp" target="_blank">yt-dlp Documentation</a>
        </p>
        <p style="font-size: clamp(0.7rem, 2vw, 0.9rem); line-height: 1.3;">
            <small>⚠️ Please respect copyright laws and YouTube's Terms of Service when downloading content.</small>
        </p>
        <p style="font-size: clamp(0.7rem, 2vw, 0.9rem); margin-top: 0.5rem;">
            <small>📱 Mobile-optimized for all devices</small>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
