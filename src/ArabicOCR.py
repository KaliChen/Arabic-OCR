import tkinter as tk
#from tkinter.ttk import *
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from tkinter import filedialog
from tkinter import ttk
import subprocess

from OCR import run, run2
#from character_segmentation import segment
#from segmentation import extract_words
#from train import prepare_char, featurizer

import cv2 as cv
import os
import time
from tqdm import tqdm
from glob import glob

import pickle
import matplotlib.pyplot as plt
import multiprocessing as mp

class ArabicOCR():    
    def __init__(self, master):
        self.parent = master
        self.model_Path = tk.StringVar()
        self.Imgfolder_Path = tk.StringVar()
        self.saveText_Path =  tk.StringVar()
        self.init_ArabicOCR()
    def loadmodel(self, event = None):
        self.model_Path.set(filedialog.askopenfilename(initialdir = "/",
                                                        title = "Select file",
                                                        filetypes = (("txt files","*.sav"),
                                                                     ("all files","*.*"))) )

    def loadImgfolder(self, event = None):
        self.Imgfolder_Path.set(filedialog.askdirectory(initialdir = "/", 
                                                        title = "Select a folder"))
    def saveTxt(self, event = None):
        self.saveText_Path.set(filedialog.asksaveasfile(filetypes=[("Synth presets",
                                                                 "*.txt")]))

    def runArabicOCR(self, event = None):
        #Clear the old data in running_time.txt
        if not os.path.exists('output'):
            os.mkdir('output')
        open('output/running_time.txt', 'w').close()

        destination = 'output/text'
        if not os.path.exists(destination):
            os.makedirs(destination)
    
        types = ['png', 'jpg']
        images_paths = []
        for t in types:
            images_paths.extend(glob(f'test/*.{t}'))
        before = time.time()

        running_time = []

        for images_path in tqdm(images_paths,total=len(images_paths)):
            running_time.append(run(images_path))

        running_time.sort()
        with open('output/running_time.txt', 'w') as r:
            for t in running_time:
                r.writelines(f'image#{t[0]}: {t[1]}\n')       
        after = time.time()
        print(f'total time to finish {len(images_paths)} images:')
        print(after - before)
        
    def init_ArabicOCR(self):
        self.ArabicOCR_tab = tk.Frame(self.parent)
        self.ArabicOCR_tab.pack(side = tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        loadModel_Button = tk.Button(self.ArabicOCR_tab, text = "Load Model",font=('Courier', 8), command = self.loadmodel)
        loadModel_Button.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)

        self.ModelPath = tk.Entry(self.ArabicOCR_tab,font=('Courier', 8), textvariable = self.model_Path)
        self.ModelPath.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)
        
        loadImgfolder_Button = tk.Button(self.ArabicOCR_tab,
                                         text = "Load Image Folder",
                                         font=('Courier', 8), command = self.loadImgfolder)
        loadImgfolder_Button.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)

        self.ImagefolderPath = tk.Entry(self.ArabicOCR_tab,font=('Courier', 8), textvariable = self.Imgfolder_Path)
        self.ImagefolderPath.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)

        
        
        runArabicOCR_Button = tk.Button(self.ArabicOCR_tab, text = "run ArabicOCR",font=('Courier', 8), command = self.runArabicOCR)
        runArabicOCR_Button.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)


if __name__ == '__main__':
    root = tk.Tk()
    ArabicOCR(root)
    #root.resizable(width=True, height=True)
    #root.geometry(MAIN_DISPLAY_SIZE)
    root.mainloop()

   
