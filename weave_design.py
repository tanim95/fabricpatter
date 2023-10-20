from tkinter import *

root = Tk()
root.title("Weave Design")
root.geometry("1000x600")

buttons = {}
frame1 = None

canvas = Canvas(root, bg="white")
canvas.grid(row=3, column=0, columnspan=10, padx=20, pady=20)

rectangles = []

background_color = "white"  # Default background color


def makeChoice(event):
    btn = buttons[event.widget]
    b = btn["row"] * 10
    b2 = btn["column"] * 10
    warp = btn["warp"]
    weft = btn["weft"]
    xx0 = b + 1
    yx0 = b2 - 28
    xx1 = b + 11
    yx1 = b2 - 18

    square_color = square_color_entry.get()

    if event.widget.cget("bg") == background_color:
        event.widget.config(bg=square_color)
        for a2 in range(1, 5):
            for a in range(1, 5):
                x0 = xx0 + (a * warp * 10) - (warp * 10)
                y0 = yx0 + (a2 * weft * 10) - (weft * 10)
                x1 = xx1 + (a * warp * 10) - (warp * 10)
                y1 = yx1 + (a2 * weft * 10) - (weft * 10)
                rectangle = canvas.create_rectangle(
                    x0, y0, x1, y1, fill=square_color, outline=square_color)
                rectangles.append(rectangle)
    elif event.widget.cget("bg") == square_color:
        # Checking if it's a double-click event
        if event.num == 1 and event.type == "4":  # Double-Button-1
            event.widget.config(bg=background_color)
            for a2 in range(1, 5):
                for a in range(1, 5):
                    x0 = xx0 + (a * warp * 10) - (warp * 10)
                    y0 = yx0 + (a2 * weft * 10) - (weft * 10)
                    x1 = xx1 + (a * warp * 10) - (warp * 10)
                    y1 = yx1 + (a2 * weft * 10) - (weft * 10)
                    # Remove rectangle from the canvas
                    for rect in rectangles[:]:
                        if canvas.coords(rect) == [x0, y0, x1, y1]:
                            canvas.delete(rect)
                            rectangles.remove(rect)


def createBoard(warp, weft):
    global buttons, frame1, rectangles, background_color
    if frame1:
        frame1.destroy()
        for rectangle in rectangles:
            canvas.delete(rectangle)
        rectangles = []
    frame1 = Frame(root)
    frame1.grid(row=3, column=10, padx=10)
    background_color = background_color_entry.get()
    canvas.config(bg=background_color, width=warp * 10 * 4, height=weft *
                  10 * 4, highlightthickness=3, highlightbackground=background_color)

    for b in range(3, weft + 3):
        for b2 in range(warp):
            x0 = (b * 10) + 10
            y0 = (b2 * 10)
            x1 = (b * 10) + 20
            y1 = (b2 * 10) + 10
            button = Button(frame1, text=" ", font="Courier 9", width=2,
                            height=1, bd=2, bg=background_color)
            button.grid(row=b, column=b2 + 1)
            buttons[button] = {"row": b2, "column": b,
                               "warp": warp, "weft": weft}
            button.bind("<Button-1>", makeChoice)

            if b == (weft + 2):
                bottom = Label(frame1, text=b2 + 1)
                bottom.grid(row=b + 1, column=b2 + 1)
            if b2 == 0:
                side = Label(frame1, text=weft + 3 - b)
                side.grid(row=b, column=b2)


def resetPattern():
    global frame1, rectangles
    if frame1:
        frame1.destroy()
        for rectangle in rectangles:
            canvas.delete(rectangle)
        rectangles = []
        canvas.config(width=1, height=1)
        frame1 = None


diagram_btn = Button(root, text="Create Pattern", command=lambda: createBoard(
    int(warp_entry.get()), int(weft_entry.get()))
)

diagram_btn.grid(row=1, column=6)

reset_btn = Button(root, text="Reset Pattern", command=resetPattern)
reset_btn.grid(row=1, column=7)

warp_label = Label(root, text="Warp")
weft_label = Label(root, text="Weft")
square_color_label = Label(root, text="Square Color")
background_color_label = Label(root, text="Background Color")

warp_label.grid(row=0, column=0)
weft_label.grid(row=0, column=2)
square_color_label.grid(row=0, column=4)
background_color_label.grid(row=0, column=6)

warp_entry = Entry(root, bd=3, width=3)
weft_entry = Entry(root, bd=3, width=3)
square_color_entry = Entry(root, bd=3, width=10)
background_color_entry = Entry(root, bd=3, width=10)

warp_entry.grid(row=0, column=1)
weft_entry.grid(row=0, column=3)
square_color_entry.grid(row=0, column=5)
background_color_entry.grid(row=0, column=7)

# default colors
square_color_entry.insert(0, "black")
background_color_entry.insert(0, "white")


def diagram():
    title_label = Label(
        root, text="Fabric Pattern Generator", font=("Arial", 16))
    title_label.grid(row=0, column=10, pady=(10, 20))


diagram()
root.mainloop()
