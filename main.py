import os, random, requests
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip

# 1. Gemini se Quote lena
def get_gemini_quote():
    api_key = os.getenv('GEMINI_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    prompt = {"contents": [{"parts":[{"text": "Write a deep, 1-sentence motivational quote."}]}]}
    res = requests.post(url, json=prompt).json()
    return res['candidates'][0]['content']['parts'][0]['text']

# 2. Pixabay se Automatic Piano Music aur Pexels se Video
def get_assets():
    # Video from Pexels
    v_headers = {"Authorization": os.getenv('PEXELS_API_KEY')}
    v_url = "https://api.pexels.com/videos/search?query=calm+nature&orientation=portrait&per_page=10"
    v_res = requests.get(v_url, headers=v_headers).json()
    v_link = random.choice(v_res['videos'])['video_files'][0]['link']
    with open("bg.mp4", 'wb') as f: f.write(requests.get(v_link).content)

    # Music from Pixabay Website (API ke through live search)
    # Aapko Pixabay API key bhi leni hogi (Free hai)
    pixabay_key = os.getenv('PIXABAY_API_KEY')
    m_url = f"https://pixabay.com/api/videos/etc/ (Actually use music endpoint)"
    # Alternative: Direct scraping/searching from a free library
    music_search_url = f"https://pixabay.com/api/audio/?key={pixabay_key}&q=slow+piano+motivation"
    m_res = requests.get(music_search_url).json()
    m_link = random.choice(m_res['hits'])['audio'] # Live search result
    with open("music.mp3", 'wb') as f: f.write(requests.get(m_link).content)

# 3. Merging (Aapki image style mein)
def create_video(quote):
    video = VideoFileClip("bg.mp4").subclip(0, 10)
    audio = AudioFileClip("music.mp3").subclip(0, 10)
    
    # Image jaisa text: White, centered, bold
    txt = TextClip(quote, fontsize=50, color='white', font='Arial-Bold', 
                   method='caption', size=(video.w*0.8, None)).set_duration(10).set_pos('center')
    
    final = CompositeVideoClip([video, txt]).set_audio(audio.volumex(0.5))
    final.write_videofile("final.mp4", fps=24, codec="libx264")

# 4. Telegram par link bhej bhej na
def post_to_tg():
    with open("final.mp4", "rb") as f:
        link = requests.post("https://catbox.moe/user/api.php", data={"reqtype": "fileupload"}, files={"fileToUpload": f}).text
    
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": f"New Motivation: {link}"})

if __name__ == "__main__":
    get_assets()
    q = get_gemini_quote()
    create_video(q)
    post_to_tg()
