FROM python:3.10

WORKDIR /app
COPY . .
# RUN apt-get update && apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
RUN apt-get update && apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 libgirepository1.0-dev
RUN pip3 install -U pip
RUN pip3 install -r /app/requirements.txt
CMD sleep infinity
