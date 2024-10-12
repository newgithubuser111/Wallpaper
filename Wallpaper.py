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
    if platform.system() == "Windows":
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    elif platform.system() == "Linux":
        import subprocess
        result = subprocess.run(['xrandr', '|', 'grep', '*'], stdout=subprocess.PIPE)
        screensize = [int(x) for x in result.stdout.decode('utf-8').split()[0].split('x')]
    else:
        screensize = (2560, 1440)  # Default resolution if undetected
    return screensize

# Fetch Reddit wallpaper
def fetch_reddit_wallpaper(subreddit='wallpaper'):
    wallpapers = []
    for submission in reddit.subreddit(subreddit).hot(limit=20):
        if submission.url.endswith(('jpg', 'jpeg', 'png')):
            wallpapers.append(submission.url)
    return random.choice(wallpapers)

# Get Gruvbox wallpaper from local directory
def fetch_gruvbox_wallpaper(directory='gruvbox_wallpapers'):
    wallpapers = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(('jpg', 'jpeg', 'png'))]
    return random.choice(wallpapers)

# Detect light or dark mode based on the time of day
def is_light_mode():
    current_hour = datetime.now().hour
    return 6 <= current_hour < 18  # Light mode between 6 AM and 6 PM

# Resize image based on the chosen mode (fit, fill, or stretch)
def resize_image(image, screen_size, mode='fill'):
    img = Image.open(BytesIO(image)) if isinstance(image, bytes) else Image.open(image)
    img_ratio = img.width / img.height
    screen_ratio = screen_size[0] / screen_size[1]
    
    if mode == 'fit':
        if img_ratio > screen_ratio:
            # Fit by width
            new_width = screen_size[0]
            new_height = int(new_width / img_ratio)
        else:
            # Fit by height
            new_height = screen_size[1]
            new_width = int(new_height * img_ratio)
        img_resized = img.resize((new_width, new_height), Image.ANTIALIAS)
    elif mode == 'fill':
        img_resized = img.resize(screen_size, Image.ANTIALIAS)
        # Center crop to fill the screen without distortion
        img_resized = img_resized.crop((0, 0, screen_size[0], screen_size[1]))
    elif mode == 'stretch':
        # Stretch to exact screen dimensions (may distort)
        img_resized = img.resize(screen_size, Image.ANTIALIAS)
    
    return img_resized

# Save image to a specified location
def save_image(img, download_location='wallpapers', filename='wallpaper.jpg'):
    if not os.path.exists(download_location):
        os.makedirs(download_location)
    filepath = os.path.join(download_location, filename)
    img.save(filepath)
    return filepath

# Set wallpaper on Windows
def set_wallpaper_windows(filepath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 3)

# Set wallpaper on Linux (GNOME)
def set_wallpaper_linux(filepath):
    os.system(f"gsettings set org.gnome.desktop.background picture-uri file://{filepath}")
    os.system(f"gsettings set org.gnome.desktop.screensaver picture-uri file://{filepath}")

# Multi-monitor wallpaper support
def apply_wallpaper(filepath):
    if platform.system() == "Windows":
        set_wallpaper_windows(filepath)
    elif platform.system() == "Linux":
        set_wallpaper_linux(filepath)

# Fetch and apply the wallpaper
def change_wallpaper(download_location, source='reddit', subreddit='wallpaper', local_directory='gruvbox_wallpapers', resize_mode='fill'):
    screen_size = get_screen_resolution()
    
    # Choose source (Reddit or Gruvbox)
    if source == 'reddit':
        wallpaper_url = fetch_reddit_wallpaper(subreddit=subreddit)
        response = requests.get(wallpaper_url)
        image_data = response.content
    elif source == 'gruvbox':
        wallpaper_path = fetch_gruvbox_wallpaper(directory=local_directory)
        image_data = wallpaper_path
    
    # Resize and save based on user preference
    resized_image = resize_image(image_data, screen_size, mode=resize_mode)
    filepath = save_image(resized_image, download_location=download_location)
    
    # Apply the wallpaper
    apply_wallpaper(filepath)
    print(f"Wallpaper set: {filepath}")

# Main loop for wallpaper rotation
def start_wallpaper_rotation(download_location, interval, source='reddit', subreddit='wallpaper', local_directory='gruvbox_wallpapers', resize_mode='fill'):
    while True:
        if source == 'gruvbox':
            mode = 'light' if is_light_mode() else 'dark'
            local_directory = f"{local_directory}_{mode}"
        
        change_wallpaper(download_location, source=source, subreddit=subreddit, local_directory=local_directory, resize_mode=resize_mode)
        time.sleep(interval)

# Main function
if __name__ == '__main__':
    source = input("Enter 'reddit' for Reddit wallpapers or 'gruvbox' for local Gruvbox wallpapers: ").lower()
    if source == 'reddit':
        subreddit = input("Enter the subreddit to fetch wallpapers from (default is 'wallpaper'): ") or 'wallpaper'
    else:
        subreddit = None
    
    download_location = input("Enter the folder where wallpapers will be saved (default is 'wallpapers'): ") or 'wallpapers'
    interval = int(input("Enter the time interval in seconds for wallpaper changes (default is 1800 seconds): ") or 1800)
    local_directory = input("Enter the folder for Gruvbox wallpapers (default is 'gruvbox_wallpapers'): ") or 'gruvbox_wallpapers'
    
    # Choose resizing mode (fit, fill, or stretch)
    resize_mode = input("Enter 'fit', 'fill', or 'stretch' for wallpaper resizing (default is 'fill'): ").lower() or 'fill'
    
    start_wallpaper_rotation(download_location, interval, source=source, subreddit=subreddit, local_directory=local_directory, resize_mode=resize_mode)
