from tkinter import *
from tkinter import messagebox
from tkinter import font as tkFont
import PIL.Image
import PIL.ImageTk
import random

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

    def mouse_click(self, event, tkinter_id):
        '''  delay mouse action to allow for double click to occur
        '''
        self.clicked = tkinter_id
        self.canvas_ref.after(300, self.mouse_action, event)


    def double_click(self, event):
        self.double_click_flag = True
        
    def mouse_action(self, event):
        id = self.clicked
        if self.double_click_flag:
            self.double_click_flag = False
            self.invoke_notes(id)
        else:
            self.change_root(id)
    

    def return_to_main_menu():
        pass

    def init_side_frame(self):
        self.frame = Frame(self.window_ref,bg='orange',width=200,height=800)
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
                                                        canvas=self.canvas_ref: self.move(-5))
        self.right_button = Button(self.button_frame, relief='flat', bg='orange', command=lambda \
                                                        canvas=self.canvas_ref: self.move(5))
        self.left_button.config(image=self.left_icon)
        self.left_button.image = self.left_icon
        self.right_button.config(image=self.right_icon)
        self.right_button.image = self.right_icon
        self.left_button.grid(row = 0, column = 0)
        self.right_button.grid(row = 0, column = 1)


        self.depth_label = Label(self.frame, text = "Depth={}".format(self.central_node.depth), bg='orange',font=('Helvetica', 20))
        self.depth_label.grid(row = 2, column = 0, sticky="s")


        self.frame.grid_propagate(False)

    def submit_child(self, node_ref, child_name):
        self.add_child_dialog.destroy()
        self.add_node(node_ref, child_name)

    def submit_child_batch(self, node_ref):
        children_names = self.inputtxt.get("1.0",END)
        self.add_child_dialog.destroy()
        for child_name in children_names.split("\n"):
            if len(child_name) > 0:
                self.add_node(node_ref, child_name)



        
    def menu_add_child_node(self):
        tkinter_id = self.clicked
        node_ref = self.tkinter_nodes_to_ids[tkinter_id]
        self.add_child_dialog = Toplevel(takefocus=True)
        self.add_child_dialog.attributes("-topmost", True)
        self.add_child_dialog.grab_set()

        child_name = StringVar()
        self.inputtxt = Entry(self.add_child_dialog, textvariable=child_name) 
        self.inputtxt.pack()    
        self.printButton = Button(self.add_child_dialog, text = "Submit", \
                            command = lambda child_name=child_name, node_ref=node_ref: \
                                self.submit_child(node_ref, child_name.get())) 
        self.printButton.pack()
      

    def menu_batch_add_child_node(self):
        tkinter_id = self.clicked
        node_ref = self.tkinter_nodes_to_ids[tkinter_id]
        self.add_child_dialog = Toplevel(takefocus=True)
        self.add_child_dialog.attributes("-topmost", True)
        self.add_child_dialog.grab_set()

        self.inputtxt = Text(self.add_child_dialog) 
        self.inputtxt.pack()    
        self.printButton = Button(self.add_child_dialog, text = "Submit", \
                            command = lambda node_ref=node_ref: \
                                self.submit_child_batch(node_ref)) 
        self.printButton.pack()

    def menu_batch_delete_node(self):
        tkinter_id = self.clicked
        node_ref = self.tkinter_nodes_to_ids[tkinter_id]

        if node_ref is self.central_node:
            if node_ref is self.root:
                if not node_ref.children: 
                    return #We deleted root, and there is no successor
                else:
                    return #We deleted root with at least one successor
            else:
                return #Central node, but not root
        else:
            #A simple child node that is currently visible
            parent = node_ref.parent   
            parent.children.remove(node_ref)
            self.redraw()
            
    def menu_go_to_parent(self):
        tkinter_id = self.clicked
        node_ref = self.tkinter_nodes_to_ids[tkinter_id]
        parent = node_ref.parent
        self.central_node = parent
        self.redraw()
            
        
    def popup(self): 
        messagebox.showinfo("",  "ID of clicked widget: {}".format(self.clicked)) 

    def show_popup_menu(self, event, id):
        self.clicked = id
        try: 
            self.popup_menu.tk_popup(event.x_root, event.y_root) 
        finally: 
            self.popup_menu.grab_release() 


    def init_popup_menu(self):
        self.popup_menu = Menu(self.window_ref, tearoff = 0)

        self.popup_menu.add_command(label = "Add child node", command = self.menu_add_child_node)
        self.popup_menu.add_command(label = "Batch add child node", command = self.menu_batch_add_child_node)
        self.popup_menu.add_command(label = "Delete node", command = self.menu_batch_delete_node)
        self.popup_menu.add_command(label = "Change style", command = self.popup)
        self.popup_menu.add_command(label = "Mark as done", command = self.popup)
        self.popup_menu.add_command(label = "Go to parent", command = self.menu_go_to_parent)

    def invoke_notes(self, tkinter_id):
        node_ref = self.tkinter_nodes_to_ids[tkinter_id]
        node_ref.open_notes_menu()
        

    def __init__(self, canvas_ref, input_text, window_ref): #Maybe more like canvas_ref? And make it a member?
        self.canvas_ref = canvas_ref
        self.window_ref = window_ref       
        root = Node(input_text, 0, None, half_width, half_height)
        self.root = root
        self.central_node = root
        self.init_side_frame()
        self.init_popup_menu()



        self.grid = [[0 for _ in range(5)] for __ in range(7)]
        self.tkinter_nodes_to_ids = {}
        self.node_queue = []
        self.central_node = root

        #Draw it
        tkinter_id = root.draw_circle(self.canvas_ref, input_text)
        #Map it
        self.tkinter_nodes_to_ids[tkinter_id] = root
        self.canvas_ref.tag_bind(tkinter_id, '<Button-3>', lambda event, tkinter_id=tkinter_id: self.show_popup_menu(event, tkinter_id))
        self.canvas_ref.tag_bind(tkinter_id, '<Button-1>', lambda _, tkinter_id=tkinter_id: self.mouse_click(_, tkinter_id))             
        self.canvas_ref.tag_bind(tkinter_id, '<Double-Button-1>', lambda _: self.double_click(_))                   
        #Grid it
        self.grid[self._determine_row(root.y)][self._determine_col(root.x)] = 1

        #Queue it
        self.node_queue.append((root.x, root.y+VERTICAL_GAP, UP_DIR))
        self.node_queue.append((root.x-HORIZONTAL_GAP, root.y, RIGHT_DIR))
        self.node_queue.append((root.x+HORIZONTAL_GAP, root.y, LEFT_DIR))
        self.node_queue.append((root.x, root.y-VERTICAL_GAP, DOWN_DIR))

        self.double_click_flag = False



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

                #Draw it
                tkinter_id = new_node.draw_circle(self.canvas_ref, new_node.input_text) #I dont like calling draw_circle like this
                self.canvas_ref.tag_bind(tkinter_id, '<Button-3>', lambda event, tkinter_id=tkinter_id: self.show_popup_menu(event, tkinter_id))
                self.canvas_ref.tag_bind(tkinter_id, '<Button-1>', lambda _, tkinter_id=tkinter_id: self.mouse_click(_, tkinter_id))             
                self.canvas_ref.tag_bind(tkinter_id, '<Double-Button-1>', lambda _: self.double_click(_))  
                #Map it
                self.tkinter_nodes_to_ids[tkinter_id] = new_node

                #Grid it. 
                self.grid[grid_y][grid_x] = 1

                
                #Queue it
                self.node_queue.append((new_node.x, new_node.y+VERTICAL_GAP, UP_DIR))
                self.node_queue.append((new_node.x-HORIZONTAL_GAP, new_node.y, RIGHT_DIR))
                self.node_queue.append((new_node.x+HORIZONTAL_GAP, new_node.y, LEFT_DIR))
                self.node_queue.append((new_node.x, new_node.y-VERTICAL_GAP, DOWN_DIR))
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
        new_node = Node(input_text, parent_node.depth+1, parent_node)
        self.add_existing_node(parent_node, new_node)


    def redraw(self):
        self.canvas_ref.delete('all')

        #Constructor, except we already know root.
        self.grid = [[0 for _ in range(5)] for __ in range(7)]
        self.tkinter_nodes_to_ids = {}
        self.node_queue = []
        root = self.central_node

        #Draw it
        tkinter_id = root.draw_circle(self.canvas_ref, root.input_text)
        self.canvas_ref.tag_bind(tkinter_id, '<Button-3>', lambda event, tkinter_id=tkinter_id: self.show_popup_menu(event, tkinter_id))
        self.canvas_ref.tag_bind(tkinter_id, '<Button-1>', lambda _, tkinter_id=tkinter_id: self.mouse_click(_, tkinter_id))             
        self.canvas_ref.tag_bind(tkinter_id, '<Double-Button-1>', lambda _: self.double_click(_))                   
        self.depth_label.config(text = "Depth={}".format(self.central_node.depth))
        #Map it
        self.tkinter_nodes_to_ids[tkinter_id] = root
        #Grid it
        self.grid[self._determine_row(root.y)][self._determine_col(root.x)] = 1

        #Queue it
        self.node_queue.append((root.x, root.y+VERTICAL_GAP, UP_DIR))
        self.node_queue.append((root.x-HORIZONTAL_GAP, root.y, RIGHT_DIR))
        self.node_queue.append((root.x+HORIZONTAL_GAP, root.y, LEFT_DIR))
        self.node_queue.append((root.x, root.y-VERTICAL_GAP, DOWN_DIR))


        children = self.central_node.children
        num_children = len(children)
        sws = self.central_node.sliding_window_start
        for i in range(sws, min(sws+num_children, sws+35)):
            self.add_existing_node(self.central_node, children[i % num_children], False)
        self.canvas_ref.update()

