import functools

from collections import OrderedDict
from tkinter import *
from tkinter import colorchooser


def no_event(func):
    @functools.wraps(func)
    def wrapper(self, *args):
        return func(self)
    return wrapper

class NotesFrame:

    #GOOD
    COLOR = 0
    REF_COUNT = 1
    HIGHLIGHT_COLOR = "#ECEC18"

    #GOOD
    labels = OrderedDict()

    #GOOD
    def show_self(self):
        try:
            self.notes_menu.deiconify()
            self.notes_menu.grab_set()

            #set colors
            # for note in self.notes:
            #     cur_note_type_input = note.note_type_input
            #     note.label.configure(fg=self.labels[cur_note_type_input][self.COLOR])
        finally:
            self.notes_menu.grab_release()

    #GOOD
    def popup_color_chooser(self):
         self.chosen_color = colorchooser.askcolor(parent=self.add_note_dialog)[1]

    #GOOD
    def add_note(self):
        self.add_note_dialog = Toplevel(takefocus=True)
        self.add_note_dialog.attributes("-topmost", True)
        self.add_note_dialog.grab_set()
        self.add_note_dialog.bind('<Return>', self.create_note_postdialog)

        #Type of note
        self.note_type_label = Label(self.add_note_dialog, text="Enter the type of note")
        self.note_type_input = Entry(self.add_note_dialog)
        self.note_type_label.pack()
        self.note_type_input.pack()

        #Color picker
        self.color_pick_label = Label(self.add_note_dialog, text="Pick a color for this note type")
        color_pick_button = Button(self.add_note_dialog, text="Pick color", command=self.popup_color_chooser)
        self.chosen_color = "#800020" #Default color
        self.color_pick_label.pack()
        color_pick_button.pack()

        #Pick previous label
        self.color_pick_label = Label(self.add_note_dialog, text="Or pick a previously made note type")
        self.prevous_label_listbox = Listbox(self.add_note_dialog)

        idx = 1
        for label in self.labels.keys():
            self.prevous_label_listbox.insert(idx, label)
            idx += 1

        self.color_pick_label.pack()
        self.prevous_label_listbox.pack()

        submit_button = Button(self.add_note_dialog, text="Submit", command=self.create_note_postdialog)
        submit_button.pack()

    #TODO
    #GOOD
    def mouse_click(self, event):
        widget = event.widget
        widget.after(300, self.mouse_action, event)

    #TODO
    #GOOD
    @no_event
    def double_click(self):
        self.double_click_flag = True
    
    #GOOD
    def mouse_action(self, event):
        widget = event.widget
        if self.double_click_flag:
            self.double_click_flag = False
            self.highlight(event)
        else:
            if not self.note_selected:
                widget.note_ref.popup_textbox(event)
            else:
                self.highlight(event)   


    def increment_ref_count(self, label):
        self.labels[label][self.REF_COUNT] += 1
    #GOOD
    def create_note_postdialog(self):
        #Are we using an old label colour or not?
        label = self.note_type_input.get()
        color = None

        label_chosen_from_list = len(label) == 0
        typed_label_exists = label in self.labels
        existing_label_chosen = label_chosen_from_list or typed_label_exists

        if existing_label_chosen: #Old label was chosen

            if label_chosen_from_list:
                chosen_label_index = self.prevous_label_listbox.curselection()[0]
                label = self.prevous_label_listbox.get(chosen_label_index)
            elif typed_label_exists:
                color = self.labels[label][self.COLOR]
                self.increment_ref_count(label)
        else:
            self.labels[label] = [self.chosen_color, 1]
            color = self.chosen_color
    
        cur_row = len(self.notes)
        new_note = Note(self.main_frame, label, color, cur_row)
        self.notes.append(new_note)
        self.add_note_dialog.destroy()

    #GOOD
    def on_close(self):
        self.notes_menu.withdraw()
        if self.note_selected:
            self.note_selected.selected = False
            self.note_selected.configure(background=self.note_selected.color)
            self.note_selected = None

    #GOOD
    def redraw(self):
        self.change_note_type_color_dialog.destroy()
        self.show_self()

    #GOOD
    def dialog_change_note_type_color(self):
        self.change_note_type_color_dialog = Toplevel(takefocus=True)
        self.change_note_type_color_dialog.attributes("-topmost", True)
        self.change_note_type_color_dialog.grab_set()
    
        self.prevous_label_listbox = Listbox(self.change_note_type_color_dialog)

        i = 1
        for label in self.labels.keys():
            self.prevous_label_listbox.insert(i, label)
            i += 1

        self.prevous_label_listbox.pack()
        self.prevous_label_listbox.bind('<<ListboxSelect>>', self.postdialog_change_note_type_color)
        self.change_note_type_color_dialog.protocol("WM_DELETE_WINDOW", self.redraw)

    #GOOD
    def configure_label_colors(self, changed_note_type_input, chosen_color):
        for note in self.notes:
            if note.note_type_input == changed_note_type_input:
                note.label.configure(fg=chosen_color)

    #GOOD
    def postdialog_change_note_type_color(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        changed_note_type_input = w.get(index)        
        chosen_color = colorchooser.askcolor(parent=self.change_note_type_color_dialog)[1]

        if chosen_color:
            self.configure_label_colors(changed_note_type_input, chosen_color)
            self.labels[changed_note_type_input][self.COLOR] = chosen_color

    #NotesFrame
    #TODO
    def __init__(self):

        self.notes_menu = Toplevel()
        self.notes_menu.attributes("-topmost", True)
        self.notes_menu.geometry("1200x800")
        self.notes_menu.rowconfigure(1, weight=1)
        self.notes_menu.columnconfigure(0, weight=1)
    
        self.top_frame = Frame(self.notes_menu, width=1200, height=30, bg="orange")
        self.top_frame.grid(row=0, column=0, sticky=EW)
        self.top_frame.columnconfigure(0, weight=1)

        self.add_node_button = Button(self.top_frame, text = "Add Note", bg='orange',font=('Helvetica', 12), \
                                      relief='flat', command = self.add_note)
        self.add_node_button.grid(row=0, column=0)
    
        self.change_note_type_color_button = Button(self.top_frame, text = "Change note type color", bg='orange',font=('Helvetica', 12), \
                                      relief='flat', command = self.dialog_change_note_type_color)
        self.change_note_type_color_button.grid(row=0, column=1)

        self.main_frame = Frame(self.notes_menu)
        self.main_frame.grid(row=1, column=0, sticky=NSEW) 
        self.main_frame.notes_frame_ref = self

        self.notes = []

        self.notes_menu.withdraw()
        self.notes_menu.protocol("WM_DELETE_WINDOW", lambda: self.on_close())

        self.note_selected = None
        self.clicked_id = None
        self.double_click_flag = False


    def swap_order_of_notes(self, index1, index2):
        half_index_1 = index1>>1
        half_index_2 = index2>>1

        temp = self.notes[half_index_1]
        self.notes[half_index_1] = self.notes[half_index_2]
        self.notes[half_index_2] = temp       

    #GOOD
    def swap_labels(self, to_widget):
        from_widget = self.note_selected

        from_widget_row_text = from_widget.grid_info()["row"]
        from_widget_row_label = from_widget_row_text - 1

        to_widget_row_text = to_widget.grid_info()["row"]
        to_widget_row_label = to_widget_row_text - 1

        self.swap_order_of_notes(from_widget_row_text, to_widget_row_text)

        from_widget.grid(row=to_widget_row_text, column=0, sticky=EW, padx=(5, 5), pady=(0, 3))
        to_widget.grid(row=from_widget_row_text, column=0, sticky=EW, padx=(5, 5), pady=(0, 3))

        from_widget.associated_label.grid(row=to_widget_row_label, column=0, sticky=NW, padx=5)
        to_widget.associated_label.grid(row=from_widget_row_label, column=0, sticky=NW, padx=5)

        from_widget.selected = False
        self.note_selected = None
        from_widget.configure(background=from_widget.color)

    #GOOD
    def highlight(self, event): #A diagram would be great for this
        widget = event.widget

        no_note_currently_selected = not self.note_selected
        selected_note_reclicked = widget is self.note_selected

        if no_note_currently_selected:
            widget.selected = True
            self.note_selected = widget
            widget.configure(background=self.HIGHLIGHT_COLOR)

        elif selected_note_reclicked:
            widget.selected = False
            self.note_selected = None
            widget.configure(background=widget.color)

        else:
            self.swap_labels(widget)

    def decrement_ref_count(self, selected_note):
        self.labels[selected_note.note_type_input][self.REF_COUNT] -= 1

        if self.labels[selected_note.note_type_input][self.REF_COUNT] == 0:
            del self.labels[selected_note.note_type_input]


    #GOOD
    def menu_delete_note(self):
        selected_note = self.selected_note

        selected_note.note_preview.grid_remove()
        selected_note.label.grid_remove()

        selected_note.note_preview.destroy()
        selected_note.label.destroy()

        self.notes.remove(selected_note)

        self.decrement_ref_count(selected_note)

    #NotesFrame
    #TODO
    def serialization_dict(self):
        keys_to_save = {
            "notes" : [note.serialization_dict() for note in self.notes]
        }
        return keys_to_save

class Note:



    #Note
    @staticmethod
    #TODO
    def _construct_from_payload(note_payload, frame_ref, cur_row):
        note = Note(frame_ref, note_payload["note_type_input"], note_payload["color"], cur_row)
        note.contents = note_payload["contents"]

        note.populate_note_preview()

        return note
    
    #Note
    #TODO
    def serialization_dict(self):
        keys_to_save = {
            "note_type_input" : self.note_type_input,
            "contents" : self.contents,
            "color": self.color
        }
        return keys_to_save
    
    def populate_note_preview(self):
        self.note_preview.configure(state="normal") #new
        self.note_preview.delete("1.0", END)
        self.note_preview.insert("1.0", self.contents)
        self.note_preview.configure(state="disabled")        

    #GOOD
    def save_text(self):
        self.contents = self.textbox_popup.get("1.0",'end-1c')
        self.populate_note_preview()
        self.win.destroy()

    #GOOD
    def popup_textbox(self, event):
        self.win = Toplevel(takefocus=True)
        self.win.attributes("-topmost", True)
        self.win.grab_set()

        self.textbox_popup = Text(self.win) 
        self.textbox_popup.delete("1.0", END)
        self.textbox_popup.insert( "1.0", self.contents)
        self.textbox_popup.pack(side = RIGHT, fill = BOTH, expand = True)

        self.win.protocol("WM_DELETE_WINDOW", self.save_text)

    #GOOD
    def init_popup_menu(self):
        self.popup_menu = Menu(self.frame_ref, tearoff = 0)
        self.popup_menu.add_command(label = "Delete note", command = self.frame_ref.notes_frame_ref.menu_delete_note)

    #GOOD
    def show_popup_menu(self, event):
        widget = event.widget
        self.frame_ref.notes_frame_ref.selected_note = widget.note_ref
        try: 
            self.popup_menu.tk_popup(event.x_root, event.y_root) 
        finally: 
            self.popup_menu.grab_release() 

    #Note
    #TODO
    def __init__(self, frame_ref, note_type_input, color, cur_row):
        self.note_type_input = note_type_input
        self.frame_ref = frame_ref
        self.contents = ""
        self.color = color

        self.label = Label(self.frame_ref, text=self.note_type_input, font=("Times New Roman", 14, "bold"), fg=color, borderwidth=2, relief="groove")
        self.label.note_ref = self
        self.label.grid(row=cur_row*2, column = 0, sticky=NW, padx=5) #NW, other is N+E+W


        self.note_preview = Text(self.frame_ref, borderwidth=1, relief="solid", height=8) #T = Text(root, bg, fg, bd, height, width, font, ..) 
        self.note_preview.associated_label = self.label
        self.note_preview.configure(state="disabled")
        self.note_preview.grid(row=cur_row*2+1, column=0, sticky=N+E+W, padx=(5, 5), pady=(0, 3)) #TODO
        self.note_preview.selected = False
        self.note_preview.color = "white"
        self.note_preview.note_ref = self
        self.note_preview.bind("<Button-1>", self.frame_ref.notes_frame_ref.mouse_click)
        self.note_preview.bind("<Double-Button-1>", self.frame_ref.notes_frame_ref.double_click)
        self.note_preview.bind("<Button-3>", self.show_popup_menu)
        self.init_popup_menu()
