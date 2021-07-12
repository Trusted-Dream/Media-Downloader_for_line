import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN  = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
MUSIC_FOLDER_ID = os.environ.get("MUSIC_FOLDER_ID")
VIDEO_FOLDER_ID = os.environ.get("VIDEO_FOLDER_ID")