class Node:

    def open_notes_menu(self):
        self.notes_menu = Toplevel(takefocus=True)
        self.notes_menu.attributes("-topmost", True)
        self.notes_menu.grab_set()
        self.notes_menu.geometry("1200x800")

        self.frame = Frame(self.notes_menu, width=1200, height=30, bg="orange")
        self.frame.pack(fill=X)

        self.add_node_button = Button(self.frame, text = "Add Note", bg='orange',font=('Helvetica', 12), \
                                      relief='flat', command = self.add_note)
        self.add_node_button.pack(side=TOP)

        self.frame2 = Frame(self.notes_menu)
        self.frame2.pack(fill = BOTH, expand = True)  

        self.frame.pack_propagate(False)

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
    Draw point in the center of the node as a visual aid if needed.
    '''
    def _draw_point(self, x, y, canvas_ref):
        canvas_ref.create_oval(x-1, y-1, x+1, y+1)

    '''
    Determine line breaks in the text via well-known "brackets"
    '''
    def _determine_bracket(self, index):
        if index <= 14:
            return 1
        if index > 14 and index <= 29:
            return 2
        if index > 29 and index <= 44:
            return 3
        
    '''
    Insert newlines/ellipses elegantly.
    '''
    def _process_text(self, inputstr):
        space_indices = []

        for i in range(0, len(inputstr)):
            if inputstr[i] == " ":
                space_indices.append((i, self._determine_bracket(i)))

        if len(space_indices) == 0: #Still doesnt account for if its long tho
            return inputstr
            
        for i in range(0, len(space_indices)-1):
            first_space_index = space_indices[i][0]
            first_space_bracket = space_indices[i][1]
            second_space_index = space_indices[i+1][0]
            second_space_bracket = space_indices[i+1][1]

            if first_space_bracket != second_space_bracket:
                inputstr = inputstr[:first_space_index] + "\n" + inputstr[first_space_index+1:]
        
        if len(space_indices) == 1:
            only_space_index = space_indices[0][0]
            only_space_bracket = space_indices[0][1]
            len_bracket = self._determine_bracket(len(inputstr)-1)

            if only_space_bracket != len_bracket:
                inputstr = inputstr[:only_space_index] + "\n" + inputstr[only_space_index+1:]  

        last_space_index = space_indices[-1][0]
        last_space_bracket = space_indices[-1][1]
        len_bracket = self._determine_bracket(len(inputstr)-1)   

        if last_space_bracket != len_bracket:
                inputstr = inputstr[:last_space_index] + "\n" + inputstr[last_space_index+1:]      
                
        if len(inputstr) >= 59:
            inputstr = inputstr[:space_indices[-1][0]] + "\n" + inputstr[space_indices[-1][0]+1:]
            if len(inputstr) >= 60:
                inputstr = inputstr[:56]
                inputstr += "..."

        return inputstr

    '''
    Actually draw the node based on x and y. Includs the text to go along with it.
    '''  
    def draw_circle(self, canvas_ref, input_text):

        x0 = self.x-RADIUS
        y0 = self.y-RADIUS
        x1 = self.x+RADIUS
        y1 = self.y+RADIUS

        id = canvas_ref.create_oval(x0, y0, x1+OFFSET, y1, fill="white")
        self.tkinter_id = id
        input_text = self._process_text(input_text)
        canvas_ref.create_text(x1-15, y1-RADIUS, text=input_text, font=("Consolas", 12, "bold"), justify="center")
        self._draw_point(x1-15, y1-RADIUS, canvas_ref)
        canvas_ref.create_rectangle(x0+HEURISTIC_1, y0+HEURISTIC_2, x1+OFFSET-HEURISTIC_1, y1-HEURISTIC_2)
        return id

    '''
    Add child to this node.
    We do 
    '''
    def add_child(self, child):
        self.children.append(child)
        
    '''
    Only requires an x, a y, and some input text.
    children = Its children. Starts empty ofc.
    dir = Which direction the next node will be added in
    next_child = Which child gets the highlight next. This is a DRAWING
        concern only.
    tkinter_id = If it DOES get drawn, we want whatever ID tkinter assigned
        to it so we can bind callbacks.
    '''
    def __init__(self, input_text, depth, parent, x=-1, y=-1):
        self.x = x
        self.y = y
        self.parent = parent
        self.input_text = input_text
        self.children = []
        self.depth = depth
        self.tkinter_id = None
        self.sliding_window_start = 0
        self.notes = None

    def create_note(self, note_type_input):
        self.add_note_dialog.destroy()
        self.notes = Note(self.frame2, note_type_input)


    def add_note(self):
        self.add_note_dialog = Toplevel(takefocus=True)
        self.add_note_dialog.attributes("-topmost", True)
        self.add_note_dialog.grab_set()

        note_type_label = Label(self.add_note_dialog, text="Enter the type of note")
        note_title = StringVar()
        note_type = StringVar()
        note_type_input = Entry(self.add_note_dialog, textvariable=note_type)
        note_type_label.pack()
        note_type_input.pack()
        submit_button = Button(self.add_note_dialog, text="Submit", command=lambda note_type_input=note_type_input:self.create_note(note_type_input.get()))
        submit_button.pack()

class Note:

    def save_text(self):
        self.contents = self.textbox_popup.get("1.0",'end-1c')
        self.note_preview.delete("1.0", END)
        self.note_preview.insert("1.0", self.contents)
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

    def __init__(self, frame, note_type_input):
        #self.note_title_input = note_title_input
        self.note_type_input = note_type_input
        self.frame_ref = frame

        self.label = Label(self.frame_ref, text=note_type_input, font=("Times New Roman", 14, "bold"), fg=self.get_random_color(), borderwidth=2, relief="groove")
        self.label.pack(padx=5, anchor="w")
        self.note_preview = Text(self.frame_ref, borderwidth=1, relief="solid", height=8) #T = Text(root, bg, fg, bd, height, width, font, ..) 
        self.note_preview.configure(state="disabled")
        self.note_preview.pack(fill=X, padx=(5, 5), pady=(0, 3)) #Order: (left, right) (up, down)
        self.note_preview.bind("<Button-1>", self.popup_textbox)
        self.contents = ""