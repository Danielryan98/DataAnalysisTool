import tkinter as tk
import matplotlib.pyplot as plt
import graphviz as gv
from subprocess import check_call
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

from Views import Views

#### REMBER TO CHANGE THE DOC ID #####
doc_id = "100713205147-2ee05a98f1794324952eea5ca678c026"
doc_id1 = "140310170010-0000000067dc80801f1df696ae52862b" #view.sortFunc

visUUID = ""
docUUID = "140310171202-000000002e5a8ff1f577548fec708d50"

#Start of window
window = tk.Tk()

window.geometry("1200x800")

#Document ID Input Label
input_doc_id_label = tk.Label(window, text="Input doc_id", font="Arial", height=2, width=10)
input_doc_id_label.place(x=0, y=0)


#Document ID Input Box
input_doc_id = tk.Entry(window) 
input_doc_id.place(x=0, y=50)


#By country button
by_country_text = tk.StringVar()
by_country_btn = tk.Button(window, textvariable=by_country_text, font="Arial", bg="Blue", fg="White", height=2, width=15, command=lambda: by_country_plot(doc_id))
by_country_text.set("By Country")
by_country_btn.place(x=0, y=100)


#By continent button
by_continent_text = tk.StringVar()
by_continent_btn = tk.Button(window, textvariable=by_continent_text, font="Arial", bg="Blue", fg="White", height=2, width=15, command=lambda: by_continent_plot(doc_id))
by_continent_text.set("By Continent")
by_continent_btn.place(x=0, y=150)


#By browser button
by_browser_text = tk.StringVar()
by_browser_btn = tk.Button(window, textvariable=by_browser_text, font="Arial", bg="Blue", fg="White", height=2, width=15, command=lambda : by_browser_plot())
by_browser_text.set("By Browser")
by_browser_btn.place(x=0, y=200)

#Also likes button
also_likes_text = tk.StringVar()
also_likes_btn = tk.Button(window, textvariable=also_likes_text, font="Arial", bg="Blue", fg="White", height=2, width=15, command=lambda : determine_func())
also_likes_text.set("Also Likes")
also_likes_btn.place(x=0, y=250)

toolbarFrame = tk.Frame(window)
toolbarFrame.place(x=150, y=0)

#Also likes graph button
also_likes_graph_text = tk.StringVar()
also_likes_graph_btn = tk.Button(window, textvariable=also_likes_graph_text, font="Arial", bg="Blue", fg="White", height=2, width=15, command=lambda : determine_func())
also_likes_graph_text.set("Also Likes Graph")
also_likes_graph_btn.place(x=0, y=300)

#Walkthrough button
tutorial_text = tk.StringVar()
tutorial_btn = tk.Button(window, textvariable=tutorial_text, font="Arial", bg="Blue", fg="White", height=2, width=15, command=lambda : determine_func())
tutorial_text.set("Tutorial")
tutorial_btn.place(x=0, y=350)

toolbarFrame = tk.Frame(window)
toolbarFrame.place(x=150, y=0)

graphFrame = tk.Frame(window)
graphFrame.place(x=150, y=50)



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

   # the figure that will contain the plot
    fig = Figure(figsize = (10, 5),
            dpi = 100)

    print(browser_dict.items())

    x_items = []
    y_items = []

    for k, v in browser_dict.items():
        x_items.append(k)
        y_items.append(v)

    x = x_items
    y = y_items

    # adding the subplot
    plot1 = fig.add_subplot(111)

    #Set x & y and bar thickness
    plot1.bar(x, y, .5)

    # plotting the graph
    plot1.plot()

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master = graphFrame)  
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()


    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    toolbar.pack()

def clear_widgets():
    #Reset toolbar frame to allow for new graph toolbar
    for widget in toolbarFrame.winfo_children():
        widget.destroy()

    #Reset chart frame to allow for new graph
    for widget in graphFrame.winfo_children():
        widget.destroy()

#Function taken from https://stackoverflow.com/a/45846841 user 'rtaft'
def format_number(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def make_graph(xs_sort):

    instance = Views()
    data_size = format_number(instance.dataList.__len__())

    clear_widgets()

    main_user_id = visUUID[-4:]
    main_doc_id = docUUID[-4:]

    # the figure that will contain the plot
    fig = Figure(figsize = (10, 5),
            dpi = 100)

    user_shape = 'box'
    has_read_shape = 'circle'

    dot = gv.Digraph('also likes')

    dot.node('Readers', 'Readers', shape='none')
    dot.node('Documents', 'Documents', shape='none')
    dot.edge('Readers', 'Documents', label='Size: ' + data_size)

    for x in xs_sort:
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

    

    instance = Views()

    if docUUID and visUUID:      
        xs_sort = instance.alsoLikes(docUUID, visUUID, instance.sortFunc)
        make_graph(xs_sort)
    else:
        xs_sort = instance.alsoLikes(docUUID, instance.sortFunc)
        make_graph(xs_sort)



window.mainloop()
#End of window
