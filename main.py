#from tkinter import *
# from tkinter import font as tkFont
from tkinter import filedialog
from math import ceil, floor
# import PIL.Image
# import PIL.ImageTk
from tree_and_node import *
import functools

class App: #GOOD TO GO

    #Helpers
    def _get_file_from_user(self):
        file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Pickle files", "*.pickle"), \
                        ("All files", "*.*")], initialdir = "saved_trees")
        return file_path
    
    #Postdialog functions
    def postdialog_create_cur_tree(self, _):
        self.tree_creation_dialog.destroy()
        self.main_menu.destroy()
        self.main_menu = None

        tree = Tree(self.subject.get())
        tree.run()
        main()



    #Dialog functions
    def dialog_make_new_tree(self):

        self.tree_creation_dialog = Toplevel(takefocus=True)
        self.tree_creation_dialog.attributes("-topmost", True)
        self.tree_creation_dialog.grab_set()
        self.tree_creation_dialog.bind('<Return>', self.postdialog_create_cur_tree)

        self.subject = StringVar()
        self.inputtxt = Entry(self.tree_creation_dialog, textvariable=self.subject)
        self.inputtxt.pack()
        self.printButton = Button(self.tree_creation_dialog, text = "Submit", \
                            command = self.postdialog_create_cur_tree)
        self.printButton.pack()

    #Window-building functions
    def init_main_menu(self):
        self.main_menu = Tk()
        self.main_menu.geometry("600x600")

        self.make_new_tree_button = Button(self.main_menu, text ="Make new tree", \
                                           command = self.dialog_make_new_tree)
        self.load_existing_tree_button = Button(self.main_menu, text ="Load existing tree", \
                                                command = self.load_existing_tree)
        self.make_new_tree_button.place(x=50,y=50)
        self.load_existing_tree_button.place(x=50, y=100)

    #Top-level functions
    def load_existing_tree(self):
        file_path = self._get_file_from_user()

        if file_path:
            self.main_menu.destroy()
            self.main_menu = None
        else:
            print("Something went wrong.")
            return

        with open(file_path, "rb") as infile:
            tree_payload = pickle.load(infile)
 
        tree = Tree._construct_from_payload(tree_payload)
        tree.redraw()
        tree.run()
        main()

    def run(self):
        self.main_menu.mainloop()

    def __init__(self):
        self.init_main_menu()

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()