from pytubefix import YouTube, extract, Playlist
#from pytube import YouTube, extract
#from pytube import Playlist
#Try using pytubefix or install the newer working fork until further notice.
#pip install pytubefix
#pip uninstall pytube
#pip install git+https://github.com/kszczepanskidev/pytube
#Make sure to log out of your YT account so you aren't detected as a bot.
import os
from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import moviepy.editor as mp
import re
import eyed3
import moviepy.video.io.VideoFileClip as VFClip
from pythumb import Thumbnail

output_folder = ""

folder_selected = False

root = Tk()
root.resizable(width=False, height=False)
#Keeps window at a small compact size
root.title(" YouTube Playlist Downloader ")
 
def StartConversion():
    print(folder_selected)
    PLAYLISTINPUT = playlisttxt.get("1.0", "end-1c")

    playlist_link_input = PLAYLISTINPUT
    playlist = Playlist(playlist_link_input)
    #Gets text input and converts it into a Playlist object

    if playlist_link_input == "":
        messagebox.showerror("Error", "Please enter a playlist URL")
        return
    elif "youtu" not in playlist_link_input:
         messagebox.showerror("Error", "Please enter a valid YouTube URL")
         return
    elif folder_selected == False:
        messagebox.showerror("Error", "Please select an output folder")
        return
    #Returns errors to make sure folders are selected and there is a link.
    
    if "playlist" not in playlist_link_input:
         #For single song downloads. Needs work as of now.
         video = YouTube(playlist_link_input)
         vid_id = extract.video_id(playlist_link_input)
         thumbnail = Thumbnail(f"https://youtu.be/{vid_id}")
         video.streams.filter().first().download(output_folder)
         thumbnail.fetch(size="maxresdefault")
         thumbnail.save(output_folder, "album_art_file", overwrite=True)
         album_art_path = os.path.join(output_folder, "album_art_file.jpg")
         mp4_path = os.path.join(output_folder, f"{video.title}.mp4")
         mp3_path = os.path.join(output_folder, os.path.splitext(video.title)[0]+'.mp3')
         new_file = mp.AudioFileClip(mp4_path)
         new_file.write_audiofile(mp3_path)
         mp3_filename = os.path.basename(mp3_path)
         selected_music_file = os.path.join(output_folder, mp3_filename)
         no_art_file = eyed3.load(selected_music_file)
         no_art_file.tag.images.set(3, open(album_art_path, 'rb').read(), 'image/jpg')
         no_art_file.tag.save()
         with VFClip.VideoFileClip(mp4_path) as opened_mp4:
          pass
         #This opens and closes the video path file to prevent any Permission Errors.
         try:
              os.remove(mp4_path)
         except PermissionError:
               print("Permission Error")
         os.remove(album_art_path)
         progress.set(100)
         if progressbar.step(100):
          messagebox.showinfo("Finished!", "The song is done downlading and converting!")
          os.startfile(output_folder)
          return
         progressbar.update()
    
    else:
     for i, url in enumerate(playlist, 1):
          #For actual playlist downloads. Mostly works. Still working on bugfixing.
          total_videos = len(playlist.video_urls)
          progress_step = 100 / total_videos
          video = YouTube(url)
          vid_id = extract.video_id(url)
          thumbnail = Thumbnail(f"https://youtu.be/{vid_id}")
          video.streams.filter().first().download(output_folder)
          #only_audio = True filter removed so that the VideoFileClip module doesn't need any fps values and return a KeyError
          for file in os.listdir(output_folder):
               if re.search('mp4', file):
                    progress.set(progress.get() + progress_step)
                    thumbnail.fetch(size="maxresdefault")
                    thumbnail.save(output_folder, "album_art_file", overwrite=True)
                    #Downloads the thumbnail as a file so it can be applied as album art so the music is less boring and bland on your phone or media player.
                    album_art_path = os.path.join(output_folder, "album_art_file.jpg")
                    mp4_path = os.path.join(output_folder, file)
                    mp3_path = os.path.join(output_folder, os.path.splitext(file)[0]+'.mp3')
                    new_file = mp.AudioFileClip(mp4_path)
                    new_file.write_audiofile(mp3_path)
                    mp3_filename = os.path.basename(mp3_path)
                    selected_music_file = os.path.join(output_folder, mp3_filename)
                    no_art_file = eyed3.load(selected_music_file)
                    no_art_file.tag.images.set(3, open(album_art_path, 'rb').read(), 'image/jpg')
                    no_art_file.tag.save()
                    #This numbers the songs in the order of the playlist.
                    if i < 10:
                         original_file_path = os.path.join(output_folder, mp3_filename)
                         numbered_file_name = f"00{i}_{mp3_filename}"
                         numbered_file_path = os.path.join(output_folder, numbered_file_name)
                         if os.path.exists(numbered_file_path):
                              os.remove(numbered_file_path)
                         os.rename(original_file_path, numbered_file_path)
                    elif 100 > i >= 10:
                         original_file_path = os.path.join(output_folder, mp3_filename)
                         numbered_file_name = f"0{i}_{mp3_filename}"
                         numbered_file_path = os.path.join(output_folder, numbered_file_name)
                         if os.path.exists(numbered_file_path):
                              os.remove(numbered_file_path)
                         os.rename(original_file_path, numbered_file_path)
                    else:
                         original_file_path = os.path.join(output_folder, mp3_filename)
                         numbered_file_name = f"{i}_{mp3_filename}"
                         numbered_file_path = os.path.join(output_folder, numbered_file_name)
                         if os.path.exists(numbered_file_path):
                              os.remove(numbered_file_path)
                         os.rename(original_file_path, numbered_file_path)
                    with VFClip.VideoFileClip(mp4_path) as opened_mp4:
                         pass
                    #This opens and closes the video path file to prevent any Permission Errors.
                    try:
                         os.remove(mp4_path)
                    except PermissionError:
                         print("Permission Error")
                    os.remove(album_art_path)
                    if progressbar.step(99.9):
                         #Need to get the progress bar to fill up completely and send a message when it's done.
                         messagebox.showinfo("Finished!", "The playlist is done downlading and converting!")
                         os.startfile(output_folder)
                         return
                    progressbar.update()


Folder_Button_Text1 = "Please select a folder"
Folder_Button_Text2 = "Folder has been selected"

def select_folder():
        global output_folder
        output_folder = filedialog.askdirectory()
        global folder_selected
        folder_selected = True
        folder_button.config(text=Folder_Button_Text2)
     
l1 = Label(text = "Enter your playlist link:")
playlisttxt = Text(root, height = 1,
                width = 25,
                bg = "light yellow")
                

folder_button = Button(root, height = 2,
                 width = 20,
                 text= Folder_Button_Text1, 
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