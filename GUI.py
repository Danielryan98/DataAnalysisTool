import json
import tkinter as tk
import matplot as mp
import matplotlib.pyplot as plt

from tkinter import * 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)

from Views import Views

class MainGUI:

    #Start of window
    window = tk.Tk()

    window.geometry("800x800")

    #By country button
    by_country_text = tk.StringVar()
    by_country_btn = tk.Button(window, textvariable=by_country_text, font="Arial", bg="Blue", fg="White", height=2, width=10, command="instance.bycountry()")
    by_country_text.set("By Country")
    by_country_btn.place(x=0, y=0)


    #By continent button
    by_continent_text = tk.StringVar()
    by_continent_btn = tk.Button(window, textvariable=by_continent_text, font="Arial", bg="Blue", fg="White", height=2, width=10, command="instance.bycontinent()")
    by_continent_text.set("By Continent")
    by_continent_btn.place(x=0, y=50)


    #By browser button
    by_browser_text = tk.StringVar()
    by_browser_btn = tk.Button(window, textvariable=by_browser_text, font="Arial", bg="Blue", fg="White", height=2, width=10, command=lambda : self.by_browser_plot())
    by_browser_text.set("By Browser")
    by_browser_btn.place(x=0, y=100)

    toolbarFrame = tk.Frame(window)
    toolbarFrame.place(x=150, y=0)

    graphFrame = tk.Frame(window)
    graphFrame.place(x=150, y=50)

    def by_browser_plot(self):
        instance = Views()
        browser_dict = instance.bybrowser()
        self.plot(browser_dict)

    def plot(self, browser_dict):
  
        #Reset toolbar frame to allow for new graph toolbar
        for widget in self.toolbarFrame.winfo_children():
            widget.destroy()

        #Reset chart frame to allow for new graph
        for widget in self.graphFrame.winfo_children():
            widget.destroy()

        # the figure that will contain the plot
        fig = Figure(figsize = (5, 5),
                    dpi = 100)
    
        print(browser_dict.items())
        x = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
        y = [10,8,6,4,2,1]
    
        

        # adding the subplot
        plot1 = fig.add_subplot(111)

        #Set x & y and bar thickness
        plot1.bar(x, y, .5)
    
        # plotting the graph
        plot1.plot()
    
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master = self.graphFrame)  
        canvas.draw()
    
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

    
        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, self.toolbarFrame)
        toolbar.update()
    
        # placing the toolbar on the Tkinter window
        toolbar.pack()


    window.mainloop()
    #End of window
