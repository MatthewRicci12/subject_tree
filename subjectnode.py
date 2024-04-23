

class subjectNode:
    def __init__(self, title, x, y, r, canvas, callback):
        self.title = title
        self.circle_id = self.place_node(x, y, r, canvas)


    def place_node(self, x, y, r, canvas): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        circle_id = canvas.create_oval(x0, y0, x1, y1)
        canvas.create_text(x0+r, y0+r, text=self.title)
        return circle_id
    
    def get_tkinter_id(self):
        return self.circle_id