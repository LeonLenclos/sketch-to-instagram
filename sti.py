#!/usr/bin/env python3
# By Léon Lenclos (2018)

import os
import subprocess

import tkinter as tk
import tkinter.messagebox as mb

from InstagramAPI import InstagramAPI

STROKE_WEIGHT = 5
SIZE = 480, 480


class Sketch2Insta(tk.Tk):
    """
    Provide a simple way to draw something and share it on Instagram
    """

    def __init__(self, sketch_size=(SIZE)):
        """
        App initialization
        """

        super(Sketch2Insta, self).__init__()
        self.wm_title("Sketch To Instagram")
        self.fullscreen = False

        # Create canvas
        w, h = sketch_size
        self.canvas = tk.Canvas(self, width=w, height=h, background='white')
        self.canvas.pack()

        # Key events
        self.bind("<Escape>", self.close)
        self.bind("s", self.save)
        self.bind("r", self.reset)
        self.bind("i", self.insta)
        self.bind("h", self.help)
        self.bind("l", self.ask_for_login)
        self.bind("f", self.toogle_fullscreen)

        # Mouse events
        self.canvas.bind('<ButtonPress>', self.mouse_press)
        self.canvas.bind('<B1-Motion>', self.draw)

        self.InstagramAPI = None

    def toogle_fullscreen(self, event):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        self.focus_set()

    def close(self, event):
        self.quit()

    def help(self, event):
        mb.showinfo('Help', 'H is for Help\nF is for Fullscreen\nS is for Save a jpg of the sketch\nR is for Reset\nL is for Log in (in Instagram)\nI is for share on Instagram\nEnjoy.')


    def ask_for_login(self, event):

        def submit():
            if self.login(username.get(), password.get()):
                login_prompt.destroy()
                mb.showinfo('', 'Hello {}, you have been successfully logged.'.format(username.get()))
            else :
                tk.Label(login_prompt, text="Wrong username or password... Try again.").pack()
        def dont():
            login_prompt.destroy()

        login_prompt = tk.Toplevel(self)
        login_prompt.wm_title("login")

        username = tk.StringVar()
        password = tk.StringVar()

        tk.Label(login_prompt, text="If you want to use the 'share on Instagram' function, enter your Instagram login.").pack()
        nameEntry = tk.Entry(login_prompt, textvariable=username).pack()
        tk.Label(login_prompt, text="And your Instagram password...").pack()
        passEntry = tk.Entry(login_prompt, textvariable=password, show='x').pack()
        tk.Button(login_prompt, text='I do not want to use this function',command=dont).pack()
        tk.Button(login_prompt, text='log in',command=submit).pack()

    def login(self, insta_login, insta_password):
        self.InstagramAPI = InstagramAPI(insta_login, insta_password)
        return self.InstagramAPI.login()

    def mouse_press(self, event):
        self.prev = event

    def draw(self, event):
        self.canvas.create_line(
            self.prev.x,
            self.prev.y,
            event.x,
            event.y,
            width=STROKE_WEIGHT
        )
        self.prev = event

    def save(self, event):
        """Save current canvas to a jpg and return the saved file path"""
        file_name_format = "{:04d}.{}"
        i = 0
        while file_name_format.format(i, "jpg") in os.listdir(): i += 1
        path_ps = file_name_format.format(i, "ps")
        path_jpg = file_name_format.format(i, "jpg")
        self.canvas.postscript(file=path_ps)
        #TODO: use a magick python lib
        subprocess.call(["convert", path_ps, path_jpg])
        subprocess.call(["rm", path_ps])
        print("saving : {}".format(path_jpg))
        return path_jpg

    def insta(self, event):
        if self.InstagramAPI:
            photo_path = self.save(event)
            caption = ""
            self.InstagramAPI.uploadPhoto(photo_path, caption=caption)
            print("posting on instagram")
            mb.showinfo('Hooray !', 'Sketch shared on Instagram !')

        else :
            mb.showinfo('Oops...', 'If you want to share this sketch on Instagram, You have to log in first.')

    def reset(self, event):
        self.canvas.delete("all")

root=Sketch2Insta()
root.mainloop()
