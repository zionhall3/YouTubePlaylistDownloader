from pytube import YouTube
from pytube import Playlist
import os
from tkinter import *
import moviepy.editor as mp
import re


from tkinter import *
 
root = Tk()
root.geometry("300x300")
root.title(" YouTube Playlist Downloader ")
 
def StartConversion():
    PLAYLISTINPUT = playlisttxt.get("1.0", "end-1c")
    ALBUMINPUT = albumtxt.get("1.0", "end-1c")
    print(PLAYLISTINPUT, ALBUMINPUT)

    current_folder = os.getcwd()
    #print(current_folder)

    playlist_link_input = PLAYLISTINPUT
    playlist = Playlist(playlist_link_input)

    #Lets user name the folder for the music.

    new_album_path = str(fr"{current_folder}\{ALBUMINPUT}")
    #Turns the folder name and its path into a string.

    isdir = os.path.isdir(new_album_path)
    #Checks if the folder already exists

    if isdir == False:
        os.mkdir(ALBUMINPUT)
        folder = new_album_path
    else:
        ALBUMINPUT = input("Sorry. That name is taken. Try a new name:")

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
     
l1 = Label(text = "Enter your playlist link:")
playlisttxt = Text(root, height = 5,
                width = 25,
                bg = "light yellow")

l2 = Label(text = "Enter your album name:")
albumtxt = Text(root, height = 5,
                width = 25,
                bg = "light yellow")
                
 
Display = Button(root, height = 2,
                 width = 20,
                 text= "Start Conversion", 
                 command = lambda:StartConversion())
   


l1.pack()
playlisttxt.pack()
l2.pack()
albumtxt.pack()
Display.pack()
 
mainloop()

