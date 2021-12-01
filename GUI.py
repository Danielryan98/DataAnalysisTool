import json
import tkinter as tk
import matplot as mp
import matplotlib.pyplot as plt

from tkinter import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

from Views import Views

doc_id = "140222143932-91796b01f94327ee809bd759fd0f6c76"

#Start of window
window = tk.Tk()

window.geometry("800x800")

#Document ID Input Label
input_doc_id_label = tk.Label(window, text="Input doc_id", font="Arial", height=2, width=10)
input_doc_id_label.place(x=0, y=0)


#Document ID Input Box
input_doc_id = tk.Entry(window) 
input_doc_id.place(x=0, y=50)


#By country button
by_country_text = tk.StringVar()
by_country_btn = tk.Button(window, textvariable=by_country_text, font="Arial", bg="Blue", fg="White", height=2, width=10, command=lambda: by_country_plot(doc_id))
by_country_text.set("By Country")
by_country_btn.place(x=0, y=100)


#By continent button
by_continent_text = tk.StringVar()
by_continent_btn = tk.Button(window, textvariable=by_continent_text, font="Arial", bg="Blue", fg="White", height=2, width=10, command=lambda: by_continent_plot(doc_id))
by_continent_text.set("By Continent")
by_continent_btn.place(x=0, y=150)


#By browser button
by_browser_text = tk.StringVar()
by_browser_btn = tk.Button(window, textvariable=by_browser_text, font="Arial", bg="Blue", fg="White", height=2, width=10, command=lambda : by_browser_plot())
by_browser_text.set("By Browser")
by_browser_btn.place(x=0, y=200)

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

    #Reset toolbar frame to allow for new graph toolbar
    for widget in toolbarFrame.winfo_children():
        widget.destroy()

    #Reset chart frame to allow for new graph
    for widget in graphFrame.winfo_children():
        widget.destroy()

    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5),
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


window.mainloop()
#End of window
