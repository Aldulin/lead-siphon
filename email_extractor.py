import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

def extract_emails(df):
    email_pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    emails = []

    for url in df.get("Website", []):
        email = ""
        try:
            if not url.startswith("http"):
                url = "http://" + url
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")
            found_emails = email_pattern.findall(soup.get_text())
            if found_emails:
                email = found_emails[0]  # Grab the first valid email
        except:
            pass
        emails.append(email)

    df["Email"] = emails
    return df
