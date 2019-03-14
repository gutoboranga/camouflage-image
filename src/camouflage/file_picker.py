import Tkinter as tk
from Tkinter import Tk, Frame, BOTH
from tkFileDialog import askopenfilename


class FilePicker(Frame):
    
    background_path = ''
    overlay_path = ''

    def __init__(self):
        root = tk.Tk()
        root.geometry("200x350")
        
        Frame.__init__(self, root, background="white")
        self.create_widgets()
        self.master.title("Choose the images")
        self.pack(fill=BOTH, expand=1)
        
        root.mainloop()
        

    def create_widgets(self):
        self.background_label = tk.Label(self, text="Background image")
        self.background_label.pack(side="top")

        self.background_open_button = tk.Button(self, None, text="Open", command= lambda: self.open('background'))
        self.background_open_button.pack(side="top")
        
        self.background_picked_label = tk.Label(self, text="", wraplength=180)
        self.background_picked_label.pack(side="top", pady=(0,20))
        
        self.overlay_label = tk.Label(self, text="Overlay image")
        self.overlay_label.pack(side="top")

        self.overlay_open_button = tk.Button(self, None, text="Open", command= lambda: self.open('overlay'))
        self.overlay_open_button.pack(side="top")
        
        self.overlay_picked_label = tk.Label(self, text="", wraplength=180)
        self.overlay_picked_label.pack(side="top", pady=(0,20))
        
        self.camouflage_button = tk.Button(self, None, text="Go", command=self.go)
        self.camouflage_button.pack(side="bottom", pady=(10,30))

    #universal methods
    def open(self, mode):
        path = askopenfilename()
        
        if mode == 'background':
            self.background_picked_label['text'] = path
            self.background_path = path
        else:
            self.overlay_picked_label['text'] = path
            self.overlay_path = path
            
    def go(self):
        self.master.destroy()

