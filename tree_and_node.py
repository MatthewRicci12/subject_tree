import PIL.Image
import PIL.ImageTk
import pickle
import functools

from tkinter import *
from tkinter import messagebox
from tkinter import font as tkFont
from textwrap3 import wrap
from notesframe_and_note import *

#Heuristic values
NUM_NODES_ON_SCREEN_HEURISTIC = 35
NUM_NODES_COL_HEURISTIC = 5
NUM_NODES_ROW_HEURISTIC = 7

#HEURISTIC_1 = 17
#HEURISTIC_2 = 20
TEXT_OFFSET = 15

RADIUS = 50
RADIUS_OFFSET = 70

MAX_LETTERS_IN_LINE_ZI = 14
MAX_TOPIC_LENGTH = 59
MAX_LINES_ZI = 4

HORIZONTAL_GAP = 185
VERTICAL_GAP = 115

DOWN_DIR = 0
LEFT_DIR = 1
RIGHT_DIR = 2
UP_DIR = 3

MAX_NODES_ON_SCREEN = 35
MAX_NUM_CHILDREN_ROW = 7
MAX_NUM_CHILDREN_COL = 5

TREE_WINDOW_WIDTH = 1000
TREE_WINDOW_HEIGHT = 600

LINE_LENGTH = 14
MAX_LINES = 4

HALF_WIDTH = 500
HALF_HEIGHT = 300 


def no_event(func):
    @functools.wraps(func)
    def wrapper(self, *args):
        return func(self)
    return wrapper

