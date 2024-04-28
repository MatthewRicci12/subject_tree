from tkinter import *
from math import ceil, floor

root = Tk()
root.geometry("1000x800")
canvas = Canvas(root, width=1000, height=800)
canvas.pack()

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

DOWN = 0
LEFT = 1
RIGHT = 2
UP = 3




half_width = 500
half_height = 400


class Tree:
    
    grid = [[0 for _ in range(5)] for __ in range(7)]
    tkinter_nodes_to_ids = {}
    #Stores tuples of: (next node x, next node y, where it came FROM)
    node_queue = []
    central_node = None

    def __init__(self, input_text):
        root = Node(input_text, half_width, half_height)
        self.root = root
        self.central_node = root

        #Draw it
        tkinter_id = root.draw_circle(canvas, input_text)
        #Map it
        self.tkinter_nodes_to_ids[tkinter_id] = root
        #Grid it
        self.grid[self._determine_row(root.y)][self._determine_col(root.x)] = 1
        self._print_grid()

        #Queue it
        self.node_queue.append((root.x, root.y+VERTICAL_GAP, UP))
        self.node_queue.append((root.x-HORIZONTAL_GAP, root.y, RIGHT))
        self.node_queue.append((root.x+HORIZONTAL_GAP, root.y, LEFT))
        self.node_queue.append((root.x, root.y-VERTICAL_GAP, DOWN))


    def _determine_row(self, y):
        root_y = self.root.y

        deviations = 0

        if y > root_y:
            while y != root_y:
                y -= VERTICAL_GAP
                deviations += 1
        else:
            while y != root_y:
                y += VERTICAL_GAP
                deviations -= 1

        return 7//2+deviations


    def _determine_col(self, x):
        root_x = self.root.x

        deviations = 0

        if x > root_x:
            while x != root_x:
                x -= HORIZONTAL_GAP
                deviations += 1
        else:
            while x != root_x:
                x += HORIZONTAL_GAP
                deviations -= 1

        return 5//2+deviations

    def _print_grid(self):
        s = [[str(e) for e in row] for row in self.grid]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print('\n'.join(table))
        print()

    def _no_collide(self, grid_x, grid_y):
        return self.grid[grid_y][grid_x] == 0  

    '''
    Make new Node, add child no matter what.

    If parent_node is central node, we populate its
    x and y based on what we pop off the queue. We also
    have the notion of an equivalent "grid" x and y.

    Now that it has an x and a y: If it's in bounds:
        draw it, map it, grid it, queue it.
    '''
    def add_node(self, parent_node, input_text):
        new_node = Node(input_text)
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

                DEBUG1 = new_node._in_bounds(source_dir)
                #DEBUG2 = self._no_collide(grid_x, grid_y)
                if not new_node._in_bounds(source_dir) or not self._no_collide(grid_x, grid_y):
                    continue #This one is bad, but we keep trying.

                #Draw it
                tkinter_id = new_node.draw_circle(canvas, new_node.input_text) #I dont like calling draw_circle like this
                
                #Map it
                self.tkinter_nodes_to_ids[tkinter_id] = new_node

                #Grid it. 
                self.grid[grid_y][grid_x] = 1
                self._print_grid()

                
                #Queue it
                self.node_queue.append((new_node.x, new_node.y+VERTICAL_GAP, UP))
                self.node_queue.append((new_node.x-HORIZONTAL_GAP, new_node.y, RIGHT))
                self.node_queue.append((new_node.x+HORIZONTAL_GAP, new_node.y, LEFT))
                self.node_queue.append((new_node.x, new_node.y-VERTICAL_GAP, DOWN))
                break #Break if we found a coordinate. No need to keep pumping.


