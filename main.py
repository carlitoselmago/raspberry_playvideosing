import sounddevice as sd
import numpy as np
import configparser
import vlc
import sys
import os

#load settings
config = configparser.ConfigParser()
config.read('config.ini')
volumethreshold=int(config["DEFAULT"]["volumethreshold"])
decay=int(config["DEFAULT"]["decay"])

singing_decay=0
singing=False

video="video.mp4"

if not os.path.isfile(video):
    print("ERROR: file ",video,"not found")
    sys.exit()

#video part 
# creating vlc media player object
media_player = vlc.MediaPlayer()
 
# media object
media = vlc.Media(video)
 
# setting media to the media player
media_player.set_media(media)

media_player.play()
media_player.set_pause(1)

def manage_sound(indata, outdata, frames, time, status):
    global singing_decay
    global decay
    global volumethreshold
    global singing

    volume_norm = np.linalg.norm(indata)*10
    if volume_norm>volumethreshold:
        singing_decay=decay
    else:
        if singing_decay>0:
            singing_decay-=1
            singing=True
        else:
            singing=False
    #print ("|" * int(volume_norm))

    if singing:
        # start playing video
        if not media_player.is_playing():
            media_player.play()
        print("DO STUFF",singing_decay)
    else:
        if media_player.is_playing():
            media_player.set_pause(1)
   

with sd.Stream(callback=manage_sound):
    sd.sleep(31536000 * 1000) #milliseconds