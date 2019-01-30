# GPMDPinfo

Only supports MacOS and Linux platforms for now
I might work on Windows if there's any personal need or external demand

Originally designed to be called in polybar and my zsh powerline.
The plugin version can be used in any command launcher (Argos in Gnome, BitBar on MacOs, Command Output on KDE)


## Usage

With no options passed, will just print the current playing song, if GPMDP is running and a song playing.

```bash
python3 gpmdpinfo.py {options}
```

ex:

 ```bash
 python3 gpmdpinfo.py
  Tell Me Why (Remastered Version), Neil Young, After The Gold Rush | 0:05/2:57
 ```

### Options

"cont" will continuously display the song info

"clear" will clear the terminal every loop

"rotate" song info will rotate from right to left.

"shorttime" only display the current time playing time

"notime" doesn't display the time.

"short" displays only the 20 first chars on the song info

To limit the size of the output, an integer can be passed.