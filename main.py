import os, random, requests
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import yt_dlp

# 1. YouTube se Automatic Piano Music Search aur Download karna
def get_youtube_music():
    # 'ytsearch1' ka matlab hai ki YouTube par search karke pehla result uthao
    search_query = "ytsearch1:No Copyright Motivational Piano Audio Library"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])
    return "music.mp3"

# 2. Gemini se Quotes aur Pexels se Video (Wahi logic)
def get_assets():
    v_headers = {"Authorization": os.getenv('PEXELS_API_KEY')}
    v_url = "https://api.pexels.com/videos/search?query=scenic+nature&orientation=portrait&per_page=15"
    v_res = requests.get(v_url, headers=v_headers).json()
    v_link = random.choice(v_res['videos'])['video_files'][0]['link']
    with open("bg.mp4", 'wb') as f: f.write(requests.get(v_link).content)

def get_quote():
    api_key = os.getenv('GEMINI_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts":[{"text": "Write a deep, 1-sentence motivational quote about inner peace."}]}]}
    res = requests.post(url, json=payload).json()
    return res['candidates'][0]['content']['parts'][0]['text']

# 3. Merging Everything
def create_video(quote):
    video = VideoFileClip("bg.mp4").subclip(0, 10)
    audio = AudioFileClip("music.mp3").subclip(0, 10) # Sirf 10 sec cut karega
    
    txt = TextClip(quote, fontsize=50, color='white', font='Arial-Bold', 
                   method='caption', size=(video.w*0.8, None)).set_duration(10).set_pos('center')
    
    final = CompositeVideoClip([video, txt]).set_audio(audio.volumex(0.4))
    final.write_videofile("final_video.mp4", fps=24, codec="libx264")

# 4. Upload to Catbox & Send to Telegram
def post_to_tg():
    with open("final_video.mp4", "rb") as f:
        link = requests.post("https://catbox.moe/user/api.php", data={"reqtype": "fileupload"}, files={"fileToUpload": f}).text
    
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": f"New Piano Motivation: {link}"})

if __name__ == "__main__":
    get_youtube_music()
    get_assets()
    q = get_quote()
    create_video(q)
    post_to_tg()
