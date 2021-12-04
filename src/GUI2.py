import tkinter as tk
import re
from tkinter import font
from tkinter.constants import DISABLED
from matplotlib import use
import matplotlib.pyplot as plt
import graphviz as gv
from subprocess import check_call
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from PIL import ImageTk, Image
from Views2 import Views2
from future.moves.tkinter import filedialog

class GUI2:
    def __init__(self, master):

        self.views = Views2()

        self.master = master
        self.master.config(bg="white")
        self.button_theme = '#1f77b4'
        self.master.geometry("1100x650")

        #Document ID Input Label.
        self.document_uuid_label = tk.Label(self.master, text="document_uuid", font="Arial", height=2, width=12, bg="white")
        self.document_uuid_label.place(x=30, y=20)

        #Document ID Input Box.
        self.document_uuid = tk.Entry(self.master, width=75, borderwidth=2) 
        self.document_uuid.place(x=150, y=32)

        #User ID Input Label.
        self.visitor_uuid_label = tk.Label(self.master, text="visitor_uuid", font="Arial", height=2, width=12, bg="white")
        self.visitor_uuid_label.place(x=45, y=51)

        #User ID Input Box.
        self.visitor_uuid = tk.Entry(self.master, width=75, borderwidth=2) 
        self.visitor_uuid.place(x=150, y=63)

        #Toolbar frame to hold toolbar.
        self.toolbarFrame = tk.Frame(self.master)
        self.toolbarFrame.config(bg="white")
        self.toolbarFrame.place(x=535, y=600)

        #Graph frame to hold the graph.
        self.graphFrame = tk.Frame(self.master)
        self.graphFrame.place(x=155, y=100)

        #Upload json button.
        self.upload_json_text = tk.StringVar()
        self.upload_json_btn = tk.Button(self.master, textvariable=self.upload_json_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda: self.get_file_from_user())
        self.upload_json_text.set("Upload json")
        self.upload_json_btn.place(x=45, y=100)

        #By country button.
        self.by_country_text = tk.StringVar()
        self.by_country_btn = tk.Button(self.master, textvariable=self.by_country_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda: self.by_country_plot())
        self.by_country_text.set("By Country")
        self.by_country_btn.place(x=45, y=160)

        #By continent button.
        self.by_continent_text = tk.StringVar()
        self.by_continent_btn = tk.Button(self.master, textvariable=self.by_continent_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda: self.by_continent_plot())
        self.by_continent_text.set("By Continent")
        self.by_continent_btn.place(x=45, y=220)

        #By browser button.
        self.by_browser_text = tk.StringVar()
        self.by_browser_btn = tk.Button(self.master, textvariable=self.by_browser_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : self.by_browser_plot())
        self.by_browser_text.set("By Browser")
        self.by_browser_btn.place(x=45, y=280)

        #Reader profiles button.
        self.reader_profiles_text = tk.StringVar()
        self.reader_profiles_btn = tk.Button(self.master, textvariable=self.reader_profiles_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : self.reader_profiles())
        self.reader_profiles_text.set("Reader Profiles")
        self.reader_profiles_btn.place(x=45, y=340)

        #Also likes button.
        self.also_likes_text = tk.StringVar()
        self.also_likes_btn = tk.Button(self.master, textvariable=self.also_likes_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : self.alsoLikes())
        self.also_likes_text.set("Also Likes")
        self.also_likes_btn.place(x=45, y=400)

        #Also likes graph button.
        self.also_likes_graph_text = tk.StringVar()
        self.also_likes_graph_btn = tk.Button(self.master, textvariable=self.also_likes_graph_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : self.alsoLikesGraph())
        self.also_likes_graph_text.set("Also Likes Graph")
        self.also_likes_graph_btn.place(x=45, y=460)

        #History button.
        self.history_text = tk.StringVar()
        self.history_btn = tk.Button(self.master, textvariable=self.history_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : self.alsoLikesGraph())
        self.history_text.set("History")
        self.history_btn.place(x=45, y=520)

        #how_to button.
        self.how_to_text = tk.StringVar()
        self.how_to_btn = tk.Button(self.master, textvariable=self.how_to_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : self.alsoLikesGraph())
        self.how_to_text.set("How-to")
        self.how_to_btn.place(x=45, y=580)

        self.paint_logo()

    def get_file_from_user(self):
        file = filedialog.askopenfilename()
        if file: #If they choose a file rather than cancelling           
            self.views.set_file_name(file)

    def paint_logo(self):
        global img
        path = "logonew.jpg"
        img= (Image.open(path))
        img = img.resize((425,100), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(self.master, image=img, height=100, width=425, bd=0)
        panel.place(x=625, y=0)

    def checkDocID(self, doc_id):
        return re.findall("^([0-9]{12})-([a-z]|[0-9]){32}$", doc_id)

    def checkUserID(self, user_id):
        return re.findall("^([0-9]|[a-z]){16}$", user_id)

    def by_country_plot(self):
        # get doc_id from input
        doc_id = self.document_uuid.get()
        if (self.checkDocID(doc_id)):
            browser_dict = self.views.bycountry(doc_id)
            self.plot(browser_dict)
        else:
            self.document_uuid.delete(0, 'end')
            self.document_uuid.insert(0, "Not a valid document UUID. Please enter another one...")

    def by_continent_plot(self):
        # get doc_id from input
        doc_id = self.document_uuid.get()
        if (self.checkDocID(doc_id)):
            browser_dict = self.views.bycontinent(doc_id)
            self.plot(browser_dict)
        else:
            self.document_uuid.delete(0, 'end')
            self.document_uuid.insert(0, "Not a valid document UUID. Please enter another one...")

    def by_browser_plot(self):
        browser_dict = self.views.bybrowser()
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
        plot1 = fig.add_subplot(111)
        plot1.bar(x, y, .5)
        plot1.plot()

        # creating the Tkinter canvas containing the Matplotlib figure,
        # and placing the canvas on the Tkinter window.
        canvas = FigureCanvasTkAgg(fig, master = self.graphFrame)  
        canvas.draw()
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar and placing it on the Tkinter window.
        toolbar = NavigationToolbar2Tk(canvas, self.toolbarFrame)
        toolbar.config(bg="white")
        toolbar.update()
        toolbar.pack()

    def clear_widgets(self):
        #Reset toolbar frame to allow for new graph toolbar.
        for widget in self.toolbarFrame.winfo_children():
            widget.destroy()

        #Reset chart frame to allow for new graph.
        for widget in self.graphFrame.winfo_children():
            widget.destroy()

    def format_number(self, num):
        num = float('{:.3g}'.format(num))
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

    def reader_profiles(self):

        users_dict = self.views.userMinutes()

        self.clear_widgets()

        # the figure that will contain the plot
        fig = Figure(figsize = (10, 5),
                dpi = 100)    

        canvas = FigureCanvasTkAgg(fig, master = self.graphFrame)  
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        list_of_readers = tk.Text(self.graphFrame, width=100, height=25)

        users_dict = dict(reversed(list(users_dict.items())[:10]))
        for k in users_dict:
            list_of_readers.insert(1.0, str(k) + " : " + str(users_dict[k]) + "\n")
        list_of_readers.place(x=100, y=25)   

    def add_to_history(self, doc_uuid, vis_uuid):
        print("will show doc uuid : vis_uuid")
        

    def alsoLikes(self):
        # get doc_id from input
        doc_id = self.document_uuid.get()
        # get vis_id from input
        user_id = self.visitor_uuid.get()
        if not user_id:
            also_likes = self.views.alsoLikes(doc_id, self.views.sortFunc) 
        else:
            also_likes = self.views.alsoLikes(doc_id, user_id, self.views.sortFunc) 

        self.clear_widgets()
        # the figure that will contain the plot
        fig = Figure(figsize = (10, 5),
                dpi = 100)    

        canvas = FigureCanvasTkAgg(fig, master = self.graphFrame)  
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        list_of_docs = tk.Text(self.graphFrame, width=100, height=25)

        for count in also_likes[:11]:
            list_of_docs.insert(tk.END, str(count[1]) + " : " + str(count[0]) + "\n")
        list_of_docs.place(x=100, y=25) 

    def alsoLikesGraph(self):
        # get doc_id from input
        doc_id = self.document_uuid.get()
        # get vis_id from input
        user_id = self.visitor_uuid.get()
        if not user_id:
            also_likes = self.views.alsoLikes(doc_id, self.views.sortFunc) 
        else:
            also_likes = self.views.alsoLikes(doc_id, user_id, self.views.sortFunc) 

        self.clear_widgets()
        
        #Format the key data so that it's in format 300k, 1m, 3m etc.
        data_size = self.format_number(self.views.dataList.__len__())

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
        

        canvas = FigureCanvasTkAgg(fig, master = self.graphFrame)  
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()