import os
import requests
import time
import random
import ctypes
from PIL import Image
import praw
import platform
from io import BytesIO
from datetime import datetime

# Configure Reddit API (replace with your credentials)
reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                     client_secret='YOUR_CLIENT_SECRET',
                     user_agent='wallpaper_script')

# Get screen resolution (works for both Windows and Linux)
def get_screen_resolution():
    """Return the screen resolution based on the operating system."""
    try:
        if platform.system() == "Windows":
            user32 = ctypes.windll.user32
            screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        elif platform.system() == "Linux":
            result = os.popen("xrandr | grep '*' | awk '{print $1}'").read()
            screensize = tuple(map(int, result.strip().split('x')))
        else:
            screensize = (2560, 1440)  # Default resolution if undetected
        return screensize
    except Exception as e:
        print(f"Error getting screen resolution: {e}")
        return (2560, 1440)

# Fetch a random Reddit wallpaper
def fetch_reddit_wallpaper(subreddit='wallpaper'):
    """Fetch a random wallpaper URL from a subreddit."""
    wallpapers = []
    try:
        for submission in reddit.subreddit(subreddit).hot(limit=20):
            if submission.url.endswith(('jpg', 'jpeg', 'png')):
                wallpapers.append(submission.url)
        return random.choice(wallpapers) if wallpapers else None
    except Exception as e:
        print(f"Error fetching Reddit wallpapers: {e}")
        return None

# Get a random Gruvbox wallpaper from a local directory
def fetch_gruvbox_wallpaper(directory='gruvbox_wallpapers'):
    """Fetch a random local wallpaper from a specified directory."""
    wallpapers = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('jpg', 'jpeg', 'png'))]
    return random.choice(wallpapers) if wallpapers else None

# Determine if it is light or dark mode based on time of day
def is_light_mode():
    """Return True if current time is between 6 AM and 6 PM."""
    return 6 <= datetime.now().hour < 18

# Resize the image to fit the screen dimensions with chosen mode
def resize_image(image, screen_size, mode='fill'):
    """Resize an image based on specified mode: 'fit', 'fill', or 'stretch'."""
    try:
        img = Image.open(BytesIO(image)) if isinstance(image, bytes) else Image.open(image)
        img_ratio = img.width / img.height
        screen_ratio = screen_size[0] / screen_size[1]

        if mode == 'fit':
            if img_ratio > screen_ratio:
                new_width = screen_size[0]
                new_height = int(new_width / img_ratio)
            else:
                new_height = screen_size[1]
                new_width = int(new_height * img_ratio)
            img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)
        elif mode == 'fill':
            img_resized = img.resize(screen_size, Image.ANTIALIAS).crop((0, 0, screen_size[0], screen_size[1]))
        elif mode == 'stretch':
            img_resized = img.resize(screen_size, Image.ANTIALIAS)
        return img_resized
    except Exception as e:
        print(f"Error resizing image: {e}")
        return None

# Save image to specified location
def save_image(img, download_location='wallpapers', filename='wallpaper.jpg'):
    """Save an image to a specific directory with a given filename."""
    try:
        os.makedirs(download_location, exist_ok=True)
        filepath = os.path.join(download_location, filename)
        img.save(filepath)
        return filepath
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

# Set wallpaper on Windows
def set_wallpaper_windows(filepath):
    """Set the wallpaper on Windows using ctypes."""
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 3)
    except Exception as e:
        print(f"Error setting wallpaper on Windows: {e}")

# Set wallpaper on Linux (GNOME)
def set_wallpaper_linux(filepath):
    """Set the wallpaper on Linux using GNOME's gsettings."""
    try:
        os.system(f"gsettings set org.gnome.desktop.background picture-uri file://{filepath}")
        os.system(f"gsettings set org.gnome.desktop.screensaver picture-uri file://{filepath}")
    except Exception as e:
        print(f"Error setting wallpaper on Linux: {e}")

# Apply wallpaper based on the operating system
def apply_wallpaper(filepath):
    """Apply the wallpaper based on the operating system."""
    if platform.system() == "Windows":
        set_wallpaper_windows(filepath)
    elif platform.system() == "Linux":
        set_wallpaper_linux(filepath)

# Fetch and apply the wallpaper
def change_wallpaper(download_location, source='reddit', subreddit='wallpaper', local_directory='gruvbox_wallpapers', resize_mode='fill'):
    """Change wallpaper by fetching, resizing, and applying based on the source."""
    screen_size = get_screen_resolution()
    
    if source == 'reddit':
        wallpaper_url = fetch_reddit_wallpaper(subreddit=subreddit)
        if not wallpaper_url:
            print("No wallpaper found on Reddit.")
            return
        response = requests.get(wallpaper_url)
        image_data = response.content
    elif source == 'gruvbox':
        wallpaper_path = fetch_gruvbox_wallpaper(directory=local_directory)
        if not wallpaper_path:
            print("No local Gruvbox wallpapers found.")
            return
        image_data = wallpaper_path

    resized_image = resize_image(image_data, screen_size, mode=resize_mode)
    if not resized_image:
        print("Failed to resize the image.")
        return

    filepath = save_image(resized_image, download_location=download_location)
    if filepath:
        apply_wallpaper(filepath)
        print(f"Wallpaper set: {filepath}")

# Main loop for wallpaper rotation
def start_wallpaper_rotation(download_location, interval, source='reddit', subreddit='wallpaper', local_directory='gruvbox_wallpapers', resize_mode='fill'):
    """Run wallpaper rotation loop based on specified interval."""
    while True:
        if source == 'gruvbox':
            mode = 'light' if is_light_mode() else 'dark'
            local_directory = f"{local_directory}_{mode}"
        
        change_wallpaper(download_location, source=source, subreddit=subreddit, local_directory=local_directory, resize_mode=resize_mode)
        time.sleep(interval)

# Main function
if __name__ == '__main__':
    source = input("Enter 'reddit' for Reddit wallpapers or 'gruvbox' for local Gruvbox wallpapers: ").strip().lower()
    subreddit = input("Enter the subreddit to fetch wallpapers from (default is 'wallpaper'): ").strip() or 'wallpaper' if source == 'reddit' else None
    download_location = input("Enter the folder where wallpapers will be saved (default is 'wallpapers'): ").strip() or 'wallpapers'
    interval = int(input("Enter the time interval in seconds for wallpaper changes (default is 1800 seconds): ").strip() or 1800)
    local_directory = input("Enter the folder for Gruvbox wallpapers (default is 'gruvbox_wallpapers'): ").strip() or 'gruvbox_wallpapers'
    resize_mode = input("Enter 'fit', 'fill', or 'stretch' for wallpaper resizing (default is 'fill'): ").strip().lower() or 'fill'
    
    start_wallpaper_rotation(download_location, interval, source=source, subreddit=subreddit, local_directory=local_directory, resize_mode=resize_mode)
