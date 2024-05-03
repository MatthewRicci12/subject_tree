from tkinter import *
from tkinter import messagebox

class App:
    def hey(self,s): 
        messagebox.showinfo("That zaza got me speakin' Esperanto",  s) 

    def do_popup(self,event): 
        try: 
            self.popup_menu.tk_popup(event.x_root, 
                                     event.y_root) 
        finally: 
            self.popup_menu.grab_release() 

    def __init__(self):
        self.root = Tk()
        self.root.geometry("1200x800")
        self.canvas = Canvas(self.root, width=1200, height=800)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        circle_id = self.canvas.create_oval((600, 300), (700, 400), fill='white')

        self.popup_menu = Menu(self.root, 
                                       tearoff = 0) 
          
        self.popup_menu.add_command(label = "say hi", 
                                    command = lambda:self.hey("hi")) 
          
        self.popup_menu.add_command(label = "say hello", 
                                    command = lambda:self.hey("hello")) 
        self.popup_menu.add_separator() 
        self.popup_menu.add_command(label = "say bye", 
                                    command = lambda:self.hey("bye")) 
        
        self.canvas.tag_bind(circle_id, '<Button-3>', self.do_popup)

        self.root.mainloop()

    def do_popup(self, event): 
        try: 
            self.popup_menu.tk_popup(event.x_root, 
                                     event.y_root) 
        finally: 
            self.popup_menu.grab_release() 


app = App()