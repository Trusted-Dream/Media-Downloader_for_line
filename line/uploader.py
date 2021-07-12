import setting as s
import math
import os
from mutagen.mp3 import MP3
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from line.messenger import push_message

os.chdir('/json')

# GoogleDrive認証設定
gauth = GoogleAuth()
gauth.CommandLineAuth()
drive = GoogleDrive(gauth)

# GoogleDrive共有フォルダID
MUSIC_FOLDER_ID = s.MUSIC_FOLDER_ID
VIDEO_FOLDER_ID = s.VIDEO_FOLDER_ID

# コンテンツ
def uploader(get_id,file_name,tag,dl_dir,line_bot_api):
    video_ext_dicts = {
        '.mp4':'video/mp4',
        '.webm':'video/webm',
        '.mkv':'video/x-matroska'
    }
    title = file_name.strip(dl_dir + r"\\")
    if tag == "/mp3":
        f = drive.CreateFile(
            {
            'title': title,
            'mimeType': 'audio/mpeg',
            'parents': 
                [{'kind': 'drive#fileLink', 'id':MUSIC_FOLDER_ID}]
            }
        )
        file_length = MP3(file_name).info.length
        dur = math.floor(file_length * 1000)
    else:
        dur = None
        root, ext = os.path.splitext(file_name)
        mimeType = video_ext_dicts.get(ext)

        f = drive.CreateFile(
            {
            'title': title,
            'mimeType': mimeType,
            'parents': 
                [{'kind': 'drive#fileLink', 'id':VIDEO_FOLDER_ID}]
            }
        )

    f.SetContentFile(dl_dir + f['title'])
    # GoogleDriveにアップロード
    f.Upload()

    # GoogleDriveのファイルIDを取得
    file_id = drive.ListFile(
        {'q': 'title =\"' + title +  '\"'}
    ).GetList()[0]['id']
    
    link = "https://drive.google.com/uc?export=view&id=" + file_id
    push_message(link,get_id,tag,title,dur,line_bot_api)