import tkinter as tk
from tkinter import ttk
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
        self.master.resizable('false', 'false')
        self.master.config(bg="white")
        self.button_theme = '#1f77b4'
        self.master.geometry("1100x700")

        #Document ID Input Label.
        self.document_uuid_label = tk.Label(self.master, text="document_uuid", font="Arial", height=2, width=12, bg="white")
        self.document_uuid_label.place(x=30, y=20)

        #Document ID Input Box.
        self.document_uuid = ttk.Combobox(self.master, width=75, postcommand=lambda:self.update_doc_history_list()) 
        self.document_uuid.place(x=150, y=32)

        #User ID Input Label.
        self.visitor_uuid_label = tk.Label(self.master, text="visitor_uuid", font="Arial", height=2, width=12, bg="white")
        self.visitor_uuid_label.place(x=45, y=53)

        #User ID Input Box.
        self.visitor_uuid = ttk.Combobox(self.master, width=75, postcommand=lambda:self.update_vis_history_list()) 
        self.visitor_uuid.place(x=150, y=65)

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
        self.upload_json_btn.place(x=45, y=125)

        #By country button.
        self.by_country_text = tk.StringVar()
        self.by_country_btn = tk.Button(self.master, textvariable=self.by_country_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda: self.by_country_plot())
        self.by_country_text.set("By Country")
        self.by_country_btn.place(x=45, y=185)

        #By continent button.
        self.by_continent_text = tk.StringVar()
        self.by_continent_btn = tk.Button(self.master, textvariable=self.by_continent_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda: self.by_continent_plot())
        self.by_continent_text.set("By Continent")
        self.by_continent_btn.place(x=45, y=245)

        #By browser full button.
        self.by_browser_full_text = tk.StringVar()
        self.by_browser_full_btn = tk.Button(self.master, textvariable=self.by_browser_full_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : self.by_browser_plot(self.views.BROWSER_FULL))
        self.by_browser_full_text.set("By Browser (Full)")
        self.by_browser_full_btn.place(x=45, y=305)

        #By browser button.
        self.by_browser_text = tk.StringVar()
        self.by_browser_btn = tk.Button(self.master, textvariable=self.by_browser_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : self.by_browser_plot(self.views.BROWSER_SHORT))
        self.by_browser_text.set("By Browser (Short)")
        self.by_browser_btn.place(x=45, y=365)

        #Reader profiles button.
        self.reader_profiles_text = tk.StringVar()
        self.reader_profiles_btn = tk.Button(self.master, textvariable=self.reader_profiles_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : self.reader_profiles())
        self.reader_profiles_text.set("Reader Profiles")
        self.reader_profiles_btn.place(x=45, y=425)

        #Also likes button.
        self.also_likes_text = tk.StringVar()
        self.also_likes_btn = tk.Button(self.master, textvariable=self.also_likes_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : self.also_likes())
        self.also_likes_text.set("Also Likes")
        self.also_likes_btn.place(x=45, y=485)

        #Also likes graph button.
        self.also_likes_graph_text = tk.StringVar()
        self.also_likes_graph_btn = tk.Button(self.master, textvariable=self.also_likes_graph_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : self.also_likes_graphs())
        self.also_likes_graph_text.set("Also Likes Graph")
        self.also_likes_graph_btn.place(x=45, y=545)

        #how_to button.
        self.how_to_text = tk.StringVar()
        self.how_to_btn = tk.Button(self.master, textvariable=self.how_to_text, font="Arial", bg=self.button_theme, fg="White", borderwidth=5, highlightbackground="black", highlightthickness=2, height=2, width=15, command=lambda : self.also_likes_graphs())
        self.how_to_text.set("How-to")
        self.how_to_btn.place(x=45, y=605)

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
        panel.place(x=640, y=5)

    def update_doc_history_list(self):
        doc_hist_list = []
        with open("doc_history.txt", "r+") as file:
            doc_hist_list = [line.rstrip() for line in file]
        file.close()
        doc_hist_list.reverse()
        self.document_uuid['values'] = doc_hist_list

    def add_doc_history(self, doc_uuid):
        if doc_uuid:
            lines = []
            with open("doc_history.txt", "r+") as file:
                lines = [line.rstrip() for line in file]
                file.truncate(0)
                file.close()
            with open("doc_history.txt", "r+") as file:
                for line in lines:
                    if line == doc_uuid:
                        lines.remove(line)
                lines.append(doc_uuid)
                for line in lines:
                    file.write(line+"\n")
                file.close()
        
    def update_vis_history_list(self):
        vis_hist_list = []
        with open("vis_history.txt", "r+") as file:
            vis_hist_list = [line.rstrip() for line in file]
        file.close()
        vis_hist_list.reverse()
        self.visitor_uuid['values'] = vis_hist_list

    def add_vis_history(self, vis_uuid):
        if vis_uuid:
            lines = []
            with open("vis_history.txt", "r+") as file:
                lines = [line.rstrip() for line in file]
                file.truncate(0)
                file.close()
            with open("vis_history.txt", "r+") as file:
                for line in lines:
                    if line == vis_uuid:
                        lines.remove(line)
                lines.append(vis_uuid)
                for line in lines:
                    file.write(line+"\n")
                file.close()

    def check_doc_id(self, doc_id):
        return re.findall("^([0-9]{12})-([a-z]|[0-9]){32}$", doc_id)

    def check_user_id(self, user_id):
        return re.findall("^([0-9]|[a-z]){16}$", user_id)

    def check_for_data(self):
        data = self.views.data_list
        if not data:
            self.error_message("oops!", "Please provide a valid JSON file, and then try again.")
        else:
            return True

    def by_country_plot(self):
        # get doc_id from input

        if self.check_for_data():
            doc_id = self.document_uuid.get()
            try:
                if self.check_doc_id(doc_id):
                    browser_dict = self.views.by_country(doc_id)
                    self.plot(browser_dict)
                else:
                    raise ValueError
            except ValueError:
                self.error_message("oops!", "Invalid document uuid. Please rectify, and then try again.")

    def by_continent_plot(self):
        data = self.views.data_list
        if not data:
            self.error_message("oops!", "Please provide a valid JSON file, and then try again.")
        else:
            # get doc_id from input
            doc_id = self.document_uuid.get()
            try:
                if self.check_doc_id(doc_id):
                    browser_dict = self.views.by_continent(doc_id)
                    self.plot(browser_dict)
                else:
                    raise ValueError
            except ValueError:
                self.error_message("oops!", "Invalid document UUID. Please rectify and then try again.")

    def by_browser_plot(self, type):
        if self.check_for_data():
            browser_dict = self.views.by_browser(type)
            self.plot(browser_dict)

    def plot(self, browser_dict):

        self.add_vis_history(self.visitor_uuid.get())
        self.add_doc_history(self.document_uuid.get())

        self.clear_widgets()

        print(browser_dict.items())

        x_items = []
        y_items = []

        for k, v in browser_dict.items():
            x_items.append(k)
            y_items.append(v)

        #Figure that will contain the plot.
        fig = Figure(figsize = (10, 5),
                dpi = 100)

        # Create the subplot. Set x & y and bar thickness. Plot the graph.
        plot = fig.add_subplot(111)
        plot.bar(x_items, y_items, .5)
        plot.plot()

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

        if self.check_for_data():

            users_dict = self.views.user_minutes()

            self.add_vis_history(self.visitor_uuid.get())
            self.add_doc_history(self.document_uuid.get())

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
 

    def also_likes(self):

        if self.check_for_data():
            try:
                if self.check_doc_id(self.document_uuid.get()):
                    self.add_vis_history(self.visitor_uuid.get())
                    self.add_doc_history(self.document_uuid.get())
                    # get doc_id from input
                    doc_id = self.document_uuid.get()
                    # get vis_id from input
                    user_id = self.visitor_uuid.get()
                    if not user_id:
                        also_likes = self.views.also_likes(doc_id, self.views.sort_func) 
                    else:
                        try:
                            if self.check_user_id(user_id):
                                also_likes = self.views.also_likes(doc_id, user_id, self.views.sort_func) 
                            else:
                                raise ValueError
                        except ValueError:
                            self.error_message("oops!", "Invalid user UUID. Please rectify and then try again.")

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
                else:
                    raise ValueError
            except ValueError:
                self.error_message("oops!", "Invalid document UUID. Please rectify and then try again.")

             

    def also_likes_graphs(self):

        if self.check_for_data():
            try:
                if self.check_doc_id(self.document_uuid.get()):
                    # get doc_id from input
                    doc_id = self.document_uuid.get()
                    # get vis_id from input
                    user_id = self.visitor_uuid.get()
                    if not user_id:
                        also_likes = self.views.also_likes(doc_id, self.views.sort_func) 
                    else:
                        try:
                            if self.check_user_id(user_id):
                                also_likes = self.views.also_likes(doc_id, user_id, self.views.sort_func) 
                            else:
                                raise ValueError
                        except ValueError:
                            self.error_message("oops!", "Invalid user UUID. Please rectify and then try again.")

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

                    with open('graph.dot', "w") as dot_file:
                        dot_file.truncate(0)
                        dot_file.write(dot.source)
                        dot_file.close()

                
                    check_call(['dot','-Tpng','graph.dot','-o','graph.png'])

                    img_arr = mpimg.imread('graph.png')

                    # adding the subplot
                    plot = fig.add_subplot(111)

                    # plotting the graph
                    plot.axis('off')
                    plot.imshow(img_arr)
                    

                    canvas = FigureCanvasTkAgg(fig, master = self.graphFrame)  
                    canvas.draw()

                    # placing the canvas on the Tkinter window
                    canvas.get_tk_widget().pack()
                else:
                    raise ValueError
            except ValueError:
                self.error_message("oops!", "Invalid document UUID. Please rectify and then try again.")
            

    def error_message(self, title, message):
        tk.messagebox.showinfo(title, message)

def main():
    root = tk.Tk()
    app = GUI2(root)
    root.mainloop()

# if __name__ == '__main__':
#     main()