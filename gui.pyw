import os
import glob
import imghdr
import sys
try:
    import PySimpleGUI as sg
    import requests
    import pychromecast
    from PIL import Image
except ImportError:
    os.system("pip install PySimpleGUI Pillow Requests PyChromecast")
    # Reopen file after modules install
    os.popen(sys.argv[0])

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
    "Argentina",
    "Australia",
    "Austria",
    "Belgium",
    "Brazil",
    "Canada",
    "Chile",
    "China",
    "Colombia",
    "Croatia",
    "Czechia",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "India",
    "Ireland",
    "Italy",
    "Mexico",
    "Peru",
    "Poland",
    "Portugal",
    "Romania",
    "Russia",
    "Spain",
    "Switzerland",
    "The Netherlands",
    "The Russian Federation",
    "The United Kingdom",
    "The United States Of America",
    "Turkey",
    "Ukraine",
]
# Genre List
genrelist = [
    "All Genres",
    "Alternative",
    "Blues",
    "Classical",
    "Country",
    "Dance",
    "Disco",
    "Drum and bass",
    "Electronic",
    "Folk",
    "Jazz",
    "Latin",
    "Love",
    "Metal",
    "New Age",
    "News",
    "Oldies",
    "Pop",
    "Rap",
    "Rock",
    "Reggae",
    "Religion",
    "RnB",
    "Punk",
    "Soul",
    "Sports",
    "Talk",
    "Techno",
    "Trance",
]
# Language List
langlist = [
    "All Languages",
    "Arabic",
    "Bulgarian",
    "Chinese",
    "Croatian",
    "Czech",
    "Danish",
    "Dutch",
    "English",
    "Finnish",
    "French",
    "German",
    "Greek",
    "Hindi",
    "Hungarian",
    "Irish",
    "Italian",
    "Japanese",
    "Korean",
    "Norwegian",
    "Polish",
    "Portuguese",
    "Romanian",
    "Russian",
    "Serbian",
    "Slovak",
    "Slovenian",
    "Spanish",
    "Swedish",
    "Thai",
    "Turkish",
    "Ukrainian",
]


# Find Window Picture
window_picture = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), "images/logo_128.ico")
window_picture = window_picture.replace("\\", "/")

# Cast Window


def Cast_window(indexurl, imageurl, nameofradio, playurls):
    layout = [
        [sg.Text("Enter your Chromecast's Name", text_color="#6590c7")],
        [sg.Text(" ")],
        [sg.Text(f"Choice for cast: {nameofradio}")],
        [sg.Input("", pad=(5, 5), key='cast')],
        [sg.Button('Cast', button_color=('#d1cfcd'), size=(15, 1))],
        [sg.Text("\nCurrently Casting on: Nothing", key="response_")],
    ]

    window = sg.Window('Cast', layout, icon=window_picture)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Cast":

            # List chromecasts on the network, but don't connect
            services, browser = pychromecast.discovery.discover_chromecasts()

            # Shut down discovery
            pychromecast.discovery.stop_discovery(browser)

            # Discover and connect to chromecasts with given name
            chromecasts, browser = pychromecast.get_listed_chromecasts(
                friendly_names=[f"{values['cast']}"])
            [cc.device.friendly_name for cc in chromecasts]

            #  Check if the chromecast exists
            if not chromecasts:
                window["response_"].update(
                    f"Unable to cast to: {values['cast']}! ", text_color="#a62d2d")
            else:
                cast = chromecasts[0]
                # Start worker thread and wait for cast device to be ready
                cast.wait()
                mc = cast.media_controller
                # Sent media to Chromecast
                mc.play_media(f'{playurls}', 'audio/mp3',
                              title=f'{nameofradio}', thumb=f"{imageurl}")
                mc.title
                mc.block_until_active()
                mc.pause()
                mc.play()
                window["response_"].update(
                    f"Currently Casting on: {values['cast']}! ", text_color="#000000")
                window['cast'].update("")

                # Shut down discovery
                pychromecast.discovery.stop_discovery(browser)

# Text Position


def TextLabel(text): return sg.Text(
    text+':', justification='left', size=(7, 1), pad=(5, 10))
def TextLabelc(text): return sg.Text(
    text+':', justification='center', size=(7, 1), pad=(110, 10))


def TextLabelr(text): return sg.Text(text+':', size=(7, 1), pad=(12, 10))

# Play Button


