'''
# Code snippet 1: Switching between windows upon closing

I have two things I am not sure how to do elegantly, that are related:
1. If you run the app, there's a main menu that pops up, then it closes, and a new
main window pops up to host all further activities. However, if you close THAT window,
we go BACK to the original, main menu. So to do that, so far I have:

tree.run()
main()
def main():
    app = App()
    app.run()

CAVEAT #1: I am going to implement the whole main.py/gui_main.py thing soon, so please ignore
the fact I am doing it this way for now. I want to switch between windows upon close.

The logic here is that the tree (sub-window) runs its mainloop. Once that loop dies, we restart the
application by calling main all over again.


2. Triggering an event when a window is closed

This is the way I found on the internet:
window.protocol("WM_DELETE_WINDOW", self.command)
Where you call .protocl() on a window, and then pass "WM_DELETE_WINDOW" and then self.command.
Is this already the best way to do it, or is there a better way?


'''


'''
Code snippet 2: Handling dialogs

So far, what I do is:
1. Initialize the dialog.

        self.add_note_dialog = Toplevel(takefocus=True)
        self.add_note_dialog.attributes("-topmost", True)
        self.add_note_dialog.grab_set()
        self.add_note_dialog.bind('<Return>', self.create_note_postdialog)

All methods, that a dialog calls, I have invented a naming convention, such that they have
the word "postdialog" in them to reminid me that they are "post" (after) the dialog. I usually
let "enter" do the same thing so you can just hit enter, instead of HAVING to click a button.

2. If I need to grab input from it:
        self.submitted_child_name_stringvar = StringVar()
        self.inputtxt = Entry(self.add_child_dialog, textvariable=self.submitted_child_name_stringvar) 

I use a string var, then bind it with an entry or something. Then in the POSTDIALOG method, I can do:
self.add_child_dialog.destroy()
submitted_child_name = self.submitted_child_name_stringvar.get()

Getting rid of the dialog, then using .get() to grab the stringvar. NOTE: I do know that you told
me how to handle dialogs, with a try/except. I will implement this, pretend that I've already
done that for now.

'''

'''
Code snippet #3: "No-event" macro

By default, if I make a call like this:
self.tree_creation_dialog.bind('<Return>', self.postdialog_create_cur_tree)

Python will yell at me that postdialog_create_cur_tree was passed two arguments (self and event) when
in reality it only takes self. But I don't need a parameter here, and I find using a dummy parameter
isn't very elegant, as if I had done:

def postdialog_create_cur_tree(self, _):
    ...

So I found a wrapper online that remedies this problem:
def no_event(func):
    @functools.wraps(func)
    def wrapper(self, *args):
        return func(self)
    return wrapper

So that I can do:
@no_event
def postdialog_create_cur_tree(self):
    ...


Is there a better way to handle Tkinter's obnoxious assumption that I always want to 
take an event?

'''

'''
Code snippet #4: Geometry and initializing windows in general

I don't think there's any magic to this, just calling its constructor and using grid, pack,
or place. But if you know something non-straightforward, do let me know!

'''

'''
Code snippet #5: Serialization

So can't pickle the application because you can't pickle TK objects. So instead, I'm only
saving the essential information needed to construct a TK object. To do this, I have a
"serialization_dict" system that's recursive. Every class has a:
1. _construct_from_payload method, which is an alternative constructor, that takes an
already-populated dictionary and constructs the class based on that. Recursive, because it
also often calls other _construct_from_payload methods. E.g. a node has children, so:

for child_node_payload in payload["children"]:
    new_node = Node._construct_from_payload(child_node_payload, node, canvas_ref)
    node.children.append(new_node)
2. A serialization_dict method, which stores only essential information. It always follows
this general form:    
def serialization_dict(self):
        keys_to_pickle = {"root" : self.root.serialization_dict(),
                          "labels": NotesFrame.labels}
        return keys_to_pickle
Where I save all non-TK objects, to be used in a constructor later.

Any other way to get past the pickling problem?

'''

'''
Code snippet #6: Event binding in general

I already showed you the @no_event debacle. But yea I generally just use bind:

note.note_preview.bind("<Button-1>", tree.root.notes_frame.mouse_click)
note.note_preview.bind("<Double-Button-1>", tree.root.notes_frame.double_click)


Or if it's a Button, that obviously just goes in "command" parameter:
self.printButton = Button(self.add_child_dialog, text = "Submit", \
                    command = self.postdialog_submit_child) 

'''

'''
Code snippet #7: Canvas for node drawing

There's a lot, I would just ctrl+f for the word "canvas", but some snippets:

1. create_* family of methods for placement of shapes
 self.tkinter_id = self.canvas_ref.create_oval(x0, y0, x1+RADIUS_OFFSET, y1, fill="white")

2. tag_bind, so that I can bind events to said objects:
       self.tkinter_ids_to_nodes[node.tkinter_id] = node
        self.canvas.tag_bind(node.tkinter_id, '<Button-3>', self.show_popup_menu)

Sadly I have to map these tkinter_ids to the node objects, so I can even tag bind them.
'''

'''
Code snippet #8: Popup menu

self.canvas.tag_bind(node.tkinter_id, '<Button-3>', self.show_popup_menu)

    def show_popup_menu(self, event):
        self.clicked_id = event.widget.find_closest(event.x, event.y)[0]
        try: 
            self.popup_menu.tk_popup(event.x_root, event.y_root) 
        finally: 
            self.popup_menu.grab_release() 

          self.popup_menu = Menu(self.tree_window, tearoff = 0)

WHERE popup_menu:

      self.popup_menu = Menu(self.tree_window, tearoff = 0)

        self.popup_menu.add_command(label = "Add child node", command = self.dialog_menu_add_child_node)
        self.popup_menu.add_command(label = "Batch add child node", command = self.dialog_menu_batch_add_child_node)
        self.popup_menu.add_command(label = "Rename node", command = self.dialog_menu_rename_node)
        self.popup_menu.add_command(label = "Delete node", command = self.menu_delete_node)
        self.popup_menu.add_command(label = "Go to parent", command = self.menu_go_to_parent)
'''

