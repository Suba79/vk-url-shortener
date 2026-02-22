import requests
from urllib.parse import urlparse


class VKAPIError(Exception):
    pass


def _get_link_key(url):
    parsed = urlparse(url)
    return parsed.path.strip('/').split('/')[-1]


def is_shorten_link(token, url):
    parsed = urlparse(url)
    
    if parsed.netloc != 'vk.cc' or not parsed.path.strip('/'):
        return False
    
    params = {
        'access_token': token,
        'v': '5.199',
        'key': _get_link_key(url),
        'interval': 'forever'
    }
    
    response = requests.get('https://api.vk.ru/method/utils.getLinkStats', params=params)
    api_response = response.json()
    
    return 'error' not in api_response


def shorten_link(token, url):
    params = {
        'access_token': token,
        'v': '5.199',
        'url': url,
        'private': 0
    }
    
    response = requests.get('https://api.vk.ru/method/utils.getShortLink', params=params)
    api_response = response.json()
    
    if 'error' in api_response:
        raise VKAPIError("Ошибка API")
    
    return api_response['response']['short_url']


def count_clicks(token, short_url):
    params = {
        'access_token': token,
        'v': '5.199',
        'key': _get_link_key(short_url),
        'interval': 'forever'
    }
    
    response = requests.get('https://api.vk.ru/method/utils.getLinkStats', params=params)
    api_response = response.json()
    
    if 'error' in api_response:
        raise VKAPIError("Ошибка API")
    
    stats = api_response['response'].get('stats', [])
    return stats[0].get('views', 0) if stats else 0