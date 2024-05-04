from tkinter import *
from tkinter import messagebox
import random



class Note:

    def popup_textbox(self, event):
        win = Toplevel(takefocus=True)
        win.attributes("-topmost", True)
        win.grab_set()
        self.contents = Text(win)
        self.contents.pack(side = RIGHT, fill = BOTH, expand = True)


    def get_random_color(self):
        return "#{:02x}{:02x}{:02x}".format(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))

    def __init__(self, frame, note_type_input):
        #self.note_title_input = note_title_input
        self.note_type_input = note_type_input

        self.label = Label(frame, text=note_type_input, font=("Times New Roman", 14, "bold"), fg=self.get_random_color(), borderwidth=2, relief="groove")
        self.label.pack(padx=5, anchor="w")
        self.textbox = Text(frame, borderwidth=1, relief="solid", height=8) #T = Text(root, bg, fg, bd, height, width, font, ..) 
        self.textbox.configure(state="disabled")
        self.textbox.pack(fill=X, padx=(5, 5), pady=(0, 3)) #Order: (left, right) (up, down)
        self.textbox.bind("<Button-1>", self.popup_textbox)
      
class App:

    def popup(self, msg):
        messagebox.showinfo("", msg)

    def __init__(self):
        self.root = Tk()
        self.root.geometry("1200x800")

    def frames(self):
        self.frame = Frame(self.root, width=1200, height=30, bg="orange")
        self.frame.pack(fill=X)

        self.button()

        self.frame2 = Frame(self.root)
        self.frame2.pack(fill = BOTH, expand = True)  

        self.frame.pack_propagate(False)

    def create_note(self, note_type_input):
        note = Note(self.frame2, note_type_input)

    def add_note(self):
        # win = Toplevel(takefocus=True)
        # win.attributes("-topmost", True)
        # win.grab_set()

        # note_title_label = Label(win, text="Enter the note title")
        # note_type_label = Label(win, text="Enter the type of note")
        # note_title = StringVar()
        # note_type = StringVar()
        # note_title_label.pack()
        # note_title_input = Entry(win, textvariable=note_title)
        # note_title_input.pack()
        # note_type_input = Entry(win, textvariable=note_type)
        # note_type_label.pack()
        # note_type_input.pack()
        # submit_button = Button(win, text="Submit", command=lambda note_title_input=note_title_input, \
        #                        note_type_input=note_type_input: self.create_note(note_title_input, note_type_input))
        # submit_button.pack()
        self.create_note("Hello")

    def button(self):
        self.add_node_button = Button(self.frame, text = "Add Note", bg='orange',font=('Helvetica', 12), relief='flat', command=self.add_note)
        self.add_node_button.pack(side=TOP)

    def run(self):
        self.frames()
        self.root.mainloop()


app = App()
app.run()


