import subprocess
import psutil

date = "date"
date_output = subprocess.check_output(date)

print("Video_started at: ", date_output.decode("utf-8"))

gs = "gst-launch-1.0 v4l2src device=/dev/video0 ! video/x-raw, format=I420, width=320, height=240, framerate=30/1 ! rtpvrawpay ! udpsink host=192.168.0.133 port=5000"

subprocess.run(gs, shell=True, stdin=subprocess.PIPE)
