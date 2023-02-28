import pycountry
import json
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from dotenv import load_dotenv
import base64
from requests import post,get
import json
import os


from dotenv import load_dotenv
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic '+ auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token



def get_auth_header(token):
    return {'Authorization': 'Bearer ' + token}



def search_for_artist(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist,track&limit=1'

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print('No artists exist')
        return None
    return json_result[0]



def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result



def get_songs_avaib(top):
    token = get_token()
    url = f'https://api.spotify.com/v1/search'
    query = f'?q={top}&type=track&limit=1'
    query_url = url + query
    headers = get_auth_header(token)
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    available_markets = json_result['tracks']['items'][0]['album']['available_markets']
    return available_markets


def get_top_10_songs_of_artist(songs):
    res = []
    for idx, song in enumerate(songs):
        res.append(song['name'])
        # print(f"{idx+1}.{song['name']}")
    return res



def form_map(list_):
    """
    this function put poins on map
    """
    map = folium.Map(location=[0, 0], zoom_start=2)
    for i in list_:
        country = pycountry.countries.get(alpha_2=i)
        geolocator = Nominatim(user_agent="Visual Studio Code")
        if country is None:
            continue
        name = country.name
        location = geolocator.geocode(name, timeout = 10, country_codes = i)
        if ',' in name:
            name = name.split(',')[0]
        try:
            location = geolocator.geocode(name, timeout = 10, country_codes = i)
        except:
            continue
        try:
            folium.Marker(location= [location.latitude, location.longitude],
                        popup = name,
                        icon=folium.Icon(color= 'darkpurple', icon = 'circle')
                        ).add_to(map)
        except AttributeError:
            continue
    map.add_child(folium.LayerControl())
    map.save('templates/Map.html')


def main(artist):
    token = get_token()
    result = search_for_artist(token, artist)
    artist_id = (result['id'])
    songs = get_songs_by_artist(token,artist_id)
    top = get_top_10_songs_of_artist(songs)
    map = form_map(get_songs_avaib(top[0]))
if __name__ == '__main__':
    main(input())