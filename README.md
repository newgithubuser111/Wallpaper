# Wallpaper
Wallpaper Rotator Script

This Python script automatically fetches and rotates 4K wallpapers from multiple sources like Reddit (e.g., r/wallpaper) and local Gruvbox-themed collections. The wallpapers are resized to fit your screen resolution and applied to both the desktop background and lock screen. The script supports multi-monitor setups and allows customization of the wallpaper change interval and download location.

Features

    Fetch Wallpapers from Reddit: Automatically grab wallpapers from subreddits like r/wallpaper, r/EarthPorn, or any subreddit of your choice.
    Local Gruvbox Theme Support: Use a collection of Gruvbox light/dark-themed wallpapers stored on your machine.
    Resize Modes: Choose from fit, fill, or stretch modes to ensure wallpapers adapt properly to your screen resolution.
    Multi-Monitor Support: Apply wallpapers across multiple monitors.
    Customizable Interval: Set the interval at which wallpapers are changed (in seconds).
    Light/Dark Mode: Automatically switch between light and dark-themed wallpapers based on the time of day.

 Requirements

Before running the script, make sure you have the following installed:

    Python 3.x
    Required Python libraries:
      pip install praw pillow requests

SETUP

  1. Clone the Repository

bash

git clone https://github.com/yourusername/wallpaper-rotator-script.git
cd wallpaper-rotator-script

2. Get Reddit API Credentials

To fetch wallpapers from Reddit, you'll need to create a Reddit application to obtain a Client ID and Client Secret. Follow these steps:

    Go to Reddit App Preferences while logged into Reddit.
    Create a new application and select "script" as the app type.
    Set http://localhost:8000 as the redirect URI.
    Copy the Client ID and Client Secret from the app.

3. Set Up the Script

Open the wallpaper_rotator.py script and replace the placeholders with your Client ID and Client Secret:

python

reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                     client_secret='YOUR_CLIENT_SECRET',
                     user_agent='wallpaper_script')

4. (Optional) Prepare Gruvbox Wallpapers

If you want to use local Gruvbox-themed wallpapers:

    Create a directory called gruvbox_wallpapers (or your preferred name).
    Store your light mode wallpapers in gruvbox_wallpapers_light and dark mode wallpapers in gruvbox_wallpapers_dark.

Usage

Run the script with the following command:

bash

python wallpaper_rotator.py

When prompted, you can configure the following options:

    Source: Choose reddit to fetch wallpapers from Reddit or gruvbox for local themed wallpapers.
    Subreddit: If using Reddit, specify the subreddit for fetching wallpapers (e.g., wallpaper, EarthPorn).
    Download Location: Specify where downloaded wallpapers will be saved.
    Interval: Set the time interval (in seconds) for changing wallpapers.
    Gruvbox Directory: If using local Gruvbox wallpapers, specify the folder containing your light/dark mode images.
    Resize Mode: Choose fit, fill, or stretch to define how the wallpaper adapts to your screen resolution.

Example Input

bash
    
    Enter 'reddit' for Reddit wallpapers or 'gruvbox' for local Gruvbox wallpapers: reddit
    Enter the subreddit to fetch wallpapers from (default is 'wallpaper'): EarthPorn
    Enter the folder where wallpapers will be saved (default is 'wallpapers'): my_wallpapers
    Enter the time interval in seconds for wallpaper changes (default is 1800 seconds): 3600
    Enter the folder for Gruvbox wallpapers (default is 'gruvbox_wallpapers'): gruvbox_wallpapers
    Enter 'fit', 'fill', or 'stretch' for wallpaper resizing (default is 'fill'): fill

Modes

    Fit: Resizes the wallpaper to fit the screen without cropping, but may leave empty space.
    Fill: Crops and resizes the wallpaper to fill the entire screen, ensuring no distortion.
    Stretch: Stretches the wallpaper to fill the screen but may cause distortion.

Multi-Monitor Setup
    
    The script automatically detects multi-monitor setups and applies wallpapers across all screens. The resizing mode is applied based on the resolution of each monitor.
    Customization
    
        Custom Subreddits: You can fetch wallpapers from any subreddit that contains images, such as r/EarthPorn, r/Art, or r/spaceporn.
        Light/Dark Mode: For Gruvbox-themed wallpapers, the script will automatically switch between gruvbox_wallpapers_light and gruvbox_wallpapers_dark based on the time of day (morning or evening).

Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request with improvements.

    Fork the project
    Create your feature branch (git checkout -b feature/new-feature)
    Commit your changes (git commit -am 'Add new feature')
    Push to the branch (git push origin feature/new-feature)
    Open a pull request

A WORD OF CAUTION NONE OF THIS CODE OR THIS README FILE WAS WRITTEN BY ME IT WAS ALL CHATGPT . I JUST WANTED TO SHARE THIS COOL SCRIPT I HAVE NO IDEA ABOUT LISCENSE OR ANYTHING. 

FEEL FREE TO IMPROVE THIS AS YOU SEE FIT. 

Thanks for reading.
