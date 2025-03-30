from tkinter import Toplevel, Button, CENTER, Message

class IterationBase:
    @staticmethod
    def newButton(parent, x, y, text, bcolor, fcolor, cmd):
        def open_new_window():
            newWindow = Toplevel(parent)
            newWindow.geometry("500x500")
            newWindow.title("Output")
            newWindow.configure(bg="#6F7172")
            result = cmd()
            Message(newWindow, text=result).pack()

        def on_enter(e):
            mybutton['background'] = bcolor
            mybutton['foreground'] = fcolor

        def on_leave(e):
            mybutton['background'] = fcolor
            mybutton['foreground'] = bcolor

        #def on_click(e):
        #    open_new_window()

        mybutton = Button(parent, width=30, height=2, border=0,
                          activebackground=bcolor, activeforeground=fcolor,
                          text=text, command=cmd, font=("Roboto", 10, "bold"))
        mybutton.bind("<Enter>", on_enter)
        mybutton.bind("<Leave>", on_leave)
        mybutton.place(relx=x, rely=y, anchor=CENTER)
        #mybutton.bind("<Button-1>", on_click)
