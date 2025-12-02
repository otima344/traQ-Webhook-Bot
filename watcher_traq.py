import requests
from bs4 import BeautifulSoup
import hashlib
import os

TARGET_URL = os.environ.get("TARGET_URL")  # 監視したいページ
WEBHOOK_ID = os.environ.get("TRAQ_WEBHOOK_ID")  # Secrets から読み込む
WEBHOOK_URL = f"https://q.trap.jp/api/v3/webhooks/{WEBHOOK_ID}"

HASH_FILE = "last_hash.txt"

def get_page_hash():
    r = requests.get(TARGET_URL)
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text()
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def load_last_hash():
    if not os.path.exists(HASH_FILE):
        return None
    with open(HASH_FILE, "r") as f:
        return f.read().strip()

def save_hash(h):
    with open(HASH_FILE, "w") as f:
        f.write(h)

def notify(message):
    headers = {"Content-Type": "text/plain; charset=utf-8"}
    res = requests.post(WEBHOOK_URL, data=message.encode("utf-8"), headers=headers)
    print("traQ response:", res.status_code, res.text)

def main():
    new_hash = get_page_hash()
    old_hash = load_last_hash()

    if new_hash != old_hash:
        print("更新を検知！")
        msg = f"🔔 ページが更新されました！\n{TARGET_URL}"
        notify(msg)
        save_hash(new_hash)
    else:
        print("変更なし")

if __name__ == "__main__":
    main()
