#from tkinter import *
# from tkinter import font as tkFont
from math import ceil, floor
# import PIL.Image
# import PIL.ImageTk
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

        #DO stuff here
        # for i in range(1, 5):
        #     self.cur_tree.add_node(self.cur_tree.root, "Linear Algebra{}".format(i))



    def move(self, amount):
        self.central_node = self.cur_tree.central_node
        if len(self.central_node.children) < 35:
            return
        self.central_node.sliding_window_start += amount
        self.cur_tree.redraw(self.canvas)




    def make_new_tree(self):

        self.main_menu.destroy() #1
        self.main_menu = None#1

        self.tree_window = Tk()
        self.tree_window.geometry("1000x600")
        self.canvas = Canvas(self.tree_window, width = 1100 - 120, height = 800)
        self.canvas.pack(side = RIGHT, fill = BOTH, expand = True)

        if not self.top_node_exists: #1
            self.tree_creation_dialog = Toplevel(takefocus=True) #1
            self.tree_creation_dialog.attributes("-topmost", True) #1
            self.tree_creation_dialog.grab_set() #1

            subject = StringVar() #1
            self.inputtxt = Entry(self.tree_creation_dialog, textvariable=subject) #1
            self.inputtxt.pack()  #1
            self.printButton = Button(self.tree_creation_dialog, text = "Submit", \
                                command = lambda subject=subject, canvas=self.canvas, \
                                tree_creation_dialog=self.tree_creation_dialog: \
                                self.create_cur_tree(subject.get()))  #1
            self.printButton.pack() #1
            self.top_node_exists = True #1

        #self.create_cur_tree("asdf") #delete when done #2

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
        #self.make_new_tree() #2
        self.top_node_exists = False #1
        self.init_main_menu() #1
        self.tree_window = Tk() #1
        self.tree_window.geometry("1000x600") #1
        self.canvas = Canvas(self.tree_window, width = 1100 - 120, height = 800) #1
        self.canvas.pack(side = RIGHT, fill = BOTH, expand = True) #1

    def run(self):
        #self.tree_window.mainloop() #2
        self.main_menu.mainloop() #1


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()