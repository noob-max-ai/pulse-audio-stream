# Pulse Audio Control Panel

## Requirements
* `sudo apt install ffmpeg`
* pactl (already installed)


## Download 
* Download the `AppImage` from release page
 ![Here](https://github.com/noob-max-ai/pulse-audio-stream/releases/tag/0.6)
* `chmod +x PulseAudioStream.AppImage`
* Run using `./PulseAudioStream.AppImage`.


## Use Android as Extended Speakers
* Install PulseDroid.apk from https://github.com/dront78/PulseDroid
  or 
  https://github.com/dront78/PulseDroid/blob/master/bin/PulseDroid.apk
* Start `./PulseControl.AppImage`. 
* In `Pulse Audio Server` menu, select an output source to capture from and
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
* Now the mic will be available to all ubuntu apps.
 
## Special Thanks to
* MatthiasCoppens/pulseaudio-virtualmic 

## Tested on 
* Ubuntu 20.04
* Ubuntu 20.04 VM
* Manjaro 20.1.2
 
