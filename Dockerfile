FROM python:3.5

RUN apt-get update \
  && apt-get -y install \
    autoconf \
    automake \
    build-essential \
    git \
    libass-dev \
    libfreetype6-dev \
    libgpac-dev \
    libmp3lame-dev \
    libopus-dev \
    libssl-dev \
    libtheora-dev \
    libtool \
    libvorbis-dev \
    openssl \
    pkg-config \
    texinfo \
    yasm \
    zlib1g-dev \
  && rm -rf /var/lib/apt/lists/*

# Install fdk-aac
RUN git clone https://github.com/mstorsjo/fdk-aac.git /tmp/fdk-aac \
  && cd /tmp/fdk-aac \
  && autoreconf -fiv \
  && ./configure --disable-shared \
  && make -j`nproc` \
  && make install \
  && make distclean \
  && cd /tmp \
  && rm -rf /tmp/fdk-aac

# Install ffmpeg
RUN git clone git://source.ffmpeg.org/ffmpeg.git /tmp/ffmpeg \
  && cd /tmp/ffmpeg \
  && ./configure \
    --disable-debug \
    --enable-small \
    --extra-libs=-ldl \
    --enable-gpl \
    --enable-libass \
    --enable-libfdk-aac \
    --enable-libmp3lame \
    --enable-libopus \
    --enable-libtheora \
    --enable-libvorbis \
    --enable-nonfree \
    --enable-openssl \
  && make -j`nproc` \
  && make install \
  && make distclean \
  && cd /tmp \
  && rm -rf /tmp/ffmpeg

COPY . /
RUN pip install -r requirements.txt \
  && rm -rf requirements.txt \
  && pip install git+https://github.com/Rapptz/discord.py@329f916e10d2f40cae7e2039269b9e3f7ecd71cc

ENTRYPOINT ["python", "-m", "discobot"]
