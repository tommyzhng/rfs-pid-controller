import os
import signal
import sys


def signal_handler(sig, frame):
    print("Ctrl+C pressed! Executing cleanup...")
    os.system("adb shell wm size reset")
    sys.exit(0)

# Register the signal handler function
signal.signal(signal.SIGINT, signal_handler)

adbSize = "adb shell wm size 1080x1920"
startcmd = "scrcpy --video-codec=h264 --video-bit-rate=12M --max-fps=30"

os.system(adbSize)
os.system(startcmd)

#cd C:\Users\tommy\Documents\Code\Python\RFS-AI & python start.py