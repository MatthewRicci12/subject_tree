
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
    
    def __init__(self, canvas, input_text):
        root = Node(input_text, 0, half_width, half_height)
        self.root = root
        self.central_node = root

        self.grid = [[0 for _ in range(5)] for __ in range(7)]
        self.tkinter_nodes_to_ids = {}
        self.node_queue = []
        self.central_node = root

        #Draw it
        tkinter_id = root.draw_circle(canvas, input_text)
        #Map it
        self.tkinter_nodes_to_ids[tkinter_id] = root
        #Grid it
        self.grid[self._determine_row(root.y)][self._determine_col(root.x)] = 1

        #Queue it
        self.node_queue.append((root.x, root.y+VERTICAL_GAP, UP_DIR))
        self.node_queue.append((root.x-HORIZONTAL_GAP, root.y, RIGHT_DIR))
        self.node_queue.append((root.x+HORIZONTAL_GAP, root.y, LEFT_DIR))
        self.node_queue.append((root.x, root.y-VERTICAL_GAP, DOWN_DIR))




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
    
    def add_existing_node(self, canvas, parent_node, new_node, do_add_child=True):
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
                tkinter_id = new_node.draw_circle(canvas, new_node.input_text) #I dont like calling draw_circle like this
                
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
    def add_node(self, canvas, parent_node, input_text):
        new_node = Node(input_text, parent_node.depth+1)
        self.add_existing_node(canvas, parent_node, new_node)


    def redraw(self, canvas):
        #Constructor, except we already know root.
        self.grid = [[0 for _ in range(5)] for __ in range(7)]
        self.tkinter_nodes_to_ids = {}
        self.node_queue = []
        root = self.central_node

        #Draw it
        tkinter_id = root.draw_circle(canvas, root.input_text)
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
        for i in range(sws, sws+35):
            self.add_existing_node(canvas, self.central_node, children[i % num_children], False)

        canvas.update()

class Node:
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
        self.tkinter_id = id
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
    def __init__(self, input_text, depth, x=-1, y=-1):
        self.x = x
        self.y = y
        self.input_text = input_text
        self.children = []
        self.depth = depth
        self.tkinter_id = None
        self.sliding_window_start = 0