class Tree:

    #Tree:Dialog functions
    #GOOD
    def dialog_menu_add_child_node(self):
        self.selected_node = self.tkinter_ids_to_nodes[self.clicked_id]
        self.add_child_dialog = Toplevel(takefocus=True)
        self.add_child_dialog.attributes("-topmost", True)
        self.add_child_dialog.grab_set()
        self.add_child_dialog.bind('<Return>', self.postdialog_submit_child)

        self.submitted_child_name_stringvar = StringVar()
        self.inputtxt = Entry(self.add_child_dialog, textvariable=self.submitted_child_name_stringvar) 
        self.inputtxt.pack()    
        self.printButton = Button(self.add_child_dialog, text = "Submit", \
                            command = self.postdialog_submit_child) 
        self.printButton.pack()

    #GOOD
    def dialog_menu_batch_add_child_node(self):
        self.selected_node = self.tkinter_ids_to_nodes[self.clicked_id]
        self.add_child_dialog = Toplevel(takefocus=True)
        self.add_child_dialog.attributes("-topmost", True)
        self.add_child_dialog.grab_set()

        self.inputtxt = Text(self.add_child_dialog) 
        self.inputtxt.pack()    
        self.printButton = Button(self.add_child_dialog, text = "Submit", \
                            command = self.postdialog_submit_child_batch) 
        self.printButton.pack()

    #GOOD
    def dialog_menu_rename_node(self): 
        self.rename_node_dialog = Toplevel(takefocus=True)
        self.rename_node_dialog.attributes("-topmost", True)
        self.rename_node_dialog.grab_set()
        self.rename_node_dialog.bind('<Return>', self.postdialog_rename_node)

        self.inputtxt = Entry(self.rename_node_dialog) 
        self.inputtxt.pack()    
        self.printButton = Button(self.rename_node_dialog, text = "Submit", \
                            command = self.postdialog_rename_node) 
        self.printButton.pack()

    #Tree:Postdialog functions
    #GOOD
    @no_event
    def postdialog_submit_child(self):
        self.add_child_dialog.destroy()
        submitted_child_name = self.submitted_child_name_stringvar.get()

        self.add_node(self.selected_node, submitted_child_name)


    #GOOD
    @no_event
    def postdialog_submit_child_batch(self):
        children_names = self.inputtxt.get("1.0",END).split("\n")
        self.add_child_dialog.destroy()

        for child_name in children_names:
            if len(child_name) > 0:
                self.add_node(self.selected_node, child_name)

    #GOOD
    @no_event
    def postdialog_rename_node(self):
        new_node_name = self.inputtxt.get()
        self.rename_node_dialog.destroy()

        selected_node = self.tkinter_ids_to_nodes[self.clicked_id]  
        self.canvas.itemconfig(selected_node.text_id, text=new_node_name)
        selected_node.input_text = new_node_name
    
    #GOOD
    #TODO: Although, is there anything I can do about this nesting?
    def menu_delete_node(self):
        selected_node = self.tkinter_ids_to_nodes[self.clicked_id]

        is_root = selected_node is self.root
        has_children = selected_node.children
        is_central_node = selected_node is self.central_node

        nonroot_central_node_deleted = is_central_node and not is_root
        root_deleted_with_successor = is_root and has_children
        root_deleted_no_successor = is_root and not has_children
        visible_child_node_deleted = not is_central_node

        if root_deleted_no_successor:
            self.return_to_main_menu()  
            return   

        elif root_deleted_with_successor:
            first_child = self.root.children[0]
            self.change_root(first_child)
            return
            
        elif nonroot_central_node_deleted:
            self.central_node = selected_node.parent
            selected_node.parent.children.remove(selected_node)
            self.redraw()      

        elif visible_child_node_deleted:
            selected_node.parent.children.remove(selected_node)
            self.redraw()            

    #GOOD
    def menu_go_to_parent(self):
        selected_node = self.tkinter_ids_to_nodes[self.clicked_id]
        self.central_node = selected_node.parent
        self.redraw()

    #Tree:Window-building functions
    #GOOD
    def init_popup_menu(self):
        self.popup_menu = Menu(self.tree_window, tearoff = 0)

        self.popup_menu.add_command(label = "Add child node", command = self.dialog_menu_add_child_node)
        self.popup_menu.add_command(label = "Batch add child node", command = self.dialog_menu_batch_add_child_node)
        self.popup_menu.add_command(label = "Rename node", command = self.dialog_menu_rename_node)
        self.popup_menu.add_command(label = "Delete node", command = self.menu_delete_node)
        self.popup_menu.add_command(label = "Go to parent", command = self.menu_go_to_parent)

        self.double_click_flag = False        

    #GOOD
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


    #Tree:Top-level functions
    #GOOD
    def change_root(self, new_root):
        self.root = new_root
        self.root.x = HALF_WIDTH
        self.root.y = HALF_HEIGHT
        self.root.parent = None 
        self.central_node = self.root
        self.redraw()    

    #GOOD
    def move(self, amount):
        if len(self.central_node.children) < MAX_NODES_ON_SCREEN:
            return
        self.central_node.sliding_window_start += amount
        self.redraw()

    #GOOD
    def mouse_click(self, event):
        self.clicked_id = event.widget.find_closest(event.x, event.y)[0]
        self.canvas.after(300, self.mouse_action, event)

    #GOOD
    @no_event
    def double_click(self):
        self.double_click_flag = True

    #GOOD
    @no_event        
    def mouse_action(self):
        if self.double_click_flag:
            self.double_click_flag = False
            self.invoke_notes(self.clicked_id)
        else:
            self.change_central_node(self.clicked_id)
    
    #TODO: Any more elegant way to do this? It's tough.
    def return_to_main_menu(self):
        NotesFrame.labels = OrderedDict()
        self.tree_window.destroy()

    #GOOD
    def save_tree(self):
        try:
            with open("saved_trees/{}.pickle".format(self.root.input_text), "wb") as outfile:
                pickle.dump(self.serialization_dict(), outfile)
            messagebox.showinfo("Successful file save",  "File saved successfully!") 
        except IOError:
            print("Something went wrong while saving the file.")


    # def popup(self): 
    #     messagebox.showinfo("",  "ID of clicked widget: {}".format(self.clicked_id)) 

    #GOOD
    def show_popup_menu(self, event):
        self.clicked_id = event.widget.find_closest(event.x, event.y)[0]
        try: 
            self.popup_menu.tk_popup(event.x_root, event.y_root) 
        finally: 
            self.popup_menu.grab_release() 

    #GOOD
    def invoke_notes(self, tkinter_id):
        selected_node = self.tkinter_ids_to_nodes[tkinter_id]
        selected_node.open_notes_menu()
        
    #GOOD
    def reset_bookkeeping_info(self):
        self.grid = [[0 for _ in range(5)] for __ in range(7)]
        self.tkinter_ids_to_nodes = {}
        self.node_queue = []

    #GOOD
    #Note: Map is needed cause you can't monkeypatch an int.
    #TODO: If you can think of anything though...
    def register_node(self, node, input_text):
        #Draw it
        node.draw_self(input_text)

        #Map it
        self.tkinter_ids_to_nodes[node.tkinter_id] = node
        self.canvas.tag_bind(node.tkinter_id, '<Button-3>', self.show_popup_menu)
        self.canvas.tag_bind(node.tkinter_id, '<Button-1>', self.mouse_click)             
        self.canvas.tag_bind(node.tkinter_id, '<Double-Button-1>', self.double_click)     
        self.canvas.tag_bind(node.text_id, '<Button-3>', self.show_popup_menu) 
        self.canvas.tag_bind(node.text_id, '<Button-1>', self.mouse_click)             
        self.canvas.tag_bind(node.text_id, '<Double-Button-1>', self.double_click)   

        #Grid it
        node_row = self.determine_row(node.y)
        node_col = self.determine_col(node.x)
        self.grid[node_row][node_col] = 1

        #Queue it
        self.node_queue.append((node.x, node.y+VERTICAL_GAP, UP_DIR))
        self.node_queue.append((node.x-HORIZONTAL_GAP, node.y, RIGHT_DIR))
        self.node_queue.append((node.x+HORIZONTAL_GAP, node.y, LEFT_DIR))
        self.node_queue.append((node.x, node.y-VERTICAL_GAP, DOWN_DIR))

    #GOOD
    def determine_row(self, y):
        diff = y - self.root.y
        return MAX_NUM_CHILDREN_ROW//2+diff//VERTICAL_GAP

    #GOOD
    def determine_col(self, x):
        diff = x - self.root.x
        return MAX_NUM_CHILDREN_COL//2+diff//HORIZONTAL_GAP

    # def print_grid(self):
    #     s = [[str(e) for e in row] for row in self.grid]
    #     lens = [max(map(len, col)) for col in zip(*s)]
    #     fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    #     table = [fmt.format(*row) for row in s]
    #     print('\n'.join(table))
    #     print()

    #GOOD
    def no_collide(self, grid_x, grid_y):
        return self.grid[grid_y][grid_x] == 0  
    
    #GOOD
    def change_central_node(self, tkinter_id):
        selected_node = self.tkinter_ids_to_nodes[tkinter_id]  
        self.central_node = selected_node
        self.central_node.x = HALF_WIDTH
        self.central_node.y = HALF_HEIGHT        
        self.redraw()

    #GOOD
    def find_coordinate_for_node(self, parent_node, new_node):
        if parent_node is self.central_node:
            while True:
                if not self.node_queue: #Tree is locked
                    return
                
                new_node.x, new_node.y, source_dir = self.node_queue.pop(0)
                grid_x, grid_y = self.determine_col(new_node.x), self.determine_row(new_node.y)

                if not new_node._in_bounds(source_dir) or not self.no_collide(grid_x, grid_y):
                    continue #This one is bad, but we keep trying.

                self.register_node(new_node, new_node.input_text)
                break #Break if we found a coordinate. No need to keep pumping.

    #GOOD
    def add_node(self, parent_node, input_text):
        new_node = Node(input_text, parent_node.depth+1, parent_node, self.canvas)
        parent_node.add_child(new_node)
        self.find_coordinate_for_node(parent_node, new_node)

    #TODO
    def redraw(self):
        self.canvas.delete('all')

        #Constructor, except we already know root.
        #before I had: central_node = self.central_node
        self.reset_bookkeeping_info()
        self.register_node(self.central_node, self.central_node.input_text)
        self.depth_label.config(text = "Depth={}".format(self.central_node.depth))

        children = self.central_node.children
        num_children = len(children)
        sws = self.central_node.sliding_window_start

        #TODO: Why this range? Consider replacing the stuff in min with variables.
        #IT would be good to explain this loop with a comment.
        #We start wherever the sliding window is. If it has more children than
        #max nodes, the 2nd item in min() will pass, thus limiting it.
        for i in range(sws, min(sws+num_children, sws+MAX_NODES_ON_SCREEN)):
            self.find_coordinate_for_node(self.central_node, children[i % num_children])

        self.canvas.update()


    #Tree:payload constructor
    #TODO: Fix how NotesFrame/Notes gets intiialized
    @staticmethod
    def _construct_from_payload(payload):
        root_payload = payload["root"]
        tree = Tree()
        tree.root = Node(root_payload["input_text"], 0, None, tree.canvas, \
                    HALF_WIDTH, HALF_HEIGHT)
        tree.central_node = tree.root
        tree.root.notes_frame = NotesFrame()
        
        for child_node_payload in root_payload["children"]:
            new_node = Node._construct_from_payload(child_node_payload, tree.root, tree.canvas)
            tree.root.add_child(new_node)


        for note_payload in root_payload["notes_frame"]["notes"]:
            cur_row = len(tree.root.notes_frame.notes)
            note = Note._construct_from_payload(note_payload, tree.root.notes_frame.main_frame, cur_row)
            note.note_preview.bind("<Button-1>", tree.root.notes_frame.mouse_click)
            note.note_preview.bind("<Double-Button-1>", tree.root.notes_frame.double_click)
            tree.root.notes_frame.notes.append(note)

        NotesFrame.labels = payload["labels"]

        return tree

    #Tree:serialization_dict
    #GOOD
    def serialization_dict(self):
        keys_to_pickle = {"root" : self.root.serialization_dict(),
                          "labels": NotesFrame.labels}
        return keys_to_pickle
    
    #GOOD
    def run(self):
        self.tree_window.mainloop()
    
    #Tree:init
    #GOOD
    def __init__(self, input_text=""): #Maybe more like canvas? And make it a member?
        self.tree_window = Tk()
        self.tree_window.geometry(f"{TREE_WINDOW_WIDTH}x{TREE_WINDOW_HEIGHT}")
        self.canvas = Canvas(self.tree_window)
        self.canvas.pack(side = RIGHT, fill = BOTH, expand = True)  
        root = Node(input_text, 0, None, self.canvas, HALF_WIDTH, HALF_HEIGHT)
        self.root = root
        self.central_node = root

        self.init_side_frame()
        self.init_popup_menu()

        self.reset_bookkeeping_info()
        self.register_node(self.root, self.root.input_text)

        self.double_click_flag = False


