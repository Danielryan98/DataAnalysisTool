import tkinter as tk
import matplotlib.pyplot as plt
import graphviz as gv
from subprocess import check_call
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from PIL import ImageTk, Image
from src.Views import Views
from tkinter.filedialog import askopenfile
from future.moves.tkinter import filedialog


#### REMBER TO CHANGE THE DOC ID #####
doc_id = "100713205147-2ee05a98f1794324952eea5ca678c026"
doc_id1 = "140310170010-0000000067dc80801f1df696ae52862b"

vis_UUID = ""
doc_UUID = "140207031738-eb742a5444c9b73df2d1ec9bff15dae9"

#Start of window.
window = tk.Tk()

window.config(bg="white")

button_theme = '#1f77b4'

window.geometry("1100x650")

#Document ID Input Label.
document_uuid_label = tk.Label(window, text="document_uuid", font="Arial", height=2, width=12, bg="white")
document_uuid_label.place(x=30, y=20)

#Document ID Input Box.
document_uuid = tk.Entry(window, width=75, borderwidth=2) 
document_uuid.place(x=150, y=32)

#User ID Input Label.
visitor_uuid_label = tk.Label(window, text="visitor_uuid", font="Arial", height=2, width=12, bg="white")
visitor_uuid_label.place(x=45, y=51)

#User ID Input Box.
visitor_uuid = tk.Entry(window, width=75, borderwidth=2) 
visitor_uuid.place(x=150, y=63)


