import os, random, requests
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

# 1. Gemini se Quote lena
def get_gemini_quote():
    api_key = os.getenv('GEMINI_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    prompt = {"contents": [{"parts":[{"text": "Write a deep, 1-sentence motivational quote about resilience."}]}]}
    res = requests.post(url, json=prompt).json()
    return res['candidates'][0]['content']['parts'][0]['text']

# 2. Live Internet se Assets dhoondhna (Music & Video)
def get_assets():
    # Pexels se naya video dhoondhna
    v_headers = {"Authorization": os.getenv('PEXELS_API_KEY')}
    v_url = "https://api.pexels.com/videos/search?query=nature+landscape&orientation=portrait&per_page=20"
    v_res = requests.get(v_url, headers=v_headers).json()
    v_link = random.choice(v_res['videos'])['video_files'][0]['link']
    with open("bg.mp4", 'wb') as f: f.write(requests.get(v_link).content)

    # Pixabay se Live Piano Music search aur download karna
    # Yahan hum search query dal rahe hain: "slow piano meditation"
    p_key = os.getenv('PIXABAY_API_KEY')
    m_search_url = f"https://pixabay.com/api/audio/?key={p_key}&q=slow+piano+meditation&per_page=10"
    m_res = requests.get(m_search_url).json()
    
    # Live results mein se random music uthana
    m_link = random.choice(m_res['hits'])['audio']
    with open("music.mp3", 'wb') as f: f.write(requests.get(m_link).content)

# 3. Video Merge (Aapki image jaisa style)
def create_video(quote):
    video = VideoFileClip("bg.mp4").subclip(0, 10)
    audio = AudioFileClip("music.mp3").subclip(0, 10)
    
    # White, Bold, Centered Text (Shadow ke saath)
    txt = TextClip(quote, fontsize=50, color='white', font='Arial-Bold', 
                   method='caption', size=(video.w*0.8, None)).set_duration(10).set_pos('center')
    
    final = CompositeVideoClip([video, txt]).set_audio(audio.volumex(0.4))
    final.write_videofile("final.mp4", fps=24, codec="libx264")

# 4. Catbox & Telegram
def post_to_tg():
    with open("final.mp4", "rb") as f:
        link = requests.post("https://catbox.moe/user/api.php", data={"reqtype": "fileupload"}, files={"fileToUpload": f}).text
    
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", 
                  data={"chat_id": chat_id, "text": f"New Motivation: {link}"})

if __name__ == "__main__":
    get_assets()
    q = get_gemini_quote()
    create_video(q)
    post_to_tg()
