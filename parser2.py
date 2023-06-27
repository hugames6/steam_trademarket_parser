from requests_html import HTMLSession

session = HTMLSession()

r = session.get('https://steamcommunity.com/market/listings/730/AWP%20%7C%20Redline%20%28Field-Tested%29')

r.html.render()

print(r.text)