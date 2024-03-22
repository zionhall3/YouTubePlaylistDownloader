from pytube import YouTube
from pytube import Playlist
import os
import pathlib
import moviepy.editor as mp
import re

current_folder = os.getcwd()
#print(current_folder)

playlist_link_input = input("Enter playlist link: ")
playlist = Playlist(playlist_link_input)


album_folder = input("Enter a name for the album:")
#Lets user name the folder for the music.

new_album_path = str(fr"{current_folder}\{album_folder}")
#Turns the folder name and its path into a string.

isdir = os.path.isdir(new_album_path)
#Checks if the folder already exists

if isdir == False:
   new_album = os.mkdir(album_folder)
   folder = new_album_path
else:
   album_folder = input("Sorry. That name is taken. Try a new name:")

#Saves the path to wherever the current directory is as a string variable.

#prints each video url, which is the same as iterating through playlist.video_urls
for url in playlist:
    print(url)
#prints address of each YouTube object in the playlist
for vid in playlist.videos:
    print(vid)

for url in playlist:
   YouTube(url).streams.filter(only_audio=True).first().download(folder)

for url in playlist:
    YouTube(url).streams.first().download()

for file in os.listdir(folder):
  if re.search('mp4', file):
    mp4_path = os.path.join(folder,file)
    mp3_path = os.path.join(folder,os.path.splitext(file)[0]+'.mp3')
    new_file = mp.AudioFileClip(mp4_path)
    new_file.write_audiofile(mp3_path)
    os.remove(mp4_path)