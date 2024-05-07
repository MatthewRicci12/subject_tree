#from tkinter import *
from tkinter import font as tkFont
from math import ceil, floor
import PIL.Image
import PIL.ImageTk
from tree_and_node import *



class App:

    def load_existing_tree(self):
        pass

    def return_to_main_menu(self):

        self.tree_window.destroy()
        self.tree_window = None
        self.cur_tree = None
        self.top_node_exists = False
        self.main_menu = Tk()
        self.main_menu.geometry("600x600")

        self.make_new_tree_button = Button(self.main_menu, text ="Make new tree", command = self.make_new_tree)
        self.load_existing_tree_button = Button(self.main_menu, text ="Load existing tree", command = self.load_existing_tree)
        self.make_new_tree_button.place(x=50,y=50)
        self.load_existing_tree_button.place(x=50, y=100)

        self.main_menu.mainloop()


    def create_cur_tree(self, subject):
        self.cur_tree = Tree(self.canvas, subject, self.tree_window)
        #self.tree_creation_dialog.destroy()
        self.init_side_frame()

        #DO stuff here
        for i in range(1, 100):
            self.cur_tree.add_node(self.canvas, self.cur_tree.root, "Linear Algebra{}".format(i))



    def move(self, amount):
        self.central_node = self.cur_tree.central_node
        if len(self.central_node.children) < 35:
            return
        self.central_node.sliding_window_start += amount
        self.cur_tree.redraw(self.canvas)

    def init_side_frame(self):
        self.frame = Frame(self.tree_window,bg='orange',width=200,height=800)
        self.frame.pack(side=LEFT)
        self.frame.columnconfigure(0, weight = 1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.back_button = Button(self.frame, relief='flat', bg='orange', text='Back', height=5, \
                                  command=self.return_to_main_menu)
        self.back_button.grid(row=0, column=0, sticky="ew")
        helv36 = tkFont.Font(family='Helvetica', size=24)
        self.back_button['font'] = helv36

        self.button_frame = Frame(self.frame, bg="orange")
        self.button_frame.grid(row=1, column=0)

        self.left_icon = PIL.ImageTk.PhotoImage(PIL.Image.open('icons/leftarrow.png').resize((30,30)))
        self.right_icon = PIL.ImageTk.PhotoImage(PIL.Image.open('icons/rightarrow.png').resize((30,30)))
        self.left_button = Button(self.button_frame, relief='flat', bg='orange', command=lambda \
                                                        canvas=self.canvas: self.move(-5))
        self.right_button = Button(self.button_frame, relief='flat', bg='orange', command=lambda \
                                                        canvas=self.canvas: self.move(5))
        self.left_button.config(image=self.left_icon)
        self.left_button.image = self.left_icon
        self.right_button.config(image=self.right_icon)
        self.right_button.image = self.right_icon
        self.left_button.grid(row = 0, column = 0)
        self.right_button.grid(row = 0, column = 1)


        self.depth_label = Label(self.frame, text = "Depth={}".format(self.cur_tree.central_node.depth), bg='orange',font=('Helvetica', 20))
        self.depth_label.grid(row = 2, column = 0, sticky="s")


        self.frame.grid_propagate(False)


    def make_new_tree(self):

        self.main_menu.destroy()
        self.main_menu = None

        self.tree_window = Tk()
        self.tree_window.geometry("1000x600")
        self.canvas = Canvas(self.tree_window, width = 1100 - 120, height = 800)
        self.canvas.pack(side = RIGHT, fill = BOTH, expand = True)

        if not self.top_node_exists:
            self.tree_creation_dialog = Toplevel(takefocus=True)
            self.tree_creation_dialog.attributes("-topmost", True)
            self.tree_creation_dialog.grab_set()

            subject = StringVar()
            self.inputtxt = Entry(self.tree_creation_dialog, textvariable=subject) 
            self.inputtxt.pack() 
            self.printButton = Button(self.tree_creation_dialog, text = "Submit", \
                                command = lambda subject=subject, canvas=self.canvas, \
                                tree_creation_dialog=self.tree_creation_dialog: \
                                self.create_cur_tree(subject.get())) 
            self.printButton.pack()
            self.top_node_exists = True


        self.tree_window.mainloop()  


    def init_main_menu(self):
        self.main_menu = Tk()
        self.main_menu.geometry("600x600")

        self.make_new_tree_button = Button(self.main_menu, text ="Make new tree", \
                                           command = self.make_new_tree)
        self.load_existing_tree_button = Button(self.main_menu, text ="Load existing tree", \
                                                command = self.load_existing_tree)
        self.make_new_tree_button.place(x=50,y=50)
        self.load_existing_tree_button.place(x=50, y=100)

        self.main_menu.mainloop()

    def __init__(self):
        # self.top_node_exists = False
        # self.init_main_menu()
        self.tree_window = Tk()
        self.tree_window.geometry("1000x600")
        self.canvas = Canvas(self.tree_window, width = 1100 - 120, height = 800)
        self.canvas.pack(side = RIGHT, fill = BOTH, expand = True)
        self.create_cur_tree("za")

    def run(self):
        self.tree_window.mainloop()
        #self.main_menu.mainloop()


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()