from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import cv2
import os 

BACKGROUND = '#f5f5f5'
BUTTONS = '#ffffff'
TEXT = '#D54A37'

def load_video():
    """ callback function """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    #video_fn = askopenfilename(initialdir=r'C:\Users\student\Documents\GitHub\K9andFriends\videos')
    video_fn = askopenfilename(initialdir=dir_path)

def do_test():
    """ callback function """
    training_msg.set("")
    res_path = test.run_testing(test_img_path.get(), output_dir.get(), float(thresh.get()))
    """res = PIL.Image.open(res_path)
    res = PIL.ImageTk.PhotoImage(res)
    # image = Label(canvas, image=res, anchor=CENTER)
    image.configure(image=res)
    image.image = res
    image.grid(row=2, column=2, columnspan=3, rowspan=12)
    """

def add_training_set():
    """ callback function """
    training_msg.set("")
    new_training_set_path.set(askdirectory())
    train.add_training_set(new_training_set_path.get())

def set_image_path():
    """ callback function """
    training_msg.set("")
    test_img_path.set(askopenfilename())

def set_output_dir():
    """ callback function """
    training_msg.set("")
    output_dir.set(askdirectory())

root = Tk()
root.title("K9 and Robot! :)")
root.configure(background=BACKGROUND)
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

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
headline = Label(root, font="Gisha 20 bold", bg=BACKGROUND, fg=TEXT, text="K9 and Robot! :)", anchor=CENTER)
headline.grid(row=0, column=0, columnspan=7, padx=10, pady=10)

# Left input and output settings
btn1 = Button(root, font="Gisha 12", fg=BUTTONS, bg=TEXT, command=load_video, text="load video", width=12)
btn1.grid(row=1, column=0, padx=15, pady=0)
btn2 = Button(root, font="Gisha 12", fg=BUTTONS, bg=TEXT, command=do_test, text="play", width=12)
btn2.grid(row=2, column=0, padx=15, pady=0)
btn3 = Button(root, font="Gisha 12", fg=BUTTONS, bg=TEXT, command=add_training_set, text="pause", width=12)
btn3.grid(row=3, column=0, padx=15, pady=0)
btn4 = Checkbutton(root, font="Gisha 12", fg=TEXT, bg=BACKGROUND, variable=paths, text="show paths", width=10)
btn4.grid(row=4, column=0, padx=15, pady=0)
btn5 = Checkbutton(root, font="Gisha 12", fg=TEXT, bg=BACKGROUND, variable=boxes, text="show boxes", width=10)
btn5.grid(row=5, column=0, padx=15, pady=0)
btn6 = Checkbutton(root, font="Gisha 12", fg=TEXT, bg=BACKGROUND, variable=distance, text="show distance", width=10)
btn6.grid(row=6, column=0, padx=15, pady=0)

# Main frame for showing results
canvas = Canvas(bg=BUTTONS, bd=5, width=0.75*w, height=0.75*h).grid(row=1, column=1, columnspan=5, rowspan=22, sticky=E)
image = Label(canvas, image="", anchor=CENTER)

# Right parameter settings
label1 = Label(root, font="Gisha 12", fg=TEXT, bg=BACKGROUND, text="dog max size:", width=15)
label1.grid(row=1, column=6, padx=0, pady=0)
entry1 = Entry(root, font="gisha 12", fg=TEXT, bg=BUTTONS, textvariable=dog_max, width=12)
entry1.grid(row=2, column=6, padx=15, pady=0)
dog_max.set("9")
label2 = Label(root, font="gisha 12", fg=TEXT, bg=BACKGROUND, text="dog min size:", width=15)
label2.grid(row=3, column=6, padx=0, pady=0)
entry2 = Entry(root, font="gisha 12", fg=TEXT, bg=BUTTONS, textvariable=dog_min, width=12)
entry2.grid(row=4, column=6, padx=15, pady=0)
dog_min.set("9")
label3 = Label(root, font="gisha 12", fg=TEXT, bg=BACKGROUND, text="robot max size:", width=15)
label3.grid(row=5, column=6, padx=0, pady=0)
entry3 = Entry(root, font="gisha 12", fg=TEXT, bg=BUTTONS, textvariable=robot_max, width=12)
entry3.grid(row=6, column=6, padx=15, pady=0)
robot_max.set("9")
label4 = Label(root, font="gisha 12", fg=TEXT, bg=BACKGROUND, text="robot min size:", width=15)
label4.grid(row=7, column=6, padx=0, pady=0)
entry4 = Entry(root, font="gisha 12", fg=TEXT, bg=BUTTONS, textvariable=robot_min, width=12)
entry4.grid(row=8, column=6, padx=15, pady=0)
robot_min.set("9")
root.mainloop()