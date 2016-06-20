# MCD

First make sure [Docker](https://www.docker.com/) is installed.

To run, simply mount the local directory containing .mcd files (for example "~/mea_recordings") to the container's /data directory.

`docker run -v ~/mea_recordings:/data tbenst/mcd`

The image will recursively look for .mcd files and convert the electrical channels to .raw. The analog channels will be processed separately into a .analog channel. This design choice makes it easy to run spike sorting software like [Spyking Circus](spyking-circus.readthedocs.org/en/latest/) on the .raw file, while retaining the analog channels for analysis.

## Developers

To build:

```
docker run -d --name display -e VNC_PASSWORD=newPW -p 5900:5900 suchja/x11server
docker build -t mcdfork .
docker run -it --link display:xserver --volumes-from display mcdfork /bin/bash
```

Connect to the VNC session using e.g. Screen Sharing on Mac OS X. `hostname: 0.0.0.0:5900`, `password:newPW`

Continue setup in container shell:
```
wine wineboot --init && wine /src/MC_DataTool-2.6.15.exe
```

Now install using the GUI. Exit bash after install finishes.

Commit changes to image, changing author field and adding ENTRYPOINT:
```
docker commit -m "installed MC_DATATOOL" -a "XXXAuthorXXX" -c "ENTRYPOINT python3 /src/mcd_helper.py" XXXContainerIDXXX mcdfork:latest
```

