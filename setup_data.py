import os
import requests
import zipfile
import io

def download_arc_data():
    print("--> Downloading ARC-AGI Data from official source...")
    url = "https://github.com/fchollet/ARC-AGI/archive/refs/heads/master.zip"
    
    r = requests.get(url)
    if r.status_code == 200:
        print("    Download complete. Unzipping...")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(".") # Extract to current folder
        
        # Rename the weird folder name GitHub gives it
        if os.path.exists("ARC-AGI-master"):
            os.rename("ARC-AGI-master", "data")
            print("    Data saved to ./data/ folder.")
            print("    Success! You now have the real training puzzles.")
    else:
        print(f"    Error downloading data: {r.status_code}")

if __name__ == "__main__":
    download_arc_data()
