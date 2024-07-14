from tkinter import *
from tkinter import messagebox
from tkinter import font as tkFont
from tkinter import colorchooser
import PIL.Image
import PIL.ImageTk
import random
import pickle
from textwrap3 import wrap
from collections import OrderedDict

RADIUS = 50
OFFSET = 70
MAX_LETTERS_IN_LINE_ZI = 14
MAX_TOPIC_LENGTH = 59
MAX_LINES_ZI = 4

#Heuristic values
NUM_NODES_ON_SCREEN_HEURISTIC = 35
NUM_NODES_COL_HEURISTIC = 5
NUM_NODES_ROW_HEURISTIC = 7
HEURISTIC_1 = 17
HEURISTIC_2 = 20

HORIZONTAL_GAP = 185
VERTICAL_GAP = 115

DOWN_DIR = 0
LEFT_DIR = 1
RIGHT_DIR = 2
UP_DIR = 3


half_width = 500
half_height = 400

class Tree:

    def move(self, amount):
        if len(self.central_node.children) < 35:
            return
        self.central_node.sliding_window_start += amount
        self.redraw(self.canvas)


    def mouse_click(self, event, id):
        self.clicked = id
        self.canvas.after(300, self.mouse_action, event)


    def double_click(self, event):
        self.double_click_flag = True
        
    def mouse_action(self, event):
        if self.double_click_flag:
            self.double_click_flag = False
            self.invoke_notes(self.clicked)
        else:
            self.change_root(self.clicked)
    

    def return_to_main_menu(self):
        self.tree_window.destroy()
        NotesFrame.labels = OrderedDict()

    #Tree
    def serialization_dict(self):
        keys_to_pickle = {"root" : self.root.serialization_dict(),
                          "labels": NotesFrame.labels}
        return keys_to_pickle

    def save_tree(self):
        try:
            with open("saved_trees/{}.pickle".format(self.root.input_text), "wb") as outfile:
                pickle.dump(self.serialization_dict(), outfile)
            messagebox.showinfo("Successful file save",  "File saved successfully!") 
        except IOError:
            print("Something went wrong while saving the file.")


    def init_side_frame(self):
        self.frame = Frame(self.tree_window,bg='orange',width=200,height=800)
        self.frame.pack(side=LEFT)
        self.frame.columnconfigure(0, weight = 1)
        self.frame.rowconfigure(3, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.back_button = Button(self.frame, relief='flat', bg='orange', text='Back', \
                                  command=self.return_to_main_menu)
        self.back_button.grid(row=0, column=0, sticky="ew")
        helv36 = tkFont.Font(family='Helvetica', size=24)
        self.back_button['font'] = helv36

        self.save_button = Button(self.frame, relief='flat', bg='orange', text='Save Tree', height=1, \
                                  command=self.save_tree, pady=1)
        self.save_button.grid(row=1, column=0, sticky="ew")
        helv14 = tkFont.Font(family='Helvetica', size=14)   
        self.save_button['font'] = helv14         

        self.button_frame = Frame(self.frame, bg="orange")
        self.button_frame.grid(row=2, column=0)

        self.left_icon = PIL.ImageTk.PhotoImage(master = self.frame, image = PIL.Image.open('icons/leftarrow.png').resize((30,30)))
        self.right_icon = PIL.ImageTk.PhotoImage(master = self.frame, image = PIL.Image.open('icons/rightarrow.png').resize((30,30)))
        self.left_button = Button(self.button_frame, relief='flat', bg='orange', command=lambda: self.move(-5))
        self.right_button = Button(self.button_frame, relief='flat', bg='orange', command=lambda: self.move(5))
        self.left_button.config(image=self.left_icon)
        self.left_button.image = self.left_icon
        self.right_button.config(image=self.right_icon)
        self.right_button.image = self.right_icon
        self.left_button.grid(row = 0, column = 0)
        self.right_button.grid(row = 0, column = 1)


        self.depth_label = Label(self.frame, text = "Depth={}".format(self.central_node.depth), bg='orange',font=('Helvetica', 20))
        self.depth_label.grid(row = 3, column = 0, sticky="s")


        self.frame.grid_propagate(False)

    def submit_child(self):
        self.add_child_dialog.destroy()
        self.add_node(self.node_ref, self.child_name.get())

    def submit_child_batch(self):
        children_names = self.inputtxt.get("1.0",END)
        self.add_child_dialog.destroy()
        for child_name in children_names.split("\n"):
            if len(child_name) > 0:
                self.add_node(self.node_ref, child_name)

    def menu_add_child_node(self):
        self.node_ref = self.tkinter_nodes_to_ids[self.clicked]
        self.add_child_dialog = Toplevel(takefocus=True)
        self.add_child_dialog.attributes("-topmost", True)
        self.add_child_dialog.grab_set()
        self.add_child_dialog.bind('<Return>', lambda event: self.submit_child())

        self.child_name = StringVar()
        self.inputtxt = Entry(self.add_child_dialog, textvariable=self.child_name) 
        self.inputtxt.pack()    
        self.printButton = Button(self.add_child_dialog, text = "Submit", \
                            command = self.submit_child) 
        self.printButton.pack()
      

    def menu_batch_add_child_node(self):
        self.node_ref = self.tkinter_nodes_to_ids[self.clicked]
        self.add_child_dialog = Toplevel(takefocus=True)
        self.add_child_dialog.attributes("-topmost", True)
        self.add_child_dialog.grab_set()

        self.inputtxt = Text(self.add_child_dialog) 
        self.inputtxt.pack()    
        self.printButton = Button(self.add_child_dialog, text = "Submit", \
                            command = self.submit_child_batch) 
        self.printButton.pack()

    def menu_delete_node(self):
        node_ref = self.tkinter_nodes_to_ids[self.clicked]

        if node_ref is self.central_node:
            if node_ref is self.root:
                if not node_ref.children:         #Del root, no successor
                    self.return_to_main_menu()
                else:                             #Del root, sucessor
                    self.root = self.root.children[0] #Lose pointer #1
                    self.root.x = half_width
                    self.root.y = half_height
                    self.root.parent = None #Lose pointer #2
                    self.central_node = self.root
                    self.redraw()
            else:            
                parent = node_ref.parent         #Central, not root
                parent.children.remove(node_ref) #Lose pointer here
                self.central_node = parent
                self.redraw()
        else:                                    #Not central
            #A simple child node that is currently visible
            parent = node_ref.parent   
            parent.children.remove(node_ref)
            self.redraw()
            
    def menu_go_to_parent(self):
        node_ref = self.tkinter_nodes_to_ids[self.clicked]
        parent = node_ref.parent
        self.central_node = parent
        self.redraw()

    def menu_rename_node(self):
        node_ref = self.tkinter_nodes_to_ids[self.clicked]    
        self.rename_node_dialog = Toplevel(takefocus=True)
        self.rename_node_dialog.attributes("-topmost", True)
        self.rename_node_dialog.grab_set()
        self.rename_node_dialog.bind('<Return>', lambda event: self.postdialog_rename_node())

        self.new_node_name = StringVar()
        self.inputtxt = Entry( self.rename_node_dialog, textvariable=self.new_node_name) 
        self.inputtxt.pack()    
        self.printButton = Button(self.rename_node_dialog, text = "Submit", \
                            command = self.postdialog_rename_node) 
        self.printButton.pack()

    def postdialog_rename_node(self):
        node_ref = self.tkinter_nodes_to_ids[self.clicked]  
        self.new_node_name = self.inputtxt.get()
        self.rename_node_dialog.destroy()
        self.canvas.itemconfig(node_ref.text_id, text=self.new_node_name)
        node_ref.input_text = self.new_node_name
        # self.canvas.delete(node_ref.tkinter_id)
        # node_ref.draw_circle(self.new_node_name)
        
    def popup(self): 
        messagebox.showinfo("",  "ID of clicked widget: {}".format(self.clicked)) 

    def show_popup_menu(self, event, id):
        self.clicked = id
        try: 
            self.popup_menu.tk_popup(event.x_root, event.y_root) 
        finally: 
            self.popup_menu.grab_release() 


    def init_popup_menu(self):
        self.popup_menu = Menu(self.tree_window, tearoff = 0)

        self.popup_menu.add_command(label = "Add child node", command = self.menu_add_child_node)
        self.popup_menu.add_command(label = "Batch add child node", command = self.menu_batch_add_child_node)
        self.popup_menu.add_command(label = "Rename node", command = self.menu_rename_node)
        self.popup_menu.add_command(label = "Delete node", command = self.menu_delete_node)
        self.popup_menu.add_command(label = "Change style", command = self.popup)
        self.popup_menu.add_command(label = "Go to parent", command = self.menu_go_to_parent)

        self.double_click_flag = False

    def invoke_notes(self, tkinter_id):
        node_ref = self.tkinter_nodes_to_ids[tkinter_id]
        node_ref.open_notes_menu()
        
    def _reset_bookeeping_info(self):
        self.grid = [[0 for _ in range(5)] for __ in range(7)]
        self.tkinter_nodes_to_ids = {}
        self.node_queue = []

    def _register_node(self, node, input_text):
        #Draw it
        tkinter_id = node.draw_circle(input_text)
        #Map it
        self.tkinter_nodes_to_ids[tkinter_id] = node
        self.canvas.tag_bind(tkinter_id, '<Button-3>', lambda event, id = tkinter_id: self.show_popup_menu(event, id)) #This lambda is necessary
        self.canvas.tag_bind(tkinter_id, '<Button-1>', lambda event, id = tkinter_id: self.mouse_click(event, id))             
        self.canvas.tag_bind(tkinter_id, '<Double-Button-1>', lambda event: self.double_click(event))     
        self.canvas.tag_bind(node.text_id, '<Button-3>', lambda event, id = tkinter_id: self.show_popup_menu(event, id)) #This lambda is necessary
        self.canvas.tag_bind(node.text_id, '<Button-1>', lambda event, id = tkinter_id: self.mouse_click(event, id))             
        self.canvas.tag_bind(node.text_id, '<Double-Button-1>', lambda event: self.double_click(event))                       
        #Grid it
        self.grid[self._determine_row(node.y)][self._determine_col(node.x)] = 1

        #Queue it
        self.node_queue.append((node.x, node.y+VERTICAL_GAP, UP_DIR))
        self.node_queue.append((node.x-HORIZONTAL_GAP, node.y, RIGHT_DIR))
        self.node_queue.append((node.x+HORIZONTAL_GAP, node.y, LEFT_DIR))
        self.node_queue.append((node.x, node.y-VERTICAL_GAP, DOWN_DIR))

    #Tree
    @staticmethod
    def _construct_from_payload(payload):
        root_payload = payload["root"]
        tree = Tree()
        tree.root = Node(root_payload["input_text"], 0, None, tree.canvas, \
                    half_width, half_height)
        tree.central_node = tree.root
        
        for child_node_payload in root_payload["children"]:
            new_node = Node._construct_from_payload(child_node_payload, tree.root, tree.canvas)
            tree.root.add_child(new_node)

        tree.root.notes_frame = NotesFrame()
        for note_payload in root_payload["notes_frame"]["notes"]:
            cur_row = len(tree.root.notes_frame.notes)
            note = Note._construct_from_payload(note_payload, tree.root.notes_frame.main_frame, cur_row)
            note.note_preview.bind("<Button-1>", tree.root.notes_frame.mouse_click) #TODO: T_T This is ghastly.
            note.note_preview.bind("<Double-Button-1>", tree.root.notes_frame.double_click)
            tree.root.notes_frame.notes.append(note)

        NotesFrame.labels = payload["labels"]

        return tree

    #Tree
    def __init__(self, input_text=""): #Maybe more like canvas? And make it a member?
        self.tree_window = Tk()
        self.tree_window.geometry("1500x600")
        self.canvas = Canvas(self.tree_window, width = 1100 - 120, height = 800)
        self.canvas.pack(side = RIGHT, fill = BOTH, expand = True)  

        root = Node(input_text, 0, None, self.canvas, half_width, half_height)

        self.root = root
        self.central_node = root
        self.init_side_frame()
        self.init_popup_menu()

        self._reset_bookeeping_info()
        self._register_node(self.root, self.root.input_text)

        self.double_click_flag = False

    def run(self):
        self.tree_window.mainloop()



    def _determine_row(self, y):
        root_y = self.root.y
        deviations = 0
        delta = y - root_y
        return 7//2+delta//VERTICAL_GAP


    def _determine_col(self, x):
        root_x = self.root.x
        deviations = 0
        delta = x - root_x
        return 5//2+delta//HORIZONTAL_GAP

    def _print_grid(self):
        s = [[str(e) for e in row] for row in self.grid]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))
        print()

    def _no_collide(self, grid_x, grid_y):
        return self.grid[grid_y][grid_x] == 0  
    
    def change_root(self, tkinter_id):
        node_ref = self.tkinter_nodes_to_ids[tkinter_id]  
        self.central_node = node_ref
        self.central_node.x = half_width
        self.central_node.y = half_height        
        self.redraw()


    
    def add_existing_node(self, parent_node, new_node, do_add_child=True):
        if do_add_child:
            parent_node.add_child(new_node)

        if parent_node is self.central_node:
            '''
            Having it run at least once because: ?
            '''
            while True:
                if not self.node_queue: #Tree is locked
                    return
                
                new_node.x, new_node.y, source_dir = self.node_queue.pop(0)
                grid_x, grid_y = self._determine_col(new_node.x), self._determine_row(new_node.y)

                if not new_node._in_bounds(source_dir) or not self._no_collide(grid_x, grid_y):
                    continue #This one is bad, but we keep trying.

                self._register_node(new_node, new_node.input_text)
                break #Break if we found a coordinate. No need to keep pumping.

    '''
    Make new Node, add child no matter what.

    If parent_node is central node, we populate its
    x and y based on what we pop off the queue. We also
    have the notion of an equivalent "grid" x and y.

    Now that it has an x and a y: If it's in bounds:
        draw it, map it, grid it, queue it.
    '''
    def add_node(self, parent_node, input_text):
        new_node = Node(input_text, parent_node.depth+1, parent_node, self.canvas)
        self.add_existing_node(parent_node, new_node)


    def redraw(self):
        self.canvas.delete('all')

        #Constructor, except we already know root.
        self._reset_bookeeping_info()

        central_node = self.central_node
        self.depth_label.config(text = "Depth={}".format(self.central_node.depth))

        self._register_node(central_node, central_node.input_text)

        children = self.central_node.children
        num_children = len(children)
        sws = self.central_node.sliding_window_start
        for i in range(sws, min(sws+num_children, sws+35)):
            self.add_existing_node(self.central_node, children[i % num_children], False)
        self.canvas.update()

