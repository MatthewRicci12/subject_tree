from tkinter import *
from tkinter import messagebox
from subjectnode import *

top = Tk()
top.geometry("600x600")

top_node_exists = False


def make_new_tree():
    top.destroy()
    newWindow = Tk()
    newWindow.geometry("1000x600")

    if not top_node_exists:
        win = Toplevel(takefocus=True)
        win.attributes("-topmost", True)
        win.grab_set()
        
        subject = StringVar()
        inputtxt = Entry(win, textvariable=subject) 
        inputtxt.pack() 
        printButton = Button(win, 
                                text = "Submit",  
                                command = lambda: create_subject_node(newWindow, win, inputtxt)) 
        printButton.pack()

    newWindow.mainloop()  


def load_existing_tree():
    pass


def node_double_clicked(event):
    messagebox.showinfo("ye", "LETS FUCKING GOOOOOOO")

def create_subject_node(newWindow, dialog, inputtxt):
    subject = inputtxt.get()
    dialog.destroy()

    newWindow.columnconfigure(0, weight=1)
    newWindow.rowconfigure(0, weight=1)

    canvas = Canvas(newWindow)
    canvas.grid(column=0, row=0, sticky=(N, W, E, S))

    half_width = newWindow.winfo_width() >> 1
    half_height = newWindow.winfo_height() >> 1

    top_subject_node = subjectNode(subject, half_width, half_height, 50, canvas, node_double_clicked)
    x=top_subject_node.get_tkinter_id()
    canvas.tag_bind(top_subject_node.get_tkinter_id(), '<ButtonPress-1>', node_double_clicked)

    button = Button(newWindow, text="submit", command=node_double_clicked)
    

make_new_tree_button = Button(top, text ="Make new tree", command = make_new_tree)
load_existing_tree_button = Button(top, text ="Load existing tree", command = load_existing_tree)
make_new_tree_button.place(x=50,y=50)
load_existing_tree_button.place(x=50, y=100)

top.mainloop()

