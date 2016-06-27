# MCD

## How to use
First make sure [Docker](https://www.docker.com/) is installed.

To run, simply mount the local directory containing .mcd files (for example "~/mea_recordings") to the container's /data directory.

`docker run -v ~/mea_recordings:/data --rm tbenst/mcd`

The image will recursively look for .mcd files and convert the electrical channels to .raw. The analog channels will be processed separately into a .analog channel. This design choice makes it easy to run spike sorting software like [Spyking Circus](spyking-circus.readthedocs.org/en/latest/) on the .raw file, while retaining the analog channels for analysis.

The `--rm` flag will remove the mcd docker container when it is finished. Note that the docker image remains local.

## Developers

### To build

```
docker run -d --name display -e VNC_PASSWORD=newPW -p 5900:5900 suchja/x11server
docker build -t tbenst/mcd:latest .
docker run -it --link display:xserver --volumes-from display -v ~/Desktop/test:/data tbenst/mcd /bin/bash
```

Connect to the VNC session using e.g. Screen Sharing on Mac OS X. `hostname: 0.0.0.0:5900`, `password:newPW`

Continue setup in container shell:
```
wine wineboot --init && wine /src/MC_DataTool-2.6.15.exe
```



Now install using the GUI. Exit bash after install finishes.

Commit changes to image, changing author field and adding CMD:
docker commit -m "updated" -c "CMD python3 /src/mcd_helper.py" cbeaaf55ba4f tbenst/mcd:latest


### To update
```
docker run -it -v ~/Desktop/test:/data tbenst/mcd /bin/bash
docker cp mcd_helper.py cbeaaf55ba4f:/src/
docker commit -m "updated" -a "Tyler Benster" -c "CMD python3 /src/mcd_helper.py" cbeaaf55ba4f tbenst/mcd:latest
```

## Legal Notice

Please note that MC_Datatool is proprietary software. Please see the following [manual](http://www.multichannelsystems.com/sites/multichannelsystems.com/files/documents/manuals/MC_Rack_Manual.pdf) for its terms of use. No license is provided for MC_DataTool and no restrictions are made in the manual on the distribution of the software. However, "no actions can be taken to decompile, reverse engineer, or otherwise attempt to discover the source code of the software."

The executable file packaged here is identical to this [download link](http://download.multichannelsystems.com/download_data/software/mc_datatool/MC_DataTool-2.6.15.exe).
