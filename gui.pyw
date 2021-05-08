import PySimpleGUI as sg
import requests
import os


# Set color background
sg.theme('GrayGrayGray')
# list radiochannels
radiochannels = []
# Available urls
urlsplay = []
# Country List
countrylist = [
  "All Countries",
  "Britain",
  "Germany",
  "Greece",
  "Ireland",
  "Sweden",
  "The United States Of America",
]
# Genre List
genrelist = [
	"All Genres",
  "Blues",
  "Classic Rock",
  "Heavy Metal",
  "Rock",
]
# Language List
langlist = [
  "All Languages",
  "English",
  "Greek",
  "Irish",
]
# Find Window Picture
window_picture = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/logo_128.ico")
window_picture = window_picture.replace("\\", "/")

# Text Position
def TextLabel(text): return sg.Text(text+':', justification='left', size=(7,1), pad=(5,10))
def TextLabelc(text): return sg.Text(text+':', justification='center', size=(7,1), pad=(110,10))
def TextLabelr(text): return sg.Text(text+':', size=(7,1), pad=(12,10))

# Define the window's contents
layout = [
            [sg.Text("Filter stations by",text_color="#6e9cd7")],
            [sg.Text("Name")],     # Part 2 - The Layout
            [sg.Input("", pad=(10,10), key='nameinput')],
            [
                TextLabel('Genre'), TextLabelc('Country'),TextLabelr('Language'),
            ],
            [
                sg.Combo(genrelist, default_value=genrelist[0], size=(20, 1), pad=(10,10), key='genre'),
                sg.Combo(countrylist, default_value=countrylist[0], size=(20, 1), pad=(10,10), key='country'),
                sg.Combo(langlist, default_value=langlist[0], size=(20, 1), pad=(10,10), key='lang')
            ],
            [sg.Button('Filter Stations', button_color=('#d1cfcd'), size=(70,1))],
            [sg.Text("Station")],
            [sg.Listbox(values=radiochannels, select_mode='extended', key='fac', size=(50, 30))],
            [sg.Button('Play', button_color=('#d1cfcd'), size=(35,1)), sg.Text("Currently Playing: Nothing", pad=(50,10), key='cp')],
        ]

# Create the window with a picture
window = sg.Window('MediaVault', layout)
window.set_icon(window_picture)


# Display and interact with the buttons events
while True:
    urlofapi = "https://de1.api.radio-browser.info/json/stations/search?limit=500"
    event, values = window.read()
    playbt = values['fac']
    nameinput = values['nameinput']
    lang = values['lang']
    country = values['country']
    genre = values['genre']
    # filters
    if lang == "All Languages":
      lang = ""
    if country == "All Countries":
      country = ""
    if genre == "All Genres":
      genre = ""
    if nameinput != "":
      urlofapi = urlofapi + f"&name={nameinput}"
    if lang != "":
      urlofapi = urlofapi + f"&language={lang}"
    if country != "":
      urlofapi = urlofapi + f"&country={country}"
    if genre != "":
      urlofapi = urlofapi + f"&tag={genre}"
    if event == sg.WIN_CLOSED: # if user closes window
        break
    # Event when someone presses Play
    if event == "Play":
      indexurl = radiochannels.index(values['fac'][0])
      try:
       os.system("taskkill /im vlc.exe /f")
      except:
        os.system("killall -KILL vlc")
      os.system(f"start vlc.exe {urlsplay[indexurl]} -f --no-video-title-show")
      window['cp'].update(f"Currently Playing: {values['fac'][0]}")
    # Event when someone presses The Filter Stations
    if event == 'Filter Stations':
        radiochannels.clear()
        urlsplay.clear()
      # Call api
        print(urlofapi)
        response = requests.get(urlofapi)
        response = response.json()
        length = len(response)
        for i in range(length):
            radiochannels.insert(len(radiochannels), response[i]['name'])
            urlsplay.insert(len(urlsplay), response[i]['url'])
        # update list
        window.FindElement('fac').Update(values=radiochannels)

# # Finish up by removing from the screen
# window.close()
