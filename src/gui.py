from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import cv2
import os 
import tracker

BACKGROUND = '#f5f5f5'
BUTTONS = '#ffffff'
TEXT = '#D54A37'

def load_video():
    """ callback function """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    #video_fn = askopenfilename(initialdir=r'C:\Users\student\Documents\GitHub\K9andFriends\videos')
    video_fn = askopenfilename(initialdir=dir_path)

def start():
    """ callback function """
    tracker.track(video_fn.get(), output_dir.get(), int(dog_min.get()), int(dog_max.get()), int(robot_min.get()), int(robot_max.get()))

def set_output_dir():
    """ callback function """
    output_dir.set(askdirectory())

root = Tk()
root.title(":)")
root.configure(background=BACKGROUND)
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('{}x{}'.format(200, root.winfo_screenheight()))

root.focus_set() # move focus to this widget
root.bind("<Escape>", lambda e: e.widget.quit())

# Define all the variables
video_fn = StringVar()
output_dir = StringVar()
paths = IntVar()
boxes = IntVar()
distance = IntVar()
dog_max = StringVar()
dog_min = StringVar()
robot_max = StringVar()
robot_min = StringVar()

# Header
headline = Label(root, font="Gisha 20 bold", bg=BACKGROUND, fg=TEXT, text="K9-Robot", anchor=CENTER)
headline.grid(row=0, column=0, columnspan=7, padx=20, pady=5)

# Left input and output settings
btn1 = Button(root, font="Gisha 12", fg=BUTTONS, bg=TEXT, command=load_video, text="Load Video", width=12)
btn1.grid(row=1, column=0, padx=20, pady=5)
video_fn.set('../videos/ana.mp4')
btn2 = Button(root, font="Gisha 12", fg=BUTTONS, bg=TEXT, command=set_output_dir, text="Output Path", width=12)
btn2.grid(row=2, column=0, padx=20, pady=5)
output_dir.set('../results')
btn3 = Button(root, font="Gisha 12", fg=BUTTONS, bg=TEXT, command=start, text="Start", width=12)
btn3.grid(row=3, column=0, padx=20, pady=5)
label1 = Label(root, font="Gisha 12", fg=TEXT, bg=BACKGROUND, text="dog max size:", width=20)
label1.grid(row=4, column=0, padx=0, pady=0)
entry1 = Entry(root, font="gisha 12", fg=TEXT, bg=BUTTONS, textvariable=dog_max, width=12)
entry1.grid(row=5, column=0, padx=20, pady=5)
dog_max.set("1000000")
label2 = Label(root, font="gisha 12", fg=TEXT, bg=BACKGROUND, text="dog min size:", width=20)
label2.grid(row=6, column=0, padx=0, pady=0)
entry2 = Entry(root, font="gisha 12", fg=TEXT, bg=BUTTONS, textvariable=dog_min, width=12)
entry2.grid(row=7, column=0, padx=20, pady=5)
dog_min.set("20000")
label3 = Label(root, font="gisha 12", fg=TEXT, bg=BACKGROUND, text="robot max size:", width=20)
label3.grid(row=8, column=0, padx=0, pady=0)
entry3 = Entry(root, font="gisha 12", fg=TEXT, bg=BUTTONS, textvariable=robot_max, width=12)
entry3.grid(row=9, column=0, padx=20, pady=5)
robot_max.set("9000")
label4 = Label(root, font="gisha 12", fg=TEXT, bg=BACKGROUND, text="robot min size:", width=20)
label4.grid(row=10, column=0, padx=0, pady=0)
entry4 = Entry(root, font="gisha 12", fg=TEXT, bg=BUTTONS, textvariable=robot_min, width=12)
entry4.grid(row=11, column=0, padx=20, pady=5)
robot_min.set("5000")
label4 = Label(root, font="gisha 12", fg=TEXT, bg=BACKGROUND, text="Press b for bounding box", width=20, anchor=W)
label4.grid(row=12, column=0, padx=5, pady=5)
label5 = Label(root, font="gisha 12", fg=TEXT, bg=BACKGROUND, text="Press t for trail", width=20, anchor=W)
label5.grid(row=13, column=0, padx=5, pady=5)
label6 = Label(root, font="gisha 12", fg=TEXT, bg=BACKGROUND, text="Press d for distance", width=20, anchor=W)
label6.grid(row=14, column=0, padx=5, pady=5)
label7 = Label(root, font="gisha 12", fg=TEXT, bg=BACKGROUND, text="Press space to pause/play", width=20, anchor=W)
label7.grid(row=15, column=0, padx=5, pady=5)
label8 = Label(root, font="gisha 12", fg=TEXT, bg=BACKGROUND, text="Press Esc to quit", width=20, anchor=W)
label8.grid(row=16, column=0, padx=5, pady=5)

root.mainloop()