class Node:
    '''
    Change highlighted node and advance this
    node's next chosen child.
    '''
    def _increment_child(self):
        pass

    '''
    Calculate if this node is even drawable
    '''
    def _in_bounds(self, source_dir):
        if source_dir == UP: #Bottom half doesn't need to account for gap
            return self.y+RADIUS <= 800 \
                and self.x-RADIUS-OFFSET >= 0 \
                and self.x+RADIUS+OFFSET <= 1000 \
                and self.y-RADIUS-VERTICAL_GAP >= 0 
        
        if source_dir == RIGHT: #Left half doesn't need to account for gap
            return self.y+RADIUS <= 800 \
                and self.x-RADIUS-OFFSET >= 0 \
                and self.x+RADIUS+HORIZONTAL_GAP+OFFSET <= 1000 \
                and self.y-RADIUS >= 0
        
        if source_dir == LEFT: #Right half doesn't need to account for gap
            return self.y+RADIUS <= 800 \
                and self.x-RADIUS-HORIZONTAL_GAP-OFFSET >= 0 \
                and self.x+RADIUS+OFFSET <= 1000 \
                and self.y-RADIUS >= 0
        
        if source_dir == DOWN: #Top half doesn't need to account for gap.
            return self.y+RADIUS+VERTICAL_GAP <= 800 \
                and self.x-RADIUS-OFFSET >= 0 \
                and self.x+RADIUS+OFFSET <= 1000 \
                and self.y-RADIUS >= 0
    '''
    Draw point in the center of the node as a visual aid if needed.
    '''
    def _draw_point(self, x, y, canvas):
        canvas.create_oval(x-1, y-1, x+1, y+1)

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
    def draw_circle(self, canvas, input_text):

        x0 = self.x-RADIUS
        y0 = self.y-RADIUS
        x1 = self.x+RADIUS
        y1 = self.y+RADIUS

        id = canvas.create_oval(x0, y0, x1+OFFSET, y1, fill="white")
        input_text = self._process_text(input_text)
        canvas.create_text(x1-15, y1-RADIUS, text=input_text, font=("Consolas", 12, "bold"), justify="center")
        self._draw_point(x1-15, y1-RADIUS, canvas)
        canvas.create_rectangle(x0+HEURISTIC_1, y0+HEURISTIC_2, x1+OFFSET-HEURISTIC_1, y1-HEURISTIC_2)
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
    def __init__(self, input_text, x=-1, y=-1):
        self.x = x
        self.y = y
        self.input_text = input_text
        self.children = []
        self.next_child = DOWN
        self.tkinter_id = None


#A Node object only needs x, y, and input text. We already know the x and y for the subject node.
tree = Tree("Differential Equations")
#Only spec input text; from here, x and y determined another way.
#tree.add_node(tree.root, "Differential Equations")

tree.add_node(tree.root, "Linear Algebra1")
tree.add_node(tree.root, "Linear Algebra2")
tree.add_node(tree.root, "Linear Algebra3")
tree.add_node(tree.root, "Linear Algebra4")

tree.add_node(tree.root, "Linear Algebra5")
tree.add_node(tree.root, "Linear Algebra6")
tree.add_node(tree.root, "Linear Algebra7")
tree.add_node(tree.root, "Linear Algebra8")
tree.add_node(tree.root, "Linear Algebra9")
tree.add_node(tree.root, "Linear Algebra10")
tree.add_node(tree.root, "Linear Algebra11")
tree.add_node(tree.root, "Linear Algebra12")
tree.add_node(tree.root, "Linear Algebra13")
tree.add_node(tree.root, "Linear Algebra14")
tree.add_node(tree.root, "Linear Algebra15")
tree.add_node(tree.root, "Linear Algebra16")
tree.add_node(tree.root, "Linear Algebra17")
tree.add_node(tree.root, "Linear Algebra18")
tree.add_node(tree.root, "Linear Algebra19")
tree.add_node(tree.root, "Linear Algebra20")
tree.add_node(tree.root, "Linear Algebra21")
tree.add_node(tree.root, "Linear Algebra22")
tree.add_node(tree.root, "Linear Algebra23")
tree.add_node(tree.root, "Linear Algebra24")
tree.add_node(tree.root, "Linear Algebra25")
tree.add_node(tree.root, "Linear Algebra26")
tree.add_node(tree.root, "Linear Algebra27")
tree.add_node(tree.root, "Linear Algebra28")
tree.add_node(tree.root, "Linear Algebra29")
tree.add_node(tree.root, "Linear Algebra30")
tree.add_node(tree.root, "Linear Algebra31")
tree.add_node(tree.root, "Linear Algebra32")
tree.add_node(tree.root, "Linear Algebra33")
tree.add_node(tree.root, "Linear Algebra34")
tree.add_node(tree.root, "Linear Algebra35")
tree.add_node(tree.root, "Linear Algebra36")
tree.add_node(tree.root, "Linear Algebra37")
tree.add_node(tree.root, "Linear Algebra38")
tree.add_node(tree.root, "Linear Algebra39")
tree.add_node(tree.root, "Linear Algebra40")
tree.add_node(tree.root, "Linear Algebra41")
tree.add_node(tree.root, "Linear Algebra42")
tree.add_node(tree.root, "Linear Algebra43")
tree.add_node(tree.root, "Linear Algebra44")
tree.add_node(tree.root, "Linear Algebra45")
tree.add_node(tree.root, "Linear Algebra46")
tree.add_node(tree.root, "Linear Algebra47")
tree.add_node(tree.root, "Linear Algebra48")
tree.add_node(tree.root, "Linear Algebra49")
tree.add_node(tree.root, "Linear Algebra50")
tree.add_node(tree.root, "Linear Algebra51")
tree.add_node(tree.root, "Linear Algebra52")
tree.add_node(tree.root, "Linear Algebra53")
tree.add_node(tree.root, "Linear Algebra54")
tree.add_node(tree.root, "Linear Algebra55")
tree.add_node(tree.root, "Linear Algebra56")
tree.add_node(tree.root, "Linear Algebra57")
tree.add_node(tree.root, "Linear Algebra58")
tree.add_node(tree.root, "Linear Algebra59")
tree.add_node(tree.root, "Linear Algebra60")
tree.add_node(tree.root, "Linear Algebra61")
tree.add_node(tree.root, "Linear Algebra62")
tree.add_node(tree.root, "Linear Algebra63")
tree.add_node(tree.root, "Linear Algebra64")
tree.add_node(tree.root, "Linear Algebra65")
tree.add_node(tree.root, "Linear Algebra66")
tree.add_node(tree.root, "Linear Algebra67")
tree.add_node(tree.root, "Linear Algebra68")
tree.add_node(tree.root, "Linear Algebra69")
tree.add_node(tree.root, "Linear Algebra70")
tree.add_node(tree.root, "Linear Algebra71")
tree.add_node(tree.root, "Linear Algebra72")
tree.add_node(tree.root, "Linear Algebra73")
tree.add_node(tree.root, "Linear Algebra74")
tree.add_node(tree.root, "Linear Algebra75")
tree.add_node(tree.root, "Linear Algebra76")
tree.add_node(tree.root, "Linear Algebra77")
tree.add_node(tree.root, "Linear Algebra78")
tree.add_node(tree.root, "Linear Algebra79")
tree.add_node(tree.root, "Linear Algebra80")
tree.add_node(tree.root, "Linear Algebra81")
tree.add_node(tree.root, "Linear Algebra82")
tree.add_node(tree.root, "Linear Algebra83")
tree.add_node(tree.root, "Linear Algebra84")
tree.add_node(tree.root, "Linear Algebra85")
tree.add_node(tree.root, "Linear Algebra86")
tree.add_node(tree.root, "Linear Algebra87")
tree.add_node(tree.root, "Linear Algebra88")
tree.add_node(tree.root, "Linear Algebra89")
tree.add_node(tree.root, "Linear Algebra90")
tree.add_node(tree.root, "Linear Algebra91")
tree.add_node(tree.root, "Linear Algebra92")
tree.add_node(tree.root, "Linear Algebra93")
tree.add_node(tree.root, "Linear Algebra94")
tree.add_node(tree.root, "Linear Algebra95")
tree.add_node(tree.root, "Linear Algebra96")
tree.add_node(tree.root, "Linear Algebra97")
tree.add_node(tree.root, "Linear Algebra98")
tree.add_node(tree.root, "Linear Algebra99")


