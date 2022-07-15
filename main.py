import configparser
import interface
from pathlib import Path
import googleapiclient.discovery
import googleapiclient.errors

# setup config
config = configparser.ConfigParser()
p = Path(__file__).parent.absolute()
playlist = ''


class configC:
    def __init__(self):
        self.settings = {
            'apikey': config['settings']['apikey'],
            'title': config['settings']['title'],
            'yturl': config['settings']['yturl'],
            'ploader': config['settings']['uploader'],
            'date': config['settings']['date'],
            'description': config['settings']['description']
        }


try:
    with open('config.ini', 'r') as configfile:
        config.read('config.ini')
except IOError:
    with open('config.ini', 'w') as configfile:
        config['settings'] = {
            'apikey': '',
            'title': 'True',
            'yturl': 'True',
            'uploader': 'False',
            'date': 'False',
            'description': 'False'
        }
        config.write(configfile)

con = configC()
playlist = ''


# get info
def main():
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=con.settings['apikey'])

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist)
    response = request.execute()
    print(response)
