from Tkinter import *
from PIL import Image, ImageTk
from preprocessor import process
from collector import capture
import numpy as np
import pickle
import random
import glob
import os
#from Tkinter import Tk, Label, Button

width = 2560
height = 1600

logo_size = 120
image_size = 275

primary_color = "#990140"
secondary_color = "#4D002A"

class Interface:
    def __init__(self, master):

        self.master = master

        master.geometry(str(width) + "x" + str(height))
        master.title("Neural Network Game")

        self.num_of_tries = 0

        self.load()

        ### FRAMES

        self.topframe = Frame(master, bg=primary_color, borderwidth = 1, relief="solid")
        self.topframe.pack(side=TOP, fill=BOTH)

        self.leftframe = Frame(master, bg=secondary_color, borderwidth = 1, relief="solid", padx=50)
        self.leftframe.pack(side=LEFT, fill=Y)

        self.rightframe = Frame(master, bg=secondary_color, borderwidth = 1, relief="solid")
        self.rightframe.pack(side=RIGHT, fill=BOTH, expand=True)

        ### TOP FRAME
        """
        self.oeop_logo = Canvas(self.topframe, width=logo_size, height=logo_size)
        self.oeop_logo.pack(side=LEFT)
        #        self.crop_img.place()
        self.oeop_logo.create_image(0, 0, image=oeop_img, anchor=NW)
            #self.oeop_logo.place(x=5)
        """
        self.title = Label(self.topframe, bg=primary_color,fg="white", text="Neural Network Game", padx=40, pady=20, font=("Helvetica", 100, "bold"))
        self.title.pack()



        self.mostec_logo = Canvas(self.topframe, width=logo_size, height=logo_size)
        #self.mostec_logo.pack()
        #        self.crop_img.place()
        self.mostec_logo.create_image(0, 0, image=self.mostec_img, anchor=NW)
        self.mostec_logo.place(relx=.9, y=15)

        self.acknowledgements = Label(self.topframe, justify=LEFT, bg=primary_color, fg="white", text="By Julian Yocum and Jenisa Nguyen", font=("Helvetica", 20))
        #self.acknowledgements.pack(side=BOTTOM)
        self.acknowledgements.place(rely=.78, relx=.5)

        ### LEFT FRAME

        self.leftgroup1 = Frame(self.leftframe, bg=primary_color, padx=10, pady=10,
                highlightbackground=secondary_color, highlightthickness=15, relief="flat")
        self.leftgroup1.pack()

        self.image_label = Label(self.leftgroup1, fg="white", bg=primary_color,text="Raw Image from Camera",
            font=("Helvetica", 18))
        self.image_label.pack()

        self.crop_img = Canvas(self.leftgroup1, width=image_size, height=image_size, highlightthickness=0)
        self.crop_img.pack()
        #self.crop_img.create_image(0, 0, image=crop_png, anchor=NW)
        self.crop_img.create_rectangle(0, 0, image_size, image_size, fill="black")

        self.leftgroup2 = Frame(self.leftframe, bg=primary_color, padx=10, pady=10,
            highlightbackground=secondary_color, highlightthickness=15, relief="flat")
        self.leftgroup2.pack()

        self.image_label = Label(self.leftgroup2, fg="white", bg=primary_color,text="Image before entering Network", font=("Helvetica", 18))
        self.image_label.pack()

        self.process_img = Canvas(self.leftgroup2, width=image_size, height=image_size, highlightthickness=0)
        self.process_img.pack()
        #self.process_img.create_image(0, 0, image=process_png, anchor=NW)
        self.process_img.create_rectangle(0, 0, image_size, image_size, fill="black")

        ### RIGHT FRAME

        self.rightgroup = Frame(self.rightframe, bg=primary_color, width=950, padx=30, pady=30,
            highlightbackground=secondary_color, highlightthickness=40, relief="flat")
        self.rightgroup.pack(fill=Y, expand=True)
        self.rightgroup.pack_propagate(0)

        self.congrats = Label(self.rightgroup, fg="white",wraplength=800, bg=primary_color,text="Congratulations!", font=("Helvetica", 90))

        self.message = Label(self.rightgroup, fg="white",wraplength=800, bg=primary_color,text="Welcome to the Neural Network Guessing Game!", font=("Helvetica", 60))
        self.message.place(anchor="center", relx=.5, rely=.42)

            # First screen
        self.start_button = Button(self.rightgroup, fg="white", width=8, height=2, highlightbackground=primary_color, relief=FLAT, text="Start!", font=("Helvetica", 30), command=self.start)
        self.start_button.place(anchor="center", relx=.5, rely=.75)

            # Second screen
        self.done_button = Button(self.rightgroup, fg="white", width=8, height=2, highlightbackground=primary_color, relief=FLAT, text="Done!", font=("Helvetica", 25), command=self.done)

        self.restart_button = Button(self.rightgroup,fg="white", width=8, height=2, highlightbackground=primary_color,text="Restart", font=("Helvetica", 25), command=self.restart)

            # Third screen
        self.right_button = Button(self.rightgroup, fg="white", width=8, height=2, highlightbackground=primary_color, relief=FLAT, text="That's it!", font=("Helvetica", 25), command=self.right_num)

        self.wrong_button = Button(self.rightgroup,fg="white", width=8, height=2, highlightbackground=primary_color,text="Not it!", font=("Helvetica", 25), command=self.wrong_num)

            # Last screen
        self.playagain_button = Button(self.rightgroup,fg="white", width=10, height=2, highlightbackground=primary_color,text="Play Again!", font=("Helvetica", 30), command=self.restart)

    def load(self):
        img0 = Image.open("../data/logos/MOSTEClogo.jpg").resize((logo_size,logo_size))
        self.mostec_img = ImageTk.PhotoImage(img0)

        img1 = Image.open("../data/logos/OEOPlogo.jpeg").resize((logo_size,logo_size))
        self.oeop_img = ImageTk.PhotoImage(img1)

        with open('../data/network.pkl', 'rb') as network_data:
            self.network = pickle.load(network_data)

        self.rand_num = random.randint(0,9)

    def start(self):
        #self.welcome.lower(self.rightgroup)
        #self.greet_button.pack()
        #self.close_button.pack()

        self.message["text"] = "I have a number from 0 to 9. Please write down your guess and hit \"done\""

        self.start_button.place_forget()
        self.done_button.place(anchor="center", relx=.35, rely=.75)
        self.restart_button.place(anchor="center", relx=.65, rely=.75)

        self.master.update()

    def done(self):
        network_img = process(capture())

        # get images
        img0 = Image.open("../data/img_process/crop.png").resize((image_size,image_size))
        crop_png = ImageTk.PhotoImage(img0)

        img1 = Image.open("../data/img_process/process.png").resize((image_size,image_size))
        process_png = ImageTk.PhotoImage(img1)

        # display images
        self.update_images(crop_png,process_png)

        # get number from neural network
        pixel_array = np.array(network_img, dtype="float32")
        pixel_array = np.append([], pixel_array)
        pixel_array = np.array([[x/255] for x in pixel_array])

        last_row = self.network.feedforward(pixel_array)

        self.user_num = last_row.argmax()

        self.check()


    def check(self):
        self.done_button.place_forget()
        self.restart_button.place_forget()
        self.message["text"] = "Your number is a " + str(self.user_num) + "!"
        self.right_button.place(anchor="center", relx=.35, rely=.75)
        self.wrong_button.place(anchor="center", relx=.65, rely=.75)
        self.master.update()

    def right_num(self):
        self.num_of_tries += 1

        if self.user_num == self.rand_num:
            self.end()
        else:
            # compare numbers
            if self.user_num < self.rand_num:
                self.message["text"] = "Too Small, Guess Again!"
            elif self.user_num > self.rand_num:
                self.message["text"] = "Too Big, Guess Again!"

            self.right_button.place_forget()
            self.wrong_button.place_forget()
            self.done_button.place(anchor="center", relx=.35, rely=.75)
            self.restart_button.place(anchor="center", relx=.65, rely=.75)
            self.master.update()


    def wrong_num(self):
        self.message["text"] = "Sorry about that,\nI'm still learning! Try Again"

        print "Moving image to data/img_fail/..."

        fl = glob.glob('../data/img_stream/*.jpg')
        last_file = max(fl, key=os.path.getctime)

        im = Image.open(last_file)
        im.save("../data/img_fail/" + os.path.basename(last_file))

        self.right_button.place_forget()
        self.wrong_button.place_forget()
        self.done_button.place(anchor="center", relx=.35, rely=.75)
        self.restart_button.place(anchor="center", relx=.65, rely=.75)
        self.master.update()


    def end(self):
        self.message["text"] = "You won in " + str(self.num_of_tries) + " tries!"
        self.congrats.place(anchor="center", relx=.5, rely=.26)

        self.right_button.place_forget()
        self.wrong_button.place_forget()
        self.playagain_button.place(anchor="center", relx=.5, rely=.75)

        self.master.update()



    def restart(self):
        self.rand_num = random.randint(0,9)
        self.num_of_tries = 0

        self.message["text"] = "Welcome to the Neural Network Guessing Game!"

        self.start_button.place(anchor="center", relx=.5, rely=.75)
        self.done_button.place_forget()
        self.restart_button.place_forget()
        self.right_button.place_forget()
        self.wrong_button.place_forget()
        self.playagain_button.place_forget()
        self.congrats.place_forget()

        self.master.update()

    def update_images(self, crop, process):
        self.crop_img.delete("all")
        self.process_img.delete("all")
        self.crop_img.create_image(0, 0, image=crop, anchor=NW)
        self.process_img.create_image(0, 0, image=process, anchor=NW)
        self.crop_img.image = crop
        self.process_img.image = process

        self.master.update()




if __name__ == "__main__":
    root = Tk()

    # might take out later
    img2 = Image.open("test/process.png").resize((image_size,image_size))
    process_png = ImageTk.PhotoImage(img2)


    img3 = Image.open("test/crop.png").resize((image_size,image_size))
    crop_png = ImageTk.PhotoImage(img3)

    my_gui = Interface(root)

    root.mainloop()

