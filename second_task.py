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
    query = f'?q={top}&type=track'
    query_url = url + query
    headers = get_auth_header(token)
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    album = json_result['tracks']['items'][0]['album']
    if album['name'] == top:
        available_markets = album['available_markets']
    return available_markets

def get_top_10_songs_of_artist(songs):
    res = []
    for idx, song in enumerate(songs):
        res.append(song['name'])
        # print(f"{idx+1}.{song['name']}")
    return res



def get_release_date(token, artist_id, top):
    track_info = get_songs_by_artist(token, artist_id)
    for elem in track_info:
        if elem['album']['name']== top:
            return elem['album']['release_date']


def main():
    artist = input()
    print('Вкажіть цифру')
    print('1.ID артиста')
    print('2.Топ 10 пісень')
    print('3.Найпопулярніша пісня')
    print('4.В яких країнах вона доступна')
    print('5.Дата випуску найпопулярнішої пісні')
    print('6.Exit')

    while True:
        number = input('Натисніть номер інформації, яку Ви хочете отримати:')
        if number == '1':
            result = search_for_artist(get_token(), artist)['id']
            print(result)
        elif number == '2':
            res = search_for_artist(get_token(), artist)['id']
            songs = get_songs_by_artist(get_token(), res)
            print(get_top_10_songs_of_artist(songs))
        elif number == '3':
            songs = get_songs_by_artist(get_token(),search_for_artist(get_token(), artist)['id'])
            top = get_top_10_songs_of_artist(songs)
            print(top[0])
        elif number == '4':
            songs = get_songs_by_artist(get_token(),search_for_artist(get_token(), artist)['id'])
            top = get_top_10_songs_of_artist(songs)
            avaible = get_songs_avaib(top[0])
            print(avaible)
        elif number == '5':
            songs = get_songs_by_artist(get_token(),search_for_artist(get_token(), artist)['id'])
            top = get_top_10_songs_of_artist(songs)
            release = get_release_date(get_token(), search_for_artist(get_token(), artist)['id'], top[0])
            print(release)
        elif number == '6':
            return "End of program!"
main()