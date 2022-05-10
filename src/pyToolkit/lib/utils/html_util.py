import requests


def get_html(url):
    html = requests.get(url)
    return html.content.decode('utf-8')
