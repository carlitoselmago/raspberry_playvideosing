#import sounddevice as sd
import numpy as np
import configparser
import vlc
import sys
import os
import alsaaudio, time, audioop

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
time.sleep(2)
media_player.set_pause(1)

videolen=media_player.get_length()
print("videolen",videolen)

#start audio listening ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

# Open the device in nonblocking capture mode. The last argument could
# just as well have been zero for blocking mode. Then we could have
# left out the sleep call in the bottom of the loop
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)

# Set attributes: Mono, 8000 Hz, 16 bit little endian samples
inp.setchannels(1)
inp.setrate(8000)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# The period size controls the internal number of frames per period.
# The significance of this parameter is documented in the ALSA api.
# For our purposes, it is suficcient to know that reads from the device
# will return this many frames. Each frame being 2 bytes long.
# This means that the reads below will return either 320 bytes of data
# or 0 bytes of data. The latter is possible because we are in nonblocking
# mode.
inp.setperiodsize(160)

while True:
    try:
        # Read data from device
        l,data = inp.read()
        if l:
            # Return the maximum of the absolute value of all samples in a fragment.
            #print (audioop.max(data, 2))
            volume_norm=int(audioop.max(data, 2)/100)
            #print ("|" * volume_norm)

            if volume_norm>volumethreshold:
                singing_decay=decay
                singing=True
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
                #print("DO STUFF",singing_decay)

                #check for video loop
                remaining=videolen-media_player.get_time()
                if remaining<200: 
                    #if remaining is less than 200ms (rarelly gives 0ms)
                    media_player.set_time(1)
                    
            else:
                if media_player.is_playing():
                    #pause video 
                    media_player.set_pause(1)
    except:
        media_player = vlc.MediaPlayer()
 
        # media object
        media = vlc.Media(video)
        
        # setting media to the media player
        media_player.set_media(media)
        current=media_player.get_time()
        print("error while true, current:",current)


    time.sleep(.001) #increase this in case of lower cpu specs
