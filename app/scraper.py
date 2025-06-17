import requests
import json
import time
from bs4 import BeautifulSoup

HEADERS = {
    "Cookie": "_t=UqcBS0sPjIAmv6WT22Lf%2FOgTbqFlWxppu41WQPNT8%2FZ4%2BMs%2BvQB5lUQrvrOEO5aDJSggHrNFVR1lK57x%2F77mIcGdOpMgZ%2BLGy3LxdQjpCTIB%2F0MIVha%2BqDNZnAfakdVJWGDTZ1BBQkbJfgPJuHm5z6No3V2%2BDxNoFachIjGqVrtSDAY58QUOh6RNODX3b03g1GlmWUO%2F9TWTptJT%2FUS77I3poPvoP%2Fpv%2ByluYsuWHdFOxcjHKirXW%2BlLGoIqhM0YWnb46cA8U76DSYyytn6Tz1B1%2FBvX%2Bn5saooNT95llUL8tBKGjSEIZEmrcTs1IIj9--1nF6BHeb0TroDSS6--9cNampsdcKiHCX53ydYnxg%3D%3D",
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"

def fetch_topic_ids():
    url = f"{BASE_URL}/latest.json"
    res = requests.get(url, headers=HEADERS)
    data = res.json()
    topic_ids = [topic["id"] for topic in data["topic_list"]["topics"]]
    return topic_ids

def scrape_discourse(output_file="app/data/discourse.json"):
    posts = []
    topic_ids = fetch_topic_ids()

    for topic_id in topic_ids:
        url = f"{BASE_URL}/t/{topic_id}"
        print(f"Fetching: {url}")
        try:
            res = requests.get(url, headers=HEADERS)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                text = soup.get_text()
                posts.append({
                    "url": url,
                    "content": text
                })
            else:
                print(f"Skipped {url} (Status {res.status_code})")
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    with open(output_file, "w") as f:
        json.dump(posts, f, indent=2)

if __name__ == "__main__":
    scrape_discourse()