class Node:

    #GOOD
    def open_notes_menu(self):
        self.notes_frame.show_self()

    '''
    Calculate if this node is even drawable
    '''
    #GOOD #TODO ALtho if you CAN make it any nicer...
    def _in_bounds(self, source_dir):
        if source_dir == UP_DIR: #Bottom half doesn't need to account for gap
            return self.y+RADIUS <= TREE_WINDOW_HEIGHT \
                and self.x-RADIUS-RADIUS_OFFSET >= 0 \
                and self.x+RADIUS+RADIUS_OFFSET <= TREE_WINDOW_WIDTH \
                and self.y-RADIUS-VERTICAL_GAP >= 0 
        
        if source_dir == RIGHT_DIR: #Left half doesn't need to account for gap
            return self.y+RADIUS <= TREE_WINDOW_HEIGHT \
                and self.x-RADIUS-RADIUS_OFFSET >= 0 \
                and self.x+RADIUS+HORIZONTAL_GAP+RADIUS_OFFSET <= TREE_WINDOW_WIDTH \
                and self.y-RADIUS >= 0
        
        if source_dir == LEFT_DIR: #Right half doesn't need to account for gap
            return self.y+RADIUS <= TREE_WINDOW_HEIGHT \
                and self.x-RADIUS-HORIZONTAL_GAP-RADIUS_OFFSET >= 0 \
                and self.x+RADIUS+RADIUS_OFFSET <= TREE_WINDOW_WIDTH \
                and self.y-RADIUS >= 0
        
        if source_dir == DOWN_DIR: #Top half doesn't need to account for gap.
            return self.y+RADIUS+VERTICAL_GAP <= TREE_WINDOW_HEIGHT \
                and self.x-RADIUS-RADIUS_OFFSET >= 0 \
                and self.x+RADIUS+RADIUS_OFFSET <= TREE_WINDOW_WIDTH \
                and self.y-RADIUS >= 0
    '''
    Draw point in the center of the node as a visual aid if desired.
    '''
    # def _draw_point(self, x, y):
    #     self.canvas_ref.create_oval(x-1, y-1, x+1, y+1)

    '''
    Insert newlines/ellipses elegantly.
    '''
    #GOOD
    def _process_text(self, inputstr):
        reformatted = '\n'.join(wrap(inputstr, width=LINE_LENGTH, max_lines=MAX_LINES, placeholder="..."))
        return reformatted

    '''
    Actually draw the node based on x and y. Includs the text to go along with it.
    '''  
    #GOOD
    def draw_self(self, input_text):

        x0 = self.x-RADIUS
        y0 = self.y-RADIUS
        x1 = self.x+RADIUS
        y1 = self.y+RADIUS

        self.tkinter_id = self.canvas_ref.create_oval(x0, y0, x1+RADIUS_OFFSET, y1, fill="white")

        input_text = self._process_text(input_text)
        self.text_id = self.canvas_ref.create_text(x1-TEXT_OFFSET, y1-RADIUS, text=input_text, font=("Consolas", 12, "bold"), justify="center")

    #GOOD
    def add_child(self, child):
        self.children.append(child)

    #Node
    #TODO
    def serialization_dict(self):
        keys_to_save = {
            "input_text" : self.input_text,
            "children" : [child.serialization_dict() for child in self.children],
            "depth" : self.depth,
            "notes_frame": self.notes_frame.serialization_dict() if self.notes_frame is not None else None
        }
        return keys_to_save
        

    #Node
    #TODO: Also, apparently inner classes is not pythonic, nor does it even work the
    #same way as in Java. I guess canvas ref is fine.
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
    #TODO
    def __init__(self, input_text, depth, parent, canvas_ref, x=-1, y=-1):
        self.x = x
        self.y = y
        self.parent = parent
        self.input_text = input_text
        self.depth = depth
        
        self.children = []
        self.tkinter_id = None
        self.sliding_window_start = 0

        self.notes_frame = NotesFrame()
        self.canvas_ref = canvas_ref