import PySimpleGUI as sg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os.path

# window layout of two columns

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25,1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40,20),
            key="-FILE LIST-"
        ),
    ],
]

image_viewer_column = [
    [sg.Text("Choose an image from the list on the left:")],
    [sg.Text(size=(40,1), key="-FILE NAME-")],
    [sg.Text(size=(40,1), key="-DIMENSIONS-")],
    [sg.Text(size=(40,1), key="-FILE SIZE-")],
    [sg.Canvas(key='-CANVAS-')],
]

# full layout
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
        sg.Slider(range=(0, 0), default_value=0, size=(15, 15), 
                  orientation='vertical', enable_events=True, key="-SLIDER-"),
    ]
]

# create the window
window = sg.Window("Image Viewer", layout, finalize=True)

def get_filename(path):
    return "File name: " + os.path.basename(filename)

def get_dimensions(dimensions):
    h, w, d = dimensions
    return "Dimensions: {} x {}".format(w, h)

def get_filesize(path):
    size = "{:,}".format(os.stat(path).st_size)
    return "File size: {} bytes".format(size)

def get_image_details(path):
    img = mpimg.imread(path)
    imgplot = plt.imshow(img)
    window["-FILE NAME-"].update(get_filename(path))
    window["-DIMENSIONS-"].update(get_dimensions(img.shape))
    window["-FILE SIZE-"].update(get_filesize(path))

# draw image on canvas
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# create a fig for embedding
fig = plt.figure(figsize=(4, 3))
fig.set_facecolor(color='#64778d')
plt.axis('off')

# associate fig with canvas
fig_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

# event loop
while True:
    event, values = window.read()
    # end program if window closed
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # folder selected, make a list of files
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif"))
        ]
        window["-FILE LIST-"].update(fnames)
    # file chosen from list
    elif event == "-FILE LIST-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            get_image_details(filename)
            fig_agg.draw()

            # update slider index
            img_index = window["-FILE LIST-"].Widget.curselection()[0]
            slider = window["-SLIDER-"]
            slider.Update(img_index + 1, range=(1, len(file_list)))
        except:
            pass
    # slider selected, display corresponding image
    elif event == "-SLIDER-":
        try:
            slider_val = int(slider.TKScale.get())
            filename = os.path.join(
                values["-FOLDER-"], fnames[slider_val - 1]
            )
            get_image_details(filename)
            fig_agg.draw()
        except:
            pass

window.close()
