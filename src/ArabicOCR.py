import tkinter as tk
from tkinter.ttk import *
from tkinter import messagebox as msg
from tkinter.ttk import Notebook
from tkinter import filedialog
from tkinter import ttk

import tkinter.messagebox as tkmsg
from PIL import Image, ImageTk, ImageDraw, ExifTags, ImageColor,ImageFont

from glob import glob
import os
#import ffmpeg
#from os.path import splitext
import platform
import ImgViewer.ImgViewer.imgview as IV #(1)

from OCR import model_name, load_model, run2, run, OCR_main

#from character_segmentation import binarize,fill,baseline_detection, horizontal_transitions, vertical_transitions, cut_points, check_baseline, inside_hole, check_hole, remove_dots, check_dots, check_stroke, filter_regions, post, extract_char, segment

class ArabicOCR(tk.Tk):
    CANVAS_WIDTH = 530
    CANVAS_HEIGHT = 360
    def __init__(self):
        super().__init__()

        self.title("Test Tool Platform:"+str(platform.system()))        

        w = 1200 # width for the Tk root
        h = 900 # height for the Tk root

        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # set the dimensions of the screen 
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        #self.geometry("1440x1020")

        '''self.notebook'''
        self.notebook = Notebook(self)
        self.notebook.pack(side = tk.TOP,fill=tk.BOTH, expand=tk.YES)

        self.init_ImgViewer()
        #self.init_Model_tab()
        #self.init_DisplaySceneMarkInfo_tab()
        self.init_ArabicOCR()
        
    def init_ImgViewer(self):
        self.init_ImgViewer_tab = tk.Frame(self.notebook)
        self.init_ImgViewer_tab.pack(side = tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.notebook.add(self.init_ImgViewer_tab, text="init_ImgViewer")
        self.ImgSwitch = tk.StringVar()
        ivfram1 = tk.Frame(self.init_ImgViewer_tab )
        ivfram1.grid(row =0, column = 0, sticky = tk.E+tk.W)
        self.iv1 = IV.ImageViewer(ivfram1)
        ivfram1_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram1_2.grid(row =0, column = 1, sticky = tk.E+tk.W)        
        opendir1 = tk.Button(ivfram1_2, text = "Open\n dir 1",font=('Courier', 9), command = self.iv1.open_dir)
        opendir1.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
        switch1 = tk.Radiobutton(ivfram1_2, text = "Img\n Switch 1",font=('Courier', 9), variable = self.ImgSwitch, value = "Img Switch 1", command = self.imgswitch)
        switch1.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)

        ivfram3 = tk.Frame(self.init_ImgViewer_tab )
        ivfram3.grid(row =0, column = 2, sticky = tk.E+tk.W)
        self.iv3 = IV.ImageViewer(ivfram3)
        ivfram3_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram3_2.grid(row =0, column = 3, sticky = tk.E+tk.W)        

        opendir3 = tk.Button(ivfram3_2, text = "Open\n dir 3",font=('Courier', 9), command = self.iv3.open_dir)
        opendir3.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)
        switch3 = tk.Radiobutton(ivfram3_2, text = "Img\n Switch 3",font=('Courier', 9), variable = self.ImgSwitch, value = "Img Switch 3", command = self.imgswitch)
        switch3.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)

        ivfram2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram2.grid(row =1, column = 0, sticky = tk.E+tk.W)
        self.iv2 = IV.ImageViewer(ivfram2)
        ivfram2_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram2_2.grid(row =1, column = 1, sticky = tk.E+tk.W)        
        
        opendir2 = tk.Button(ivfram2_2, text = "Open\n dir 2",font=('Courier', 9), command = self.iv2.open_dir)
        opendir2.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
        switch2 = tk.Radiobutton(ivfram2_2, text = "Img\n Switch 2",font=('Courier', 9), variable = self.ImgSwitch, value = "Img Switch 2", command = self.imgswitch)
        switch2.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
  
        ivfram4 = tk.Frame(self.init_ImgViewer_tab )
        ivfram4.grid(row =1, column = 2, sticky = tk.E+tk.W)
        self.iv4 = IV.ImageViewer(ivfram4)
        ivfram4_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram4_2.grid(row =1, column = 3, sticky = tk.E+tk.W)        

        opendir1 = tk.Button(ivfram4_2, text = "Open\n dir 4",font=('Courier', 9), command = self.iv4.open_dir)
        opendir1.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
        switch4 = tk.Radiobutton(ivfram4_2, text = "Img\n Switch 4",font=('Courier', 9), variable = self.ImgSwitch, value = "Img switch 4", command = self.imgswitch)
        switch4.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)

    def imgswitch(self):
        if self.ImgSwitch.get() =="Img Switch 1": imageFile = self.iv1.image_paths[self.iv1.image_idx]
        elif self.ImgSwitch.get() =="Img Switch 2": imageFile = self.iv2.image_paths[self.iv2.image_idx]
        elif self.ImgSwitch.get() =="Img Switch 3": imageFile = self.iv3.image_paths[self.iv3.image_idx]
        elif self.ImgSwitch.get() =="Img Switch 4": imageFile = self.iv4.image_paths[self.iv4.image_idx]
        """
        self.awsrk.imageFile = imageFile
        self.alpr.imageFile = imageFile
        self.iss.imageFile = imageFile
        self.haar.imageFile = imageFile
        self.DlibImg.imageFile = imageFile
        self.ocrtess.imageFile = imageFile
        self.clrP.imageFile = imageFile
        """
    def init_Model_tab(self):
        self.Model_tab = tk.Frame(self.notebook)
        self.notebook.add(self.Model_tab, text="Model_tab")
        
        #self.Model_tab = tk.Frame(self.parent)
        #self.Model_tab.pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)

        ListModel = tk.Label(self.Model_tab)
        ListModel.pack(side=tk.TOP, expand=tk.NO)

        self.Table_of_Model = ttk.Treeview(ListModel,height = 3)
        self.Table_of_Model.heading("#0", text = "List of Model")#icon column
        #self.Table_of_font.heading("#1", text = "Path")
        self.Table_of_Model.column("#0", width = 500)#icon column
        #self.Table_of_font.column("#1", width = 90)
        self.Table_of_Model.tag_configure('T', font = 'Courier,4')
        self.Table_of_Model.bind("<Double-1>",self.Select_model)
        #self.Table_of_Model.bind("<Double-1>",self.Load_model)
        self.Table_of_Model.pack(side=tk.TOP, expand=tk.NO, fill=tk.BOTH)
        self.List_Model_Button = tk.Button(ListModel, text = "List Model",font=('Courier', 10), command = self.List_model)
        self.List_Model_Button.pack(side=tk.TOP, expand=tk.YES, fill = tk.BOTH) 
    def Select_model(self, event = None):
        for item in self.Table_of_Model.selection():
            self.item_text = self.Table_of_Model.item(item, "values")
        tkmsg.showinfo("Information",self.item_text[0])
        self.Load_model()
        
        print("self.item_text")
        print(self.item_text)
        print("self.item_text[0]")
        print(self.item_text[0])
        
        ##self.DisplaySceneMarkInfo.insert(tk.END,self.item_text[0])

        
    def List_model(self, event = None):
        Modellist = glob( "models/*.[sS][aA][vV]" )           
        for sav in Modellist:
            (head, filename) = os.path.split(sav)
            self.Table_of_Model.insert("", index = 'end', text = filename,  values = (sav))

    def init_DisplaySceneMarkInfo_tab(self):
        self.DisplaySceneMarkInfo_tab = tk.Frame(self.notebook)
        self.notebook.add(self.DisplaySceneMarkInfo_tab, text="DisplaySceneMarkInfo")
        self.DisplaySceneMarkInfo_Frame = tk.LabelFrame(self.DisplaySceneMarkInfo_tab, text="Display ArabicOCR Info", font=('Courier', 9))
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
        DisplaySceneMarkInfoCLEAR =tk.Button(self.DisplaySceneMarkInfo_tab, text = "Clear",font=('Courier', 9), command = self.DisplaySceneMarkInfoCLEAR)
        DisplaySceneMarkInfoCLEAR.pack(side=tk.TOP, expand=tk.NO) 

    def DisplaySceneMarkInfoCLEAR(self, event = None):
        self.DisplaySceneMarkInfo.delete('1.0', tk.END)
        tkmsg.showinfo("Information","CLEAR")

    def runOCR_main(event = None):
        #model_name = '1L_NN.sav'
        
        OCR_main()
        
    def init_ArabicOCR(self):
        self.ArabicOCR_tab = tk.Frame(self.notebook)
        self.notebook.add(self.ArabicOCR_tab, text="init_ArabicOCR")
        #self.ArabicOCR_tab.pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)
        
        runArabicOCR_Button = tk.Button(self.ArabicOCR_tab, text = "run ArabicOCR",font=('Courier', 8), command = self.runOCR_main)
        runArabicOCR_Button.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)

        self.Model_tab = tk.Frame(self.ArabicOCR_tab)
        self.Model_tab.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)
        #self.Model_tab = tk.Frame(self.parent)
        #self.Model_tab.pack(side = tk.TOP, expand=tk.YES, fill=tk.BOTH)

        ListModel = tk.Label(self.Model_tab)
        ListModel.pack(side=tk.TOP, expand=tk.NO,fill = tk.X)

        self.Table_of_Model = ttk.Treeview(ListModel,height = 3)
        self.Table_of_Model.heading("#0", text = "List of Model")#icon column
        #self.Table_of_font.heading("#1", text = "Path")
        self.Table_of_Model.column("#0", width = 500)#icon column
        #self.Table_of_font.column("#1", width = 90)
        self.Table_of_Model.tag_configure('T', font = 'Courier,4')
        self.Table_of_Model.bind("<Double-1>",self.Select_model)
        #self.Table_of_Model.bind("<Double-1>",self.Load_model)
        self.Table_of_Model.pack(side=tk.TOP, expand=tk.NO, fill=tk.BOTH)
        self.List_Model_Button = tk.Button(ListModel, text = "List Model",font=('Courier', 10), command = self.List_model)
        self.List_Model_Button.pack(side=tk.TOP, expand=tk.YES, fill = tk.BOTH)

        self.DisplaySceneMarkInfo_tab = tk.Frame(self.ArabicOCR_tab)
        #self.notebook.add(self.DisplaySceneMarkInfo_tab, text="DisplaySceneMarkInfo")
        self.DisplaySceneMarkInfo_tab.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)
        self.DisplaySceneMarkInfo_Frame = tk.LabelFrame(self.DisplaySceneMarkInfo_tab, text="Display ArabicOCR Info", font=('Courier', 9))
        self.DisplaySceneMarkInfo_Frame .pack(side=tk.TOP, expand=tk.NO, fill = tk.X)
        self.DisplaySceneMarkInfo = tk.Text(self.DisplaySceneMarkInfo_Frame, width = 70, height = 7) 
        DisplaySceneMarkInfo_sbarV = tk.Scrollbar(self.DisplaySceneMarkInfo_Frame, orient=tk.VERTICAL)
        DisplaySceneMarkInfo_sbarH = tk.Scrollbar(self.DisplaySceneMarkInfo_Frame, orient=tk.HORIZONTAL)
        DisplaySceneMarkInfo_sbarV.config(command=self.DisplaySceneMarkInfo.yview)
        DisplaySceneMarkInfo_sbarH.config(command=self.DisplaySceneMarkInfo.xview)
        self.DisplaySceneMarkInfo.config(yscrollcommand=DisplaySceneMarkInfo_sbarV.set)
        self.DisplaySceneMarkInfo.config(xscrollcommand=DisplaySceneMarkInfo_sbarH.set)
        DisplaySceneMarkInfo_sbarV.pack(side=tk.RIGHT, fill=tk.Y)
        DisplaySceneMarkInfo_sbarH.pack(side=tk.BOTTOM, fill=tk.X)
        self.DisplaySceneMarkInfo.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)
        DisplaySceneMarkInfoCLEAR =tk.Button(self.DisplaySceneMarkInfo_tab, text = "Clear",font=('Courier', 9), command = self.DisplaySceneMarkInfoCLEAR)
        DisplaySceneMarkInfoCLEAR.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)   
                # image frame
        self.iframe = tk.Frame(self.ArabicOCR_tab)
        self.iframe.pack()
        self.image_canvas = tk.Canvas(self.iframe, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,cursor='plus')
        image_Canvas_sbarV = tk.Scrollbar(self.iframe, orient=tk.VERTICAL)
        image_Canvas_sbarH = tk.Scrollbar(self.iframe, orient=tk.HORIZONTAL)
        image_Canvas_sbarV.config(command=self.image_canvas.yview)
        image_Canvas_sbarH.config(command=self.image_canvas.xview)
        self.image_canvas.config(yscrollcommand=image_Canvas_sbarV.set)
        self.image_canvas.config(xscrollcommand=image_Canvas_sbarH.set)
        image_Canvas_sbarV.pack(side=tk.RIGHT, fill=tk.Y)
        image_Canvas_sbarH.pack(side=tk.BOTTOM, fill=tk.X)
        self.image_canvas.pack(pady=0, anchor=tk.N, fill = tk.X)      

if __name__ == "__main__":
    
    TT = ArabicOCR()
    TT.mainloop()


