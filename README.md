# otto_robotto
Home server executor that takes direction from dropbox, neato

## What does otto robotto allow you to do?
Run otto on a server you wish to control remotely using dropbox to pass commands to and execute

Once otto is running simply edit the commands.conf file and give it one of the pre-determined commands to run (see below)

You can also execute custom commands if you define them in otto.conf on the server, this is to prevent someone from maliciously executing commands on your server should they get access to your dropbox a/c.

Data from otto can be retrieved by using the log command which returns the full log file to dropbox

## Setup
pip install -r requirements.txt

## Running
```
sudo python otto.py
ctrl-z (this pauses application)
bg (this resume application in background)
```

## Requirements
You will need to have a dropbox account

API access can be found here: https://www.dropbox.com/developers/apps

To download torrents you will need to download libtorrent

## Libtorrent
###Ubuntu command
```
sudo apt-get install python-libtorrent
```

###Windows Install
```
grab msi from here: http://sourceforge.net/projects/libtorrent/files/py-libtorrent/
```
## Standard commands
###tor   
```
tor http://www.url.com/torrentname.torrent
```
###com
This allows execution of extra commands written in otto.conf (see below for examples)
```
com 1
```
###mag
Download a magnet link to the TORRENT_DIR that was specified at first run (can be changed in otto.conf)
```
mag magnet:?xt=urn:btih:A89911197425F048EE1FDFA11D6DFABB15ADDEEF&dn=filenameblablabla&tr=udp://tracker.trackersite.tk:6969/announce
```
###log
Returns the log file to your dropbox account, this is handy to see progress of downloads and also results of commands executed with com command
```
log
```
###exit
Shuts otto down, WARNING: this means you will need to start it manually again
```
exit
```
###reload
Reloads otto.conf
```
reload
```
###magtv
Same as mag except downloads to TORRENT_DIR/tv
```
mag magnet:?xt=urn:btih:A89911197425F048EE1FDFA11D6DFABB15ADDEEF&dn=filenameblablabla&tr=udp://tracker.trackersite.tk:6969/announce
```
###magmovie
Same as mag except downloads to TORRENT_TV/movies
```
mag magnet:?xt=urn:btih:A89911197425F048EE1FDFA11D6DFABB15ADDEEF&dn=filenameblablabla&tr=udp://tracker.trackersite.tk:6969/announce
```


## Adding extra commands
The otto.conf file which is generate after first run of the application contains a section called 'commands'

The commands section is in the syntax: command = command including arguments e.g.
```
1 = ls -lah
```
to execute the command 1 above, you would type the following into the commands.conf
```
com 1
```
this will execute 
```
ls -lah
``` 
on the operating system running otto, the results will be put into the log file which can be retrieved to dropbox by entering
```
log
``` 
into commands.conf