from pytube import YouTube
from pytube import Playlist
import os
from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import moviepy.editor as mp
import re
import urllib3
import eyed3
import requests
import io
from PIL import Image

output_folder = ""

folder_selected = False

http = urllib3.PoolManager()

root = Tk()
root.title(" YouTube Playlist Downloader ")
 
def StartConversion():
    print(folder_selected)
    PLAYLISTINPUT = playlisttxt.get("1.0", "end-1c")

    playlist_link_input = PLAYLISTINPUT
    playlist = Playlist(playlist_link_input)

    if playlist_link_input == "":
        messagebox.showerror("Error", "Please enter a playlist URL")
        return

    elif folder_selected == False:
        messagebox.showerror("Error", "Please select an output folder")
        return

    for i, url in enumerate(playlist, 1):
        total_videos = len(playlist.video_urls)
        progress_step = 100 / total_videos
        video = YouTube(url)
        thumbnail = video.thumbnail_url
        video.streams.filter(only_audio=True).first().download(output_folder)
        for file in os.listdir(output_folder):
            if re.search('mp4', file):
                img_content = requests.get(thumbnail).content
                img_file = io.BytesIO(img_content)
                img = Image.open(img_file)
                album_art_path = os.path.join(output_folder, "album_art_file.png")
                with open (f'{output_folder}/album_art_file.png', "wb") as album_art:
                     img.save(album_art, "PNG")
                mp4_path = os.path.join(output_folder, file)
                mp3_path = os.path.join(output_folder, os.path.splitext(file)[0]+'.mp3')
                new_file = mp.AudioFileClip(mp4_path)
                new_file.write_audiofile(mp3_path)
                mp3_filename = os.path.basename(mp3_path)
                selected_music_file = os.path.join(output_folder, mp3_filename)
                no_art_file = eyed3.load(selected_music_file)
                no_art_file.tag.images.set(3, open(album_art_path, 'rb').read(), 'image/png')
                no_art_file.tag.save()
                if i < 10:
                     os.rename(os.path.join(output_folder, mp3_filename), os.path.join(output_folder, f"00{i}_{mp3_filename}"))
                elif 100 > i >= 10:
                     os.rename(os.path.join(output_folder, mp3_filename), os.path.join(output_folder, f"0{i}_{mp3_filename}"))
                else:
                     os.rename(os.path.join(output_folder, mp3_filename), os.path.join(output_folder, f"{i}_{mp3_filename}"))
                os.remove(mp4_path)
                if os.path.exists(mp3_path):
                     os.replace(mp3_path)
                os.remove(album_art_path)
                progress.set(progress.get() + progress_step)
                if progressbar.step(100):
                     messagebox.showinfo("Finished!", "The playlist is done downlading and converting!")
                     return
                progressbar.update()


def select_folder():
        global output_folder
        output_folder = filedialog.askdirectory()
        global folder_selected
        folder_selected = True
        print(folder_selected)
     
l1 = Label(text = "Enter your playlist link:")
playlisttxt = Text(root, height = 1,
                width = 25,
                bg = "light yellow")
                

folder_button = Button(root, height = 2,
                 width = 20,
                 text= "Select Folder", 
                 command = lambda:select_folder())

download_button = Button(root, height = 2,
                 width = 20,
                 text= "Download", 
                 command = lambda:StartConversion())

progress = tk.DoubleVar()
progressbar = ttk.Progressbar(variable=progress, maximum=100)
progressbar.place(x=50, y=250, width=200)
progress.set(0)


l1.pack()
playlisttxt.pack()
folder_button.pack()
download_button.pack()
progressbar.pack(fill=tk.X, padx=10, pady=5)
 
mainloop()
