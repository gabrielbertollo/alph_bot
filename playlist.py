import requests
import time

def fetch_playlist(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data.get("playlist", [])
    except requests.RequestException as e:
        print(f"Error fetching playlist: {e}")
        return []

def save_playlist_to_txt(playlist, filename="playlist.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        if playlist:
            if playlist[0].get('position') == 0:
                file.write("### Now Playing ###\n")
                now_playing = playlist[0]
                requester = now_playing.get('viewer', {}).get('username', 'Unknown')   
                vip = now_playing.get('vip', False)
                file.write(f"{now_playing['string']} | by: {requester} {'(VIP)' if vip else ''}\n\n")
        
            file.write("### Next Up ###\n")
            for song in playlist[0:5]:
                if song.get('position') == 0:
                    continue
                position = song.get('position', 'Unknown')
                requester = song.get('viewer', {}).get('username', 'Unknown')
                vip = song.get('vip', False)
                file.write(f"{position}. {song['string']} | by: {requester} {'(VIP)' if vip else ''}\n")
            
            if len(playlist) > 5:
                file.write(f"\nAnd {len(playlist) - 5} more songs...")
                
        else:
            file.write("")
    
    print(f"Playlist updated: {filename}")

def main():
    API_URL = "https://rsplaylist.com/ajax/playlist.php?channel=alpheratzwow"
    INTERVAL = 10 
    
    while True:
        playlist = fetch_playlist(API_URL)
        save_playlist_to_txt(playlist)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
