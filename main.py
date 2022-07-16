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
            'path': config['settings']['path'],
            'export': config['settings']['export']
        }


try:
    with open('config.ini', 'r') as configfile:
        config.read('config.ini')
except IOError:
    with open('config.ini', 'w') as configfile:
        config['settings'] = {
            'apikey': '',
            'path': p,
            'export': 'Title, URL'
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


def saveset():
    print('ok')


def exportsh():
    print('ex')


# interface.dirpath.get()
interface.savebut.config(command=saveset())
interface.exportbut.config(command=exportsh())

# populate fields

interface.root.mainloop()