def PlayButton(values, radiovalue, imageofradio, indexurl, radiovalueurl, urlsplay):
    # Check if There is a image url
    if os.path.exists(f"./radio_images/{radiovalue}.png") == False and imageofradio[indexurl] == "":
        window['ri'].update(filename="./images/NoImage.png")
    else:
        # Download Radio Icon
        if os.path.exists(f"./radio_images/{radiovalue}.png") == False and imageofradio[indexurl] != "":
            response = requests.get(imageofradio[indexurl])
            file = open(f"./radio_images/{radiovalue}.png", "wb")
            file.write(response.content)
            file.close()
        # Check if file is a image and if it is use it.
        if imghdr.what(f"./radio_images/{radiovalue}.png") is not None:
            image = Image.open(f"./radio_images/{radiovalue}.png")
            new_image = image.resize((100, 100))
            new_image.save(f"./radio_images/{radiovalue}.png")
            window['ri'].update(filename=f"./radio_images/{radiovalue}.png")

        # If Image is not a png then replace with NoRadio Image
        if imghdr.what(f"./radio_images/{radiovalue}.png") != "png":
            window['ri'].update(filename="./images/NoImage.png")

        # Check if the png file actually exists.
        if os.path.exists(f"./radio_images/{radiovalue}.png") is True:
            window['ri'].update(filename=f"./radio_images/{radiovalue}.png")

    # Update Title for playing.
    window['cp'].update(value=f"Currently Playing: {radiovalueurl}")

    # Kill old vlc
    try:
        os.system("taskkill /im vlc.exe /f")
    except ImportError:
        pass
    else:
        os.system("killall -KILL vlc")
    # Start VLC
    try:
        os.system(
            f"start vlc.exe {urlsplay[indexurl]} -f --no-video-title-show")
    except ImportError:
        pass
    else:
        os.system(f"vlc {urlsplay[indexurl]} -f --no-video-title-show")
        os.system(
            f"/Applications/VLC.app/Contents/MacOS/VLC {urlsplay[indexurl]} -f --no-video-title-show")


# Define the window's contents
layoutradio = [
    [
        sg.Image(filename="", size=(10, 10), pad=(25, 10), key='ri')
    ],
    [
        sg.Text("\nCurrently Playing: Nothing", pad=(0, 20), key='cp')
    ],
]
layout = [
    [
        sg.Text("Filter stations by", text_color="#6e9cd7"),
        sg.Text("                                                                                                    "),
        sg.Button('Cast', button_color=('#d1cfcd'), size=(5, 1))
    ],
    [sg.Text("Name")],     # Part 2 - The Layout
    [sg.Input("", pad=(10, 10), key='nameinput')],
    [
        TextLabel('Genre'), TextLabelc(
            'Country'), TextLabelr('Language'),
    ],
    [
        sg.Combo(genrelist, default_value=genrelist[0], size=(
            20, 1), pad=(10, 10), key='genre'),
        sg.Combo(countrylist, default_value=countrylist[0], size=(
            20, 1), pad=(10, 10), key='country'),
        sg.Combo(langlist, default_value=langlist[0], size=(
            20, 1), pad=(10, 10), key='lang')
    ],
    [sg.Button('Discover', button_color=('#d1cfcd'), size=(70, 1))],
    [sg.Text("Station")],
    [sg.Listbox(values=radiochannels, select_mode='extended',
                key='fac', size=(50, 30)), sg.Column(layoutradio)],
    [sg.Button('Play', button_color=('#d1cfcd'), size=(35, 1)), sg.Text("                      "),
     sg.Button('Clear Cache', button_color=('#d1cfcd'), size=(15, 1)), sg.Text("", key='fb')],
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
    lang: str = values['lang'].lower()
    country = values['country']
    genre = values['genre']

    # filters
    if lang == "all languages":
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
        urlofapi = urlofapi + f"&tags={genre}"
    if event == sg.WIN_CLOSED:  # if user closes window
        break

    # Reset Checkmark
    window["fb"].update(value="")

    # When someone clicks the Cast button
    if event == "Cast":
        # Check if a radio channel has been chosen.
        if not radiochannels:
            pass
        else:
            indexurl = radiochannels.index(values['fac'][0])
            nameofradio = values['fac'][0]
            imageurl = imageofradio[indexurl]
            playurls = urlsplay[indexurl]
            Cast_window(indexurl, imageurl, nameofradio, playurls)

    # When someone clicks the Clear Cache Button
    if event == "Clear Cache":
        files = glob.glob('./radio_images/*')
        for f in files:
            os.remove(f)
        window["fb"].update(value="✓")

    # Event when someone presses Play
    if event == "Play":
        if not radiochannels:
            pass
        else:
            radiovalueurl = str(values['fac'][0])
            radiovalue = str(values['fac'][0]).replace(
                r'[\W_]+', "").replace('\t', "").replace(" ", "")
            indexurl = radiochannels.index(radiovalueurl)
            PlayButton(values, radiovalue, imageofradio,
                       indexurl, radiovalueurl, urlsplay)

    # Event when someone presses Discorver Button
    if event == 'Discover':
        radiochannels.clear()
        urlsplay.clear()
        imageofradio.clear()

        # Call radio channels api
        response = requests.get(urlofapi)
        response = response.json()
        length = len(response)
        if len(response) == 0:
            radiochannels.insert(len(radiochannels),
                                 "* No Radio Stations Found")
        else:
            for i in range(length):
                radiochannels.insert(len(radiochannels), response[i]['name'])
                urlsplay.insert(len(urlsplay), response[i]['url'])
                imageofradio.insert(len(imageofradio), response[i]['favicon'])

        # Update list
        window.find_element('fac').Update(values=radiochannels)
