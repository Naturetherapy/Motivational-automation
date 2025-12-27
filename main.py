import os, random, requests, re

def get_gemini_quote():
    api_key = os.getenv('GEMINI_API_KEY')
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    prompt = {"contents": [{"parts":[{"text": "Write a deep 1-sentence motivational quote."}]}]}
    res = requests.post(url, json=prompt).json()
    return res['candidates'][0]['content']['parts'][0]['text']

def get_live_assets():
    # 1. Pexels Live Video Search
    v_headers = {"Authorization": os.getenv('PEXELS_API_KEY')}
    v_res = requests.get("https://api.pexels.com/videos/search?query=nature&per_page=10", headers=v_headers).json()
    video_url = random.choice(v_res['videos'])['video_files'][0]['link']

    # 2. Chosic Live Music Search (No Saved Links)
    # Hum website par 'Slow Piano' search karke MP3 link nikalenge
    search_url = "https://www.chosic.com/free-music/all/?keyword=slow+piano&sort=random"
    html = requests.get(search_url).text
    # Regex se MP3 link dhoondhna
    mp3_links = re.findall(r'https://www.chosic.com/wp-content/uploads/[^"\'>]+\.mp3', html)
    music_url = random.choice(mp3_links) if mp3_links else "https://www.chosic.com/wp-content/uploads/2021/07/Rain.mp3"

    return video_url, music_url

def post_to_tg(v_url, m_url, quote):
    token = os.getenv('TG_TOKEN')
    chat_id = os.getenv('TG_CHAT_ID')
    caption = f"✨ {quote}\n\n🎵 Background Piano Included"
    
    # Video bhejte hain
    requests.post(f"https://api.telegram.org/bot{token}/sendVideo", 
                  data={"chat_id": chat_id, "video": v_url, "caption": caption})
    # Music bhejte hain (As per instruction, music hamesha rahega)
    requests.post(f"https://api.telegram.org/bot{token}/sendAudio", 
                  data={"chat_id": chat_id, "audio": m_url})

if __name__ == "__main__":
    q = get_gemini_quote()
    v, m = get_live_assets()
    post_to_tg(v, m, q)
