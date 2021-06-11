# Pulse Audio Control Panel

## Requirements
* `sudo apt install ffmpeg`
* pactl (already installed)

## Use Android as Extended Speakers
* Install PulseDroid.apk from https://github.com/dront78/PulseDroid
  or
  https://github.com/dront78/PulseDroid/blob/master/bin/PulseDroid.apk
* Start `./PulseControl.AppImage`. 
* In `Pulse Audio Server` menu select an output source to capture from and
  click start. It'll show the ip to connect to.
* Enter the ip and port in PulseDroid app and hit play.
* If you can't hear the audio, stop the server and change output source.


## Use Android as mic

* Download IP webcam and start it as an audio server (disable video for battery life).
  When you start server, note the ip and port,
* Enter the path to `IP Webcam` audio source in the text entry in the format
  http://192.168.10.7:8080/audio.opus
  http://<ip address>:<port>/audio.opus
* Hit `start server` 


## Special Thanks to
* MatthiasCoppens/pulseaudio-virtualmic 

## Tested on 
* Ubuntu 20.04
* Ubuntu 20.04 VM

