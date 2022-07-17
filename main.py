import configparser
import interface
from datetime import date
import xlwt
import googleapiclient.discovery
import googleapiclient.errors


# get info
def main():
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=interface.apifield.get())
    try:
        # get name of playlist
        request = youtube.playlists().list(
            part="snippet",
            id=interface.plfield.get()
        ).execute()
        pltitle = request['items'][0]['snippet']['title']

        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=interface.plfield.get(),
            maxResults="50"
        ).execute()

        # check if there are more pages
        token = request.get('nextPageToken')
        while 'nextPageToken' in request:
            nextPage = youtube.playlistItems().list(
                part="snippet",
                playlistId=interface.plfield.get(),
                maxResults="50",
                pageToken=token
            ).execute()
            request['items'] = request['items'] + nextPage['items']

            if 'nextPageToken' not in nextPage:
                request.pop('nextPageToken', None)
            else:
                token = nextPage['nextPageToken']
        return pltitle, request['items']
    except Exception as e:
        interface.messagebox.showerror('Error', str(e))


def saveset():
    config['settings']['apikey'] = interface.apifield.get()
    config['settings']['playlist'] = interface.plfield.get()
    config['settings']['path'] = interface.dirpath.get()
    config['settings']['export'] = ''
    for indx in range(interface.lbox.size()):
        config['settings']['export'] += interface.lbox.get(indx) + ' '
    config['settings']['export'] = config['settings']['export'][:-1]
    try:
        with open('config.ini', 'w') as y:
            config.write(y)
        interface.messagebox.showinfo('Save Settings', 'Settings have been saved.')
    except IOError:
        interface.messagebox.showerror('Save Settings', 'Settings could not be saved.')


def exportsh():
    config['settings']['export'] = ''
    for indx in range(interface.lbox.size()):
        config['settings']['export'] += interface.lbox.get(indx) + ' '
    config['settings']['export'] = config['settings']['export'][:-1]
    tdate = today.strftime("%b-%d-%Y")
    data = main()
    sheet.write(0, 0, 'Playlist: ' + data[0] + ' ' + tdate)
    y = 0
    try:
        for a in config['settings']['export'].split():
            x = 1
            sheet.write(x, y, a, style=xlwt.easyxf('font: bold 1'))
            for b in data[1]:
                x += 1
                match a:
                    case 'Title':
                        sheet.write(x, y, b['snippet']['title'])
                    case 'URL':
                        sheet.write(x, y, 'https://www.youtube.com/watch?v='+b['snippet']['resourceId']['videoId'])
                    case 'Uploader':
                        sheet.write(x, y, b['snippet']['videoOwnerChannelTitle'])
                    case 'Date':
                        sheet.write(x, y, b['snippet']['publishedAt'].split('T')[0])
                    case 'Description':
                        sheet.write(x, y, b['snippet']['description'])
            y += 1
        wb.save(interface.os.path.join(interface.dirpath.get(), data[0] + '_' + tdate + '.xls'))
        interface.messagebox.showinfo('Export Spreadsheet', 'Spreadsheet has been created.')
    except Exception as ex:
        interface.messagebox.showerror('Error', str(ex))


# setup
config = configparser.ConfigParser()
today = date.today()
wb = xlwt.Workbook()
sheet = wb.add_sheet('Playlist', cell_overwrite_ok=True)

# pyinstaller dirpath
if getattr(interface.sys, 'frozen', False):
    interface.dirpath.set(interface.os.path.dirname(interface.sys.executable))
else:
    interface.dirpath.set(interface.os.path.dirname(interface.os.path.abspath(__file__)))

try:
    with open('config.ini', 'r') as configfile:
        config.read('config.ini')
except IOError:
    with open('config.ini', 'w') as configfile:
        config['settings'] = {
            'apikey': '',
            'playlist': '',
            'path': interface.dirpath.get(),
            'export': 'Title URL'
        }
        config.write(configfile)


# load buttons
interface.savebut.config(command=saveset)
interface.exportbut.config(command=exportsh)

# populate fields
interface.apifield.set(config['settings']['apikey'])
interface.plfield.set(config['settings']['playlist'])
interface.dirpath.set(config['settings']['path'])

for item in config['settings']['export'].split():
    interface.lbox.insert(interface.END, item)
    match item:
        case 'Title':
            interface.c1but.select()
        case 'URL':
            interface.c2but.select()
        case 'Uploader':
            interface.c3but.select()
        case 'Date':
            interface.c4but.select()
        case 'Description':
            interface.c5but.select()


interface.root.mainloop()