def paint_logo():
    global img
    path = "logonew.jpg"
    img= (Image.open(path))
    img = img.resize((425,100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(window, image=img, height=100, width=425, bd=0)
    panel.place(x=625, y=0)

paint_logo()

#Toolbar frame to hold toolbar.
toolbarFrame = tk.Frame(window)
toolbarFrame.config(bg="white")
toolbarFrame.place(x=535, y=600)

#Graph frame to hold the graph.
graphFrame = tk.Frame(window)
graphFrame.place(x=155, y=100)

#Upload json button.
upload_json_text = tk.StringVar()
upload_json_btn = tk.Button(window, textvariable=upload_json_text, font="Arial", bg=button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda: get_file_from_user())
upload_json_text.set("Upload json")
upload_json_btn.place(x=45, y=100)

#By country button.
by_country_text = tk.StringVar()
by_country_btn = tk.Button(window, textvariable=by_country_text, font="Arial", bg=button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda: by_country_plot(doc_id))
by_country_text.set("By Country")
by_country_btn.place(x=45, y=160)

#By continent button.
by_continent_text = tk.StringVar()
by_continent_btn = tk.Button(window, textvariable=by_continent_text, font="Arial", bg=button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda: by_continent_plot(doc_id))
by_continent_text.set("By Continent")
by_continent_btn.place(x=45, y=230)

#By browser button.
by_browser_text = tk.StringVar()
by_browser_btn = tk.Button(window, textvariable=by_browser_text, font="Arial", bg=button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : by_browser_plot())
by_browser_text.set("By Browser")
by_browser_btn.place(x=45, y=300)

#Also likes button.
also_likes_text = tk.StringVar()
also_likes_btn = tk.Button(window, textvariable=also_likes_text, font="Arial", bg=button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : determine_func())
also_likes_text.set("Also Likes")
also_likes_btn.place(x=45, y=370)

#Also likes graph button.
also_likes_graph_text = tk.StringVar()
also_likes_graph_btn = tk.Button(window, textvariable=also_likes_graph_text, font="Arial", bg=button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : determine_func())
also_likes_graph_text.set("Also Likes Graph")
also_likes_graph_btn.place(x=45, y=440)

#Walkthrough button.
tutorial_text = tk.StringVar()
tutorial_btn = tk.Button(window, textvariable=tutorial_text, font="Arial", bg=button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : determine_func())
tutorial_text.set("Tutorial")
tutorial_btn.place(x=45, y=510)

def get_file_from_user():
    file = tk.filedialog.askopenfile(parent=window, mode='r', title="Select a JSON file", filetype=[("JSON", ".json")]) #Prompt user to choose file to upload documenmts for
    if file: #If they choose a file rather than cancelling
        views = Views()
        views.__init__(file.name)


def by_country_plot(doc_id):
    instance = Views()
    browser_dict = instance.bycountry(doc_id)
    plot(browser_dict)

def by_continent_plot(doc_id):
    instance = Views()
    browser_dict = instance.bycontinent(doc_id)
    plot(browser_dict)

def by_browser_plot():
    instance = Views()
    browser_dict = instance.bybrowser()
    plot(browser_dict)

def plot(browser_dict):

    clear_widgets()

    print(browser_dict.items())

    x_items = []
    y_items = []

    for k, v in browser_dict.items():
        x_items.append(k)
        y_items.append(v)

    x = x_items
    y = y_items

    #Figure that will contain the plot.
    fig = Figure(figsize = (10, 5),
            dpi = 100)

    # Create the subplot. Set x & y and bar thickness. Plot the graph.
    plot1 = fig.add_subplot(111)
    plot1.bar(x, y, .5)
    plot1.plot()

    # creating the Tkinter canvas containing the Matplotlib figure,
    # and placing the canvas on the Tkinter window.
    canvas = FigureCanvasTkAgg(fig, master = graphFrame)  
    canvas.draw()
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar and placing it on the Tkinter window.
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    toolbar.config(bg="white")
    toolbar.update()
    toolbar.pack()

def clear_widgets():
    #Reset toolbar frame to allow for new graph toolbar.
    for widget in toolbarFrame.winfo_children():
        widget.destroy()

    #Reset chart frame to allow for new graph.
    for widget in graphFrame.winfo_children():
        widget.destroy()

#Function taken from https://stackoverflow.com/a/45846841 user 'rtaft'.
def format_number(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

def make_list(xs_sort):
    print(xs_sort)

def make_graph(xs_sort):

    #Clear the canvas.
    clear_widgets()

    #Views instance to grab data from.
    views = Views()

    #Format the key data so that it's in format 300k, 1m, 3m etc.
    data_size = format_number(views.dataList.__len__())

    #Slice the id's so that we only work with the last 4 characters. 
    main_user_id = vis_UUID[-4:]
    main_doc_id = doc_UUID[-4:]

    #Node Shapes
    user_shape = 'box'
    has_read_shape = 'circle'

    # the figure that will contain the plot
    fig = Figure(figsize = (10, 5),
            dpi = 100)
    

    #New graphviz digraph called also likes
    dot = gv.Digraph('also likes')

    #Graph key
    dot.node('Readers', 'Readers', shape='none')
    dot.node('Documents', 'Documents', shape='none')
    dot.edge('Readers', 'Documents', label='Size: ' + data_size)

    for x in xs_sort[:11]:
        if x[1] == main_doc_id:
            dot.node(x[1], x[1], shape=has_read_shape, color='green', style='filled')
        else:
            dot.node(x[1], x[1], shape=has_read_shape)
        for y in x[2]:
            if y == main_user_id:
                dot.node(y, y, shape=user_shape, color='green', style='filled')
                dot.edge(y, x[1])
            else:
                dot.node(y, y, shape=user_shape)
                dot.edge(y, x[1])
      
    print(dot.source)

    with open('graph.dot', "w") as dotfile:
        dotfile.truncate(0)
        dotfile.write(dot.source)
        dotfile.close()

   
    check_call(['dot','-Tpng','graph.dot','-o','graph.png'])

    img_arr = mpimg.imread('graph.png')

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.axis('off')
    plot1.imshow(img_arr)
    

    canvas = FigureCanvasTkAgg(fig, master = graphFrame)  
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

def determine_func():

    views = Views()

    if doc_UUID and vis_UUID:      
        make_graph(views.alsoLikes(doc_UUID, vis_UUID, views.sortFunc))
    else:
        make_graph(views.alsoLikes(doc_UUID, views.sortFunc))


window.mainloop()
#End of window