class Node:

    def open_notes_menu(self):
        self.notes_frame.show_self()

    '''
    Calculate if this node is even drawable
    '''
    def _in_bounds(self, source_dir):
        if source_dir == UP_DIR: #Bottom half doesn't need to account for gap
            return self.y+RADIUS <= 800 \
                and self.x-RADIUS-OFFSET >= 0 \
                and self.x+RADIUS+OFFSET <= 1000 \
                and self.y-RADIUS-VERTICAL_GAP >= 0 
        
        if source_dir == RIGHT_DIR: #Left half doesn't need to account for gap
            return self.y+RADIUS <= 800 \
                and self.x-RADIUS-OFFSET >= 0 \
                and self.x+RADIUS+HORIZONTAL_GAP+OFFSET <= 1000 \
                and self.y-RADIUS >= 0
        
        if source_dir == LEFT_DIR: #Right half doesn't need to account for gap
            return self.y+RADIUS <= 800 \
                and self.x-RADIUS-HORIZONTAL_GAP-OFFSET >= 0 \
                and self.x+RADIUS+OFFSET <= 1000 \
                and self.y-RADIUS >= 0
        
        if source_dir == DOWN_DIR: #Top half doesn't need to account for gap.
            return self.y+RADIUS+VERTICAL_GAP <= 800 \
                and self.x-RADIUS-OFFSET >= 0 \
                and self.x+RADIUS+OFFSET <= 1000 \
                and self.y-RADIUS >= 0
    '''
    Draw point in the center of the node as a visual aid if desired.
    '''
    def _draw_point(self, x, y):
        self.canvas_ref.create_oval(x-1, y-1, x+1, y+1)

    '''
    Insert newlines/ellipses elegantly.
    '''
    def _process_text(self, inputstr):
        linelength = 14
        reformatted = '\n'.join(wrap(inputstr, width=linelength, max_lines=4, placeholder="..."))
        return reformatted

    '''
    Actually draw the node based on x and y. Includs the text to go along with it.
    '''  
    def draw_circle(self, input_text):

        x0 = self.x-RADIUS
        y0 = self.y-RADIUS
        x1 = self.x+RADIUS
        y1 = self.y+RADIUS

        id = self.canvas_ref.create_oval(x0, y0, x1+OFFSET, y1, fill="white")
        self.tkinter_id = id

        input_text = self._process_text(input_text)
        self.text_id = self.canvas_ref.create_text(x1-15, y1-RADIUS, text=input_text, font=("Consolas", 12, "bold"), justify="center")
        #self._draw_point(x1-15, y1-RADIUS, self.canvas_ref)
        #self.canvas_ref.create_rectangle(x0+HEURISTIC_1, y0+HEURISTIC_2, x1+OFFSET-HEURISTIC_1, y1-HEURISTIC_2)
        return id

    '''
    Add child to this node.
    We do 
    '''
    def add_child(self, child):
        self.children.append(child)

    #Node
    def serialization_dict(self):
        keys_to_save = {
            "input_text" : self.input_text,
            "children" : [child.serialization_dict() for child in self.children],
            "depth" : self.depth,
            "notes_frame": self.notes_frame.serialization_dict() if self.notes_frame is not None else None
        }
        return keys_to_save
        

    #Node
    @staticmethod
    def _construct_from_payload(payload, parent, canvas_ref):
        node = Node(payload["input_text"], payload["depth"], parent, canvas_ref)

        for child_node_payload in payload["children"]:
            new_node = Node._construct_from_payload(child_node_payload, node, canvas_ref)
            node.children.append(new_node)

        node.notes_frame = NotesFrame()
        for note_payload in payload["notes_frame"]["notes"]:
            cur_row = len(node.notes_frame.notes)
            print(f"Cur row in side of Node._construct_from_payload: {cur_row}")
            note = Note._construct_from_payload(note_payload, node.notes_frame.main_frame, cur_row)
            node.notes_frame.notes.append(note)

        return node
    

    #Node
    def __init__(self, input_text, depth, parent, canvas_ref, x=-1, y=-1):
        self.x = x
        self.y = y
        self.parent = parent
        self.input_text = input_text
        self.children = []
        self.depth = depth
        self.tkinter_id = None
        self.sliding_window_start = 0
        self.notes_frame = NotesFrame()
        self.canvas_ref = canvas_ref


