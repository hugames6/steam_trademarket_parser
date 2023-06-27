from bs4 import BeautifulSoup
import requests
import re
import json


url = "https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Black%20Laminate%20%28Battle-Scarred%29"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition Yx GX)"
}

req = requests.get(url, headers=headers)
src = req.text

# with open(f"index.html", "w", encoding="utf-8") as file:
#     file.write(src)

# with open(f"index.html", encoding="utf-8") as file:
#     src = file.read()

soup = BeautifulSoup(src, 'lxml')

# nak = soup.find(lambda t: t.name == 'script' and 'var g_rgAsset' in t.text)

# kley = re.search(r'var g_rgAsset = (\[.*\]);', nak.text, flags=re.S)[1]

# ki = kley.replace("'", '"')
# ki = re.sub(r"^(\s*)(.*?):", r'\1"\2":', ki, flags=re.M)

# data = json.loads(ki)

# print(data)

nak = soup.find_all('script')

kley = str(nak[27])

# print(kley)

var_re = re.compile(r'var g_rgAssets=\[(.+)\]')
date_mach = var_re.findall(kley)

print(date_mach)

# if "Sticker" in kley:
#     print('TRUE')

# print(nak)
# nakleyki = soup.find_all('script')
# nakleyki_find = re.search(r'g_rgAssets\s*=\s*(.*?}])\s*\n', str(soup.find_all('script')), flags=re.DOTALL)
