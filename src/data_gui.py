#Library imports
import tkinter as tk
import graphviz as gv
from subprocess import check_call
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

#Class imports
from functionalities import Functionalities

class DataGUI:
    def __init__(self, file_name):

        self.master = tk.Tk()
        self.views = Functionalities()
        self.views.set_file_name(file_name)

        self.master.config(bg="white")
        self.button_theme = '#1f77b4'
        self.master.geometry("1100x650")

        #Toolbar frame to hold toolbar.
        self.toolbar_frame = tk.Frame(self.master)
        self.toolbar_frame.config(bg="white")
        self.toolbar_frame.place(x=450, y=570)

        #Graph frame to hold the graph.
        self.graph_frame = tk.Frame(self.master)
        self.graph_frame.place(x=70, y=70)


    def by_country_plot(self, doc_id):
        browser_dict = self.views.by_country(doc_id)
        self.plot(browser_dict)    

    def by_continent_plot(self, doc_id):
        browser_dict = self.views.by_continent(doc_id)
        self.plot(browser_dict)

    def by_browser_plot(self):
        browser_dict = self.views.by_browser()
        self.plot(browser_dict)


    def plot(self, browser_dict):

        self.clear_widgets()

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
        plot = fig.add_subplot(111)
        plot.bar(x, y, .5)
        plot.plot()

        # creating the Tkinter canvas containing the Matplotlib figure,
        # and placing the canvas on the Tkinter window.
        canvas = FigureCanvasTkAgg(fig, master = self.graph_frame)  
        canvas.draw()
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar and placing it on the Tkinter window.
        toolbar = NavigationToolbar2Tk(canvas, self.toolbar_frame)
        toolbar.config(bg="white")
        toolbar.update()
        toolbar.pack()

    def clear_widgets(self):
        #Reset toolbar frame to allow for new graph toolbar.
        for widget in self.toolbar_frame.winfo_children():
            widget.destroy()

        #Reset chart frame to allow for new graph.
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

    def format_number(self, num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    def reader_profiles(self):

        users_dict = self.views.user_minutes()

        self.clear_widgets()

        # the figure that will contain the plot
        fig = Figure(figsize = (10, 5),
                dpi = 100)    

        canvas = FigureCanvasTkAgg(fig, master = self.graph_frame)  
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        list_of_readers = tk.Text(self.graph_frame, width=100, height=25)

        users_dict = dict(reversed(list(users_dict.items())[:10]))
        for k in users_dict:
            list_of_readers.insert(1.0, str(k) + " : " + str(users_dict[k]) + "\n")
        list_of_readers.place(x=100, y=25)   
    
    def also_likes(self, doc_id, user_id):
        if not user_id:
            also_likes = self.views.also_likes(doc_id, self.views.sort_func) 
        else:
            also_likes = self.views.also_likes(doc_id, user_id, self.views.sort_func) 

        self.clear_widgets()
        # the figure that will contain the plot
        fig = Figure(figsize = (10, 5),
                dpi = 100)    

        canvas = FigureCanvasTkAgg(fig, master = self.graph_frame)  
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        list_of_docs = tk.Text(self.graph_frame, width=100, height=25)

        for count in also_likes[:11]:
            list_of_docs.insert(tk.END, str(count[1]) + " : " + str(count[0]) + "\n")
        list_of_docs.place(x=100, y=25) 

    def also_likes_graph(self, doc_id, user_id):
        if not user_id:
            also_likes = self.views.also_likes(doc_id, self.views.sort_func) 
        else:
            also_likes = self.views.also_likes(doc_id, user_id, self.views.sort_func) 

        self.clear_widgets()
        
        #Format the key data so that it's in format 300k, 1m, 3m etc.
        data_size = self.format_number(self.views.data_list.__len__())

        #Slice the id's so that we only work with the last 4 characters. 
        main_user_id = user_id[-4:]
        main_doc_id = doc_id[-4:]

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

        for count in also_likes[:11]:
            if count[1][-4:] == main_doc_id:
                dot.node(count[1][-4:], count[1][-4:], shape=has_read_shape, color='green', style='filled')
            else:
                dot.node(count[1][-4:], count[1][-4:], shape=has_read_shape)
            for user in count[2]:
                if user[-4:] == main_user_id:
                    dot.node(user[-4:], user[-4:], shape=user_shape, color='green', style='filled')
                    dot.edge(user[-4:], count[1][-4:])
                else:
                    dot.node(user[-4:], user[-4:], shape=user_shape)
                    dot.edge(user[-4:], count[1][-4:])

        print(dot.source)

        with open('output\graph.dot', "w") as dotfile:
            dotfile.truncate(0)
            dotfile.write(dot.source)
            dotfile.close()

    
        check_call(['dot','-Tpng','output\graph.dot','-o','output\graph.png'])

        img_arr = mpimg.imread('output\graph.png')

        # adding the subplot
        plot = fig.add_subplot(111)

        # plotting the graph
        plot.axis('off')
        plot.imshow(img_arr)
        

        canvas = FigureCanvasTkAgg(fig, master = self.graph_frame)  
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()


