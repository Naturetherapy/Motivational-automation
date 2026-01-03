import os
import json
import requests

# data.json se info nikalna
with open('data.json') as f:
    data = json.load(f)

# Image aur Music download karna
with open('bg.jpg', 'wb') as f:
    f.write(requests.get(data['image_url']).content)
with open('music.mp3', 'wb') as f:
    f.write(requests.get(data['music_url']).content)

# FFmpeg Command: Image + Music + Text "Lucas Hart"
cmd = (
    f'ffmpeg -loop 1 -i bg.jpg -i music.mp3 -t 8 -vf '
    f'"drawtext=text=\'{data["quote"]}\':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=(h-text_h)/2,'
    f'drawtext=text=\'Lucas Hart\':fontcolor=yellow:fontsize=30:x=(w-text_w)/2:y=h-100" '
    f'-pix_fmt yuv420p output.mp4 -y'
)
os.system(cmd)