# create_circle(half_width, half_height, canvas, "Differential Equations")
# add_node(canvas, "Differential Equations1")
# add_node(canvas, "Differential Equations2")
# add_node(canvas, "Differential Equations3")
# add_node(canvas, "Differential Equations4")

root.mainloop()

#Bug: No spaces breaks it




# from tkinter import *
# from tkinter import messagebox
# from subjectnode import *


# top_node_exists = False



# def add_child_to_node(event):
#     pass


# def create_subject_node(inputtxt):
#     global newWindow

#     subject = inputtxt.get()
#     inputtxt.master.destroy()

#     half_width = newWindow.winfo_width() >> 1
#     half_height = newWindow.winfo_height() >> 1

#     #top_subject_node = subjectNode(subject, half_width, half_height, canvas, add_child_to_node)

# def make_new_tree():
#     global newWindow

#     top.destroy()
#     newWindow = Tk()
#     newWindow.geometry("1000x600")

#     if not top_node_exists:
#         win = Toplevel(takefocus=True)
#         win.attributes("-topmost", True)
#         win.grab_set()

#         subject = StringVar()
#         inputtxt = Entry(win, textvariable=subject) 
#         inputtxt.pack() 
#         printButton = Button(win, text = "Submit", \
#                              command = lambda inputtxt=inputtxt: create_subject_node(inputtxt)) 
#         printButton.pack()

#     newWindow.mainloop()  


# def load_existing_tree():
#     pass



# top = Tk()
# top.geometry("600x600")
# newWindow = None
# newWindow.columnconfigure(0, weight=1)
# newWindow.rowconfigure(0, weight=1)
# canvas = Canvas(newWindow)
# canvas.grid(column=0, row=0, sticky=(N, W, E, S))

# make_new_tree_button = Button(top, text ="Make new tree", command = make_new_tree)
# load_existing_tree_button = Button(top, text ="Load existing tree", command = load_existing_tree)
# make_new_tree_button.place(x=50,y=50)
# load_existing_tree_button.place(x=50, y=100)

# top.mainloop()

