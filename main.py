from tkinter import *
from tkinter import font as tkFont
from math import ceil, floor
from PIL import Image, ImageTk
from tree_and_node import *




top = None
newWindow = None
cur_tree = None
top_node_exists = False



def create_cur_tree(inputtxt, canvas, win):
    global cur_tree, newWindow

    cur_tree = Tree(canvas, inputtxt)
    win.destroy()
    init_frame(newWindow)


    #DO stuff here
    for i in range(1, 100):
        cur_tree.add_node(canvas, cur_tree.root, "Linear Algebra{}".format(i))


def make_new_tree():

    global newWindow, top, cur_tree, top_node_exists

    top.destroy()
    top = None

    newWindow = Tk()
    newWindow.geometry("1000x600")
    canvas = Canvas(newWindow, width = 1100 - 120, height = 800)
    canvas.pack(side = RIGHT, fill = BOTH, expand = True)

    if not top_node_exists:
        win = Toplevel(takefocus=True)
        win.attributes("-topmost", True)
        win.grab_set()

        subject = StringVar()
        inputtxt = Entry(win, textvariable=subject) 
        inputtxt.pack() 
        printButton = Button(win, text = "Submit", \
                             command = lambda subject=subject, canvas=canvas, win=win: create_cur_tree(subject.get(), canvas, win)) 
        printButton.pack()
        top_node_exists = True


    newWindow.mainloop()  


def return_to_main_menu():
    global newWindow, cur_tree, top_node_exists, top

    newWindow.destroy()
    newWindow = None
    cur_tree = None
    top_node_exists = False
    top = Tk()
    top.geometry("600x600")

    make_new_tree_button = Button(top, text ="Make new tree", command = make_new_tree)
    load_existing_tree_button = Button(top, text ="Load existing tree", command = load_existing_tree)
    make_new_tree_button.place(x=50,y=50)
    load_existing_tree_button.place(x=50, y=100)

    top.mainloop()


def move_left():
    pass

def move_right():
    pass

def init_frame(root):
    global cur_tree

    frame = Frame(root,bg='orange',width=200,height=800)
    frame.pack(side=LEFT)
    frame.columnconfigure(0, weight = 1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(1, weight=1)

    back_button = Button(frame, relief='flat', bg='orange', text='Back', height=5, command=return_to_main_menu)
    back_button.grid(row=0, column=0, sticky="ew")
    helv36 = tkFont.Font(family='Helvetica', size=24)
    back_button['font'] = helv36

    button_frame = Frame(frame, bg="orange")
    button_frame.grid(row=1, column=0)

    left_icon = ImageTk.PhotoImage(Image.open('icons/leftarrow.png').resize((30,30)))
    right_icon = ImageTk.PhotoImage(Image.open('icons/rightarrow.png').resize((30,30)))
    left_button = Button(button_frame, relief='flat', bg='orange', command=move_left)
    right_button = Button(button_frame, relief='flat', bg='orange', command=move_right)
    left_button.config(image=left_icon)
    left_button.image = left_icon
    right_button.config(image=right_icon)
    right_button.image = right_icon
    left_button.grid(row = 0, column = 0)
    right_button.grid(row = 0, column = 1)


    depth_label = Label(frame, text = "Depth={}".format(cur_tree.central_node.depth), bg='orange',font=('Helvetica', 20))
    depth_label.grid(row = 2, column = 0, sticky="s")


    frame.grid_propagate(False)


def load_existing_tree():
    pass



top = Tk()
top.geometry("600x600")

make_new_tree_button = Button(top, text ="Make new tree", command = make_new_tree)
load_existing_tree_button = Button(top, text ="Load existing tree", command = load_existing_tree)
make_new_tree_button.place(x=50,y=50)
load_existing_tree_button.place(x=50, y=100)

top.mainloop()
