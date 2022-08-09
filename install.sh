sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
sudo apt-get install libasound2-dev
sudo pip3 install pyaudio
pip install -r requirements.txt
#install usbmount (automount usb drives)
sudo sed -i "s/\(PrivateMounts *= *\).*/\1no/" /lib/systemd/system/systemd-udevd.service
apt install usbmount

#copy rc.local
cp etc/rc.local /etc/rc.local

#download a sample video file and place it as video.mp4
wget http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4 -O video.mp4