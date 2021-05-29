import PySimpleGUI as sg
import requests
import os
from PIL import Image
import glob
import imghdr

# Set color background
sg.theme('GrayGrayGray')
# list radiochannels
radiochannels = []
# Available urls
urlsplay = []
# Available url images
imageofradio = []
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
layoutradio = [
    [
        sg.Image(filename="", size=(10, 10), pad=(25,10), key='ri' )
    ],
    [
        sg.Text("\nCurrently Playing: Nothing", pad = (0,20), key='cp')
    ],
    ]
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
            [sg.Button('Discover', button_color=('#d1cfcd'), size=(70,1))],
            [sg.Text("Station")],
            [sg.Listbox(values=radiochannels, select_mode='extended', key='fac', size=(50, 30)), sg.Column(layoutradio)],
            [sg.Button('Play', button_color=('#d1cfcd'), size=(35,1)), sg.Text("                      ") ,sg.Button('Clear Cache', button_color=('#d1cfcd'), size=(15,1)), sg.Text("", key='fb')],
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
    # Event when someone presses clear Cache
    window["fb"].update(value="")
    if event == "Clear Cache":
        files = glob.glob('./radio_images/*')
        for f in files:
            os.remove(f)
        window["fb"].update(value="✓")
    # Event when someone presses Play
    if event == "Play":
      if not radiochannels:
        print("Haha no crash")
      else:
        indexurl = radiochannels.index(values['fac'][0])
        # Download Radio Icon
        if os.path.exists(f"./radio_images/{str(values['fac'][0])}.png") == False and imageofradio[indexurl] == "":
            window['ri'].update(filename="./images/NoImage.png")

        if os.path.exists(f"./radio_images/{str(values['fac'][0])}.png") == False and imageofradio[indexurl] != "":
          response = requests.get(imageofradio[indexurl])
          file = open(f"./radio_images/{str(values['fac'][0])}.png", "wb")
          file.write(response.content)
          file.close()
          if imghdr.what(f"./radio_images/{str(values['fac'][0])}.png") != None:
            image = Image.open(f"./radio_images/{str(values['fac'][0])}.png")
            new_image = image.resize((100, 100))
            new_image.save(f"./radio_images/{str(values['fac'][0])}.png")
            window['ri'].update(filename=f"./radio_images/{values['fac'][0]}.png")
            if imghdr.what(f"./radio_images/{str(values['fac'][0])}.png") != "png":
                window['ri'].update(filename="./images/NoImage.png")

            if os.path.exists(f"./radio_images/{str(values['fac'][0])}.png") == True:
                window['ri'].update(filename=f"./radio_images/{values['fac'][0]}.png")
          else:
            window['ri'].update(filename="./images/NoImage.png")
        window['cp'].update(value=f"Currently Playing: {str(values['fac'][0])}")
        # Kill old vlc
        try:
          os.system("taskkill /im vlc.exe /f")
        except ImportError:
          print("A module is missing or its not installed corrently")
        else:
          os.system("killall -KILL vlc")
        # Start VLC
        try:
          os.system(f"start vlc.exe {urlsplay[indexurl]} -f --no-video-title-show")
        except ImportError:
            print("A module is missing or its not installed corrently")
        else:
          os.system(f"vlc {urlsplay[indexurl]} -f --no-video-title-show")
    # Event when someone presses The Filter Stations
    if event == 'Discover':
        radiochannels.clear()
        urlsplay.clear()
        imageofradio.clear()
      # Call api
        # print(urlofapi)
        response = requests.get(urlofapi)
        response = response.json()
        # print(response)
        length = len(response)
        for i in range(length):
            radiochannels.insert(len(radiochannels), response[i]['name'])
            urlsplay.insert(len(urlsplay), response[i]['url'])
            imageofradio.insert(len(imageofradio), response[i]['favicon'])
        # update list
        window.FindElement('fac').Update(values=radiochannels)
# # Finish up by removing from the screen
# window.close()