class NotesFrame:

    COLOR = 0
    REF_COUNT = 1

    labels = OrderedDict()

    def show_self(self):
        try:
            self.notes_menu.deiconify()
            self.notes_menu.grab_set()

            #set colors
            for note in self.notes:
                cur_note_type_input = note.note_type_input
                note.label.configure(fg=self.labels[cur_note_type_input][self.COLOR])
        finally:
            self.notes_menu.grab_release()

    def popup_color_chooser(self):
         self.chosen_color = colorchooser.askcolor(parent=self.add_note_dialog)[1]

    def add_note(self):
        self.add_note_dialog = Toplevel(takefocus=True)
        self.add_note_dialog.attributes("-topmost", True)
        self.add_note_dialog.grab_set()
        self.add_note_dialog.bind('<Return>', lambda event: self.create_note_postdialog())

        #Type of note
        self.note_type_label = Label(self.add_note_dialog, text="Enter the type of note")
        self.note_type = StringVar()
        note_type_input = Entry(self.add_note_dialog, textvariable=self.note_type)
        self.note_type_label.pack()
        note_type_input.pack()

        #Color picker
        self.color_pick_label = Label(self.add_note_dialog, text="Pick a color for this note type")
        color_pick_button = Button(self.add_note_dialog, text="Pick color", command=self.popup_color_chooser)
        self.chosen_color = "#800020" #Default color
        self.color_pick_label.pack()
        color_pick_button.pack()

        #Pick previous label
        self.color_pick_label = Label(self.add_note_dialog, text="Or pick a previously made note type")
        self.prevous_label_listbox = Listbox(self.add_note_dialog)
        i = 1
        for label in self.labels.keys():
            self.prevous_label_listbox.insert(i, label)
            i += 1
        self.color_pick_label.pack()
        self.prevous_label_listbox.pack()

        submit_button = Button(self.add_note_dialog, text="Submit", command=self.create_note_postdialog)
        submit_button.pack()

    def mouse_click(self, event):
        widget = event.widget
        widget.after(300, self.mouse_action, event)


    def double_click(self, event):
        self.double_click_flag = True
        
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
    
    def create_note_postdialog(self):
        #Are we using an old label colour or not?
        label = self.note_type.get()
        color = None
        if len(label) == 0: #Old label was chosen
            chosen_label_index = self.prevous_label_listbox.curselection()[0]
            label = self.prevous_label_listbox.get(chosen_label_index)
            color = self.labels[label][self.COLOR]
            self.labels[label][self.REF_COUNT] += 1
        elif label in self.labels:
            color = self.labels[label][self.COLOR] #Merge opportunity with code above
            self.labels[label][self.REF_COUNT] += 1           
        else:
            self.labels[label] = [self.chosen_color, 1]
            color = self.chosen_color
        cur_row = len(self.notes)
        new_note = Note(self.main_frame, label, color, cur_row)       
        self.notes.append(new_note)
        self.add_note_dialog.destroy()

    def on_close(self):
        self.notes_menu.withdraw()
        if self.note_selected:
            self.note_selected.selected = False
            self.note_selected.configure(background=self.note_selected.color)
            self.note_selected = None

    def redraw(self):
        self.change_note_type_color_dialog.destroy()
        self.show_self()

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

    def postdialog_change_note_type_color(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        note_type_input = w.get(index)        
        chosen_color = colorchooser.askcolor(parent=self.change_note_type_color_dialog)[1]

        if chosen_color is None:
            return
        else:
            self.labels[note_type_input][self.COLOR] = chosen_color
    

        

    #NotesFrame
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
        self.clicked = None
        self.double_click_flag = False

    def swap_labels(self, to_widget):
        from_widget = self.note_selected
        from_widget_row = from_widget.grid_info()["row"]
        to_widget_row = to_widget.grid_info()["row"]

        temp = self.notes[from_widget_row>>1]
        self.notes[from_widget_row>>1] = self.notes[to_widget_row>>1]
        self.notes[to_widget_row>>1] = temp

        from_widget.grid(row=to_widget_row, column=0, sticky=EW, padx=(5, 5), pady=(0, 3))
        to_widget.grid(row=from_widget_row, column=0, sticky=EW, padx=(5, 5), pady=(0, 3))
        from_widget.selected = False
        self.note_selected = None
        from_widget.configure(background=from_widget.color)

    def highlight(self, event): #A diagram would be great for this
        widget = event.widget
        cur_selected = self.note_selected

        if not widget.selected and not cur_selected:
            if cur_selected is not None:
                cur_selected.selected = False 
                cur_selected.configure(background=cur_selected.color)

            widget.selected = True
            self.note_selected = widget
            widget.configure(background="#ECEC18")

        elif widget is cur_selected:

            widget.selected = False
            self.note_selected = None
            widget.configure(background=widget.color)

        else:
            self.swap_labels(widget)

    def menu_delete_note(self):
        selected_note = self.selected_note
        selected_note.note_preview.grid_remove()
        selected_note.label.grid_remove()
        selected_note.note_preview.destroy()
        selected_note.label.destroy()
        self.notes.remove(selected_note)

        self.labels[selected_note.note_type_input][self.REF_COUNT] -= 1

        if self.labels[selected_note.note_type_input][self.REF_COUNT] == 0:
            del self.labels[selected_note.note_type_input]

    #NotesFrame
    def serialization_dict(self):
        keys_to_save = {
            "notes" : [note.serialization_dict() for note in self.notes]
        }
        return keys_to_save

class Note:

    #Note
    @staticmethod
    def _construct_from_payload(note_payload, frame_ref, cur_row):
        note = Note(frame_ref, note_payload["note_type_input"], note_payload["color"], cur_row)
        note.contents = note_payload["contents"]
        note.note_preview.configure(state="normal") #new
        note.note_preview.delete("1.0", END)
        note.note_preview.insert("1.0", note.contents)
        note.note_preview.configure(state="disabled")
        return note
    
    #Note
    def serialization_dict(self):
        keys_to_save = {
            "note_type_input" : self.note_type_input,
            "contents" : self.contents,
            "color": self.color
        }
        return keys_to_save

    def save_text(self):
        self.contents = self.textbox_popup.get("1.0",'end-1c')
        self.note_preview.configure(state="normal") #new
        self.note_preview.delete("1.0", END)
        self.note_preview.insert("1.0", self.contents)
        self.note_preview.configure(state="disabled")
        self.win.destroy()


    def popup_textbox(self, event):
        self.win = Toplevel(takefocus=True)
        self.win.attributes("-topmost", True)
        self.win.grab_set()
        self.textbox_popup = Text(self.win) 
        self.textbox_popup.delete("1.0", END)
        self.textbox_popup.insert( "1.0", self.contents)
        self.textbox_popup.pack(side = RIGHT, fill = BOTH, expand = True)
        self.win.protocol("WM_DELETE_WINDOW", self.save_text)


    def get_random_color(self):
        return "#{:02x}{:02x}{:02x}".format(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))

    def init_popup_menu(self):
        self.popup_menu = Menu(self.frame_ref, tearoff = 0)
        self.popup_menu.add_command(label = "Delete note", command = self.frame_ref.notes_frame_ref.menu_delete_note)

    def show_popup_menu(self, event):
        widget = event.widget
        self.frame_ref.notes_frame_ref.selected_note = widget.note_ref
        try: 
            self.popup_menu.tk_popup(event.x_root, event.y_root) 
        finally: 
            self.popup_menu.grab_release() 

    #Note
    def __init__(self, frame_ref, note_type_input, color, cur_row):
        self.note_type_input = note_type_input
        self.frame_ref = frame_ref
        self.contents = ""
        self.color = color

        self.label = Label(self.frame_ref, text=self.note_type_input, font=("Times New Roman", 14, "bold"), fg=color, borderwidth=2, relief="groove")
        self.label.grid(row=cur_row*2, column = 0, sticky=NW, padx=5) #NW, other is N+E+W


        self.note_preview = Text(self.frame_ref, borderwidth=1, relief="solid", height=8) #T = Text(root, bg, fg, bd, height, width, font, ..) 
        self.note_preview.configure(state="disabled")
        self.note_preview.grid(row=cur_row*2+1, column=0, sticky=N+E+W, padx=(5, 5), pady=(0, 3)) #TODO
        self.note_preview.selected = False
        self.note_preview.color = "white"
        self.note_preview.note_ref = self
        self.note_preview.bind("<Button-1>", self.frame_ref.notes_frame_ref.mouse_click)
        self.note_preview.bind("<Double-Button-1>", self.frame_ref.notes_frame_ref.double_click)
        self.note_preview.bind("<Button-3>", self.show_popup_menu)
        self.init_popup_menu()
