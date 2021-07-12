#!/bin/env python3
import youtube_dl
import asyncio
import concurrent.futures
import os
import shutil
from glob import glob
from line.uploader import uploader
from line.messenger import push_message

class Worker(object):
    def __init__(self,tag,url,get_id,line_bot_api):
        # 並列処理に使用するプロセス数
        self.maxworker = 8
        # /mp3 /mov /nomov
        self.tag = tag
        # DL URL
        self.url = url
        # LINEのUID or GID
        self.get_id = get_id
        # LINE API
        self.line_bot_api = line_bot_api
        self.dl_dir = "/temp/download_media/"
        os.makedirs(self.dl_dir, exist_ok=True)

    # ダウンロード
    def download(self):
        # ニコニコ動画/dailymotion/tiktok/twitterはフォーマット指定なし
        noconv = set(["nicovideo","dailymotion","tiktok","twitter"])
        mov = set(["/mov","/nomov"])
        tag = self.tag

        if [x for x in noconv if x in self.url]:
            fmt = {}
        elif tag == "/mp3":
            fmt = (
                {'format':'bestaudio[ext=mp3]/bestaudio[ext=m4a]/bestaudio'}
            )
        elif tag in str(mov):
            fmt = ({'format':'bestvideo+bestaudio'})

        option = {
            'outtmpl':self.dl_dir + '%(title)s.%(ext)s',
            'restrictfilenames':'True',
            'quiet':'True',
            'default_search':'error'
        }
        # フォーマット形成
        option.update(fmt)
        try:
            with youtube_dl.YoutubeDL(option) as ydl: ydl.download([self.url])
        except Exception as e:
            return e

    # 変換処理部分
    def convert(self,data):
        ext_dict = {
            '.m4a' : ['ffmpeg -y -i "%s" -ab 256k "%s" -loglevel quiet','/mp3'],
            '.mp4' : ['ffmpeg -y -i "%s" -ab 256k "%s" -loglevel quiet','/mp3'],
            '.webm': ['ffmpeg -y -i "%s" "%s" -loglevel quiet','/mov'],
            '.mkv' : ['ffmpeg -y -i "%s" -vcodec copy "%s" -loglevel quiet','/mov'],
        }
        root, ext = os.path.splitext(data)
        formats = ext_dict.get(ext)
        if formats != None and formats[1] == self.tag:
            if ext != ".mp4" and self.tag == "/mov":
                cnv_mp4 = '%s.mp4' % root
                data = cnv_mp4
                cmd = formats[0] % (root+ext, cnv_mp4)
                os.system(cmd)
                os.remove(root+ext)
            else:
                cnv_mp3 = '%s.mp3' % root
                data = cnv_mp3
                cmd = formats[0] % (root+ext, cnv_mp3)
                os.system(cmd)
                os.remove(root+ext)
        # アップローダー
        uploader(self.get_id,data,self.tag,self.dl_dir,self.line_bot_api)

    # 並列処理
    async def multi_convert(self,loop,file_list):
        executor = concurrent.futures.ProcessPoolExecutor()
        queue = asyncio.Queue()
        [queue.put_nowait(files) for files in file_list]
        async def proc(q):
            while not q.empty():
                data = await q.get()
                future = loop.run_in_executor(executor, self.convert,data)
                await future
        tasks = [asyncio.create_task(proc(queue)) for data in range(self.maxworker)]
        return await asyncio.wait(tasks)

    def run(self):
        msg = self.download()
        if "ERROR" in str(msg):
            push_message("",self.get_id,"","ダウンロードに失敗しました。",self.url,self.line_bot_api)
            raise Exception('Download Failed')
        opt = set(["/mp3","/mov"])
        if self.tag in str(opt):
            fileExtensions = set([ "mp4", "m4a","mkv","webm"])
            file_list = []
            # DLしたファイルの拡張子の切り取り
            for ext in fileExtensions:
                file_list.extend(glob("%s*.%s" % (self.dl_dir,ext)))
            # 処理の並列化
            loop = asyncio.new_event_loop()
            loop.run_until_complete(
                self.multi_convert(loop,file_list)
            )
            shutil.rmtree(self.dl_dir)