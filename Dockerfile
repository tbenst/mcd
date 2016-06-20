FROM suchja/wine

USER root
RUN mkdir /src
COPY mcd_helper.py /src/
COPY MC_DataTool-2.6.15.exe /src/
RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
				wine \
                wine32 \
				python3 \
		&& rm -rf /var/lib/apt/lists/*

USER xclient

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
