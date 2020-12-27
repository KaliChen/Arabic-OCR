import tkinter as tk
#from tkinter.ttk import *
from tkinter import messagebox as tkmsg
from tkinter.ttk import Notebook
from tkinter import filedialog
from tkinter import ttk
import subprocess
#import glob
from ImgViewer.imgview import ImageViewer

import cv2 as cv
import os
import time
from tqdm import tqdm
from glob import glob
#from OCR import run, run2, model_name, predicted_Text 
from character_segmentation import segment
from segmentation import extract_words
from train import prepare_char, featurizer
import pickle
import matplotlib.pyplot as plt
import multiprocessing as mp

class ArabicOCR():    
    def __init__(self, master):
        self.parent = master
        self.imageFile = str()
        self.init_Model_tab()
        self.imgview = ImageViewer(self.parent)
        ImageConfig_Button = tk.Button(self.parent, text = "ImageConfig",font=('Courier', 8), command = self.image_config)
        ImageConfig_Button.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)        
        self.init_ArabicOCR()
        self.init_DisplaySceneMarkInfo_tab()


    def image_config(self, event = None):
        imageFile = self.imgview.image_paths[self.imgview.image_idx]
        self.imageFile = str(imageFile)
        self.DisplaySceneMarkInfo.insert(tk.END,self.imageFile)

    def Select_model(self, event = None):
        for item in self.Table_of_Model.selection():
            self.item_text = self.Table_of_Model.item(item, "values")
        tkmsg.showinfo("Information",self.item_text[0])
        print(self.item_text)
        print(self.item_text[0])
        self.DisplaySceneMarkInfo.insert(tk.END,self.item_text[0])

    def List_model(self, event = None):
        Modellist = glob( "models/*.[sS][aA][vV]" )           
        for sav in Modellist:
            (head, filename) = os.path.split(sav)
            self.Table_of_Model.insert("", index = 'end', text = filename,  values = (sav))

    def init_Model_tab(self):
        self.Model_tab = tk.Frame(self.parent)
        self.Model_tab.pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)

        ListModel = tk.Label(self.Model_tab)
        ListModel.pack(side=tk.TOP, expand=tk.NO)

        self.Table_of_Model = ttk.Treeview(ListModel,height = 3)
        self.Table_of_Model.heading("#0", text = "List of Model")#icon column
        #self.Table_of_font.heading("#1", text = "Path")
        self.Table_of_Model.column("#0", width = 500)#icon column
        #self.Table_of_font.column("#1", width = 90)
        self.Table_of_Model.tag_configure('T', font = 'Courier,4')
        self.Table_of_Model.bind("<Double-1>",self.Select_model)
        self.Table_of_Model.pack(side=tk.TOP, expand=tk.NO, fill=tk.BOTH)
        self.List_Model_Button = tk.Button(ListModel, text = "List Model",font=('Courier', 10), command = self.List_model)
        self.List_Model_Button.pack(side=tk.TOP, expand=tk.YES, fill = tk.BOTH) 

    def init_DisplaySceneMarkInfo_tab(self):
        self.DisplaySceneMarkInfo_Frame = tk.LabelFrame(self.parent, text="Display ArabicOCR Info", font=('Courier', 9))
        self.DisplaySceneMarkInfo_Frame .pack(side=tk.TOP, expand=tk.NO)
        self.DisplaySceneMarkInfo = tk.Text(self.DisplaySceneMarkInfo_Frame, width = 70, height = 7) 
        DisplaySceneMarkInfo_sbarV = tk.Scrollbar(self.DisplaySceneMarkInfo_Frame, orient=tk.VERTICAL)
        DisplaySceneMarkInfo_sbarH = tk.Scrollbar(self.DisplaySceneMarkInfo_Frame, orient=tk.HORIZONTAL)
        DisplaySceneMarkInfo_sbarV.config(command=self.DisplaySceneMarkInfo.yview)
        DisplaySceneMarkInfo_sbarH.config(command=self.DisplaySceneMarkInfo.xview)
        self.DisplaySceneMarkInfo.config(yscrollcommand=DisplaySceneMarkInfo_sbarV.set)
        self.DisplaySceneMarkInfo.config(xscrollcommand=DisplaySceneMarkInfo_sbarH.set)
        DisplaySceneMarkInfo_sbarV.pack(side=tk.RIGHT, fill=tk.Y)
        DisplaySceneMarkInfo_sbarH.pack(side=tk.BOTTOM, fill=tk.X)
        self.DisplaySceneMarkInfo.pack(side=tk.TOP, expand=tk.NO)
        DisplaySceneMarkInfoCLEAR =tk.Button(self.parent, text = "Clear",font=('Courier', 9), command = self.DisplaySceneMarkInfoCLEAR)
        DisplaySceneMarkInfoCLEAR.pack(side=tk.TOP, expand=tk.NO)

    def DisplaySceneMarkInfoCLEAR(self, event = None):
        self.DisplaySceneMarkInfo.delete('1.0', tk.END)
        tkmsg.showinfo("Information","CLEAR")

    def load_model(self):
        location = 'models'
        if os.path.exists(location):
            model = pickle.load(open(f'models/{model_name}', 'rb'))
            return model
        
    def run2(self, obj):
        word, line = obj
        model = load_model()
        # For each word in the image
        char_imgs = segment(line, word)
        txt_word = ''
        # For each character in the word
        for char_img in char_imgs:
            try:
                ready_char = prepare_char(char_img)
            except:
                # plt.imshow(word, 'gray')
                # plt.show()
                # breakpoint()
                continue
            feature_vector = featurizer(ready_char)
            predicted_char = model.predict([feature_vector])[0]
            #print(predicted_char)
            txt_word += predicted_char
        #print(txt_word)
        return txt_word


    def run(self, image_path):
        # Read test image
        full_image = cv.imread(image_path)
        predicted_text = ''

        # Start Timer
        before = time.time()
        words = extract_words(full_image)       # [ (word, its line),(word, its line),..  ]
        #print(words)
        pool = mp.Pool(mp.cpu_count())
        predicted_words = pool.map(self.run2, words)
        print("predicted_words: ")
        print(predicted_words)
        pool.close()
        pool.join()
        # Stop Timer
        after = time.time()

        # append in the total string.
        for word in predicted_words:
            print("word: "+word+"\n")
            predicted_text += word
        predicted_text += ' '
        print("predicted_text:\n")
        print(predicted_text)
        predicted_Text = str(predicted_text)
        exc_time = after-before
        # Create file with the same name of the image
        img_name = image_path.split('\\')[1].split('.')[0]
        # img_idx = int(img_name.split('_')[1])         # the valid one for testing day.
        img_idx = int(''.join(i for i in img_name if i.isdigit()))
        print("img_idx:\n")
        print(img_idx)
        with open(f'output/text/{img_name}.txt', 'w', encoding='utf8') as fo:
            fo.writelines(predicted_text)
    
        return (img_idx, exc_time)
        # with open('output/running_time.txt', 'a') as fo:
        #     fo.write(f'{img_idx}: {exc_time:.2f}s\n')


    def runArabicOCR(self, event = None):
        model_name = self.item_text[0]
        print(model_name)
        self.DisplaySceneMarkInfo.insert(tk.END,model_name)
        #Clear the old data in running_time.txt
        if not os.path.exists('output'):
            os.mkdir('output')
        open('output/running_time.txt', 'w').close()

        destination = 'output/text'
        if not os.path.exists(destination):
            os.makedirs(destination)
        """
        types = ['png', 'jpg']
        images_paths = []
        for t in types:
            images_paths.extend(glob(f'test/*.{t}'))
            #print(images_paths)
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
        """
        self.run(self.imageFile)
        print(self.imageFile)
        self.DisplaySceneMarkInfo.insert(tk.END,predicted_Text)
        print(predicted_Text)
    def init_ArabicOCR(self):
        self.ArabicOCR_tab = tk.Frame(self.parent)
        self.ArabicOCR_tab.pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)
        
        runArabicOCR_Button = tk.Button(self.ArabicOCR_tab, text = "run ArabicOCR",font=('Courier', 8), command = self.runArabicOCR)
        runArabicOCR_Button.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)


if __name__ == '__main__':
    root = tk.Tk()
    ArabicOCR(root)
    #root.resizable(width=True, height=True)
    #root.geometry(MAIN_DISPLAY_SIZE)
    root.mainloop()

   
