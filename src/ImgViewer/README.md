![https://ithelp.ithome.com.tw/upload/images/20200923/20119608C3lwW3TMeg.png](https://ithelp.ithome.com.tw/upload/images/20200923/20119608C3lwW3TMeg.png)

做一個類別class ImageViewer()並初始化:

```
    def __init__(self, master):
        self.parent = master
```

上一頁和下一頁的功能和左右鍵綁定再一起:

```
        self.parent.bind("<Left>", self.prev)
        self.parent.bind("<Right>", self.next)
```

執行init_imageviewerUI部分

```
        self.init_imageviewer()
```
定義init_imageviewerUI部分

```
    def init_imageviewer(self):
        self.image_paths = list() # image abs_paths
        # 目錄
        self.root_dir = None
        self.image_dir = None
        self.image_tk = None # showing tkimage
        self.image_idx = 0 # current image idex
        self.image_cnt = 0 # num of image
        self.image_cur_id = None # showing tkimage id
        # 主面板
        self.mframe = tk.Frame(self.parent)
        self.mframe.pack(fill=tk.BOTH, expand=1)
        # 圖像面板
        self.iframe = tk.Frame(self.mframe)
        self.iframe.pack()
        self.image_canvas = tk.Canvas(self.iframe,
                                      width=self.CANVAS_WIDTH, 
                                      height=self.CANVAS_HEIGHT,
                                      cursor='plus')
        #y-move
        image_Canvas_sbarV = tk.Scrollbar(self.iframe, orient=tk.VERTICAL)
        #x-move
        image_Canvas_sbarH = tk.Scrollbar(self.iframe, orient=tk.HORIZONTAL)
        image_Canvas_sbarV.config(command=self.image_canvas.yview)
        image_Canvas_sbarH.config(command=self.image_canvas.xview)
        self.image_canvas.config(yscrollcommand=image_Canvas_sbarV.set)
        self.image_canvas.config(xscrollcommand=image_Canvas_sbarH.set)
        image_Canvas_sbarV.pack(side=tk.RIGHT, fill=tk.Y)
        image_Canvas_sbarH.pack(side=tk.BOTTOM, fill=tk.X)
        # 圖像面板收尾
        self.image_canvas.pack(pady=0, anchor=tk.N)
        # 控制面板
        self.cframe = tk.Frame(self.mframe)
        self.cframe.pack(side=tk.TOP, padx=5, pady=10)
        self.prev_button = ttk.Button(self.cframe, 
                                      text="<<", 
                                      width=10, 
                                      command=self.prev)
        self.prev_button.pack(side = tk.LEFT, padx=5)
        self.next_button = ttk.Button(self.cframe,
                                      text=">>",
                                      width=10,
                                      command=self.next)
        self.next_button.pack(side = tk.LEFT, padx=5)
        # 狀態面板
        self.sframe = tk.Frame(self.mframe)
        self.sframe.pack(side=tk.TOP, padx=5, pady=10)
        self.status_label = ttk.Label(self.sframe,
                                     text="{:3d}/{:3d}".format(0,0),
                                     width=10,
                                     anchor=tk.CENTER)
        self.status_label.pack(side = tk.LEFT, padx=5)
```
上一張功能
```
    def prev(self, event=None):
        if self.image_cnt == 0:
            return
        if 0 < self.image_idx:
            self.image_idx -= 1
            #3.9)
            self.show_image(self.image_idx)
```
下一張功能
```
    def next(self, event=None):
        if self.image_cnt == 0:
            return
        if self.image_idx < (self.image_cnt-1):
            self.image_idx += 1
            #3.9)
            self.show_image(self.image_idx)
```
更新圖片狀態
```
    def update_imagestatus(self):
        if self.image_cnt != 0:
            self.status_label.configure(text="{:3d}/{:3d}".format(self.image_idx+1,self.image_cnt))
        else:
            self.status_label.configure(text="{:3d}/{:3d}".format(0,0))
```
顯示圖片
```
    def show_image(self, idx):
        if idx < 0 or idx >= self.image_cnt:
            raise ValueError("imageidx invalid")
        image_cv = cv2.imread(self.image_paths[idx],cv2.IMREAD_UNCHANGED )
        image_cv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_cv)
        self.image_tk = ImageTk.PhotoImage(image_pil)
        w, h = image_pil.size
        self.image_canvas.config(scrollregion=(0,0,w,h))
        disp_x = disp_y = 0
        self.image_cur_id = self.image_canvas.create_image(disp_x, disp_y,
                                                           image=self.image_tk,
                                                           anchor=tk.NW)
        self.update_imagestatus()
```
打開圖片資料夾功能
```
    def open_dir(self):
        self.root_dir = tkfd.askdirectory()
        self.image_dir = self.root_dir
        if self.image_dir == "":
            return
        if not os.path.exists(self.image_dir):
            tkmsg.showwarning("Warning", message="{} doesn't exist.".format(self.image_dir))
            return
        if not os.path.isdir(self.image_dir):
            tkmsg.showwarning("Warning", message="{} isn't dir.".format(self.image_dir))
            return
        self.image_paths = list()
        accepted_ext = (".jpeg", '.jpg', '.png')
        for ext in accepted_ext:
            self.image_paths.extend(glob.glob(os.path.join(self.image_dir, "*"+ext)))
        image_cnt = len(self.image_paths)
        if image_cnt == 0:
            tkmsg.showwarning("Warning", message="image doesn't exist.")
            return
        self.image_idx = 0
        self.image_cnt = image_cnt
        self.show_image(self.image_idx)
```
![https://ithelp.ithome.com.tw/upload/images/20200915/20119608oQz63W0FND.jpg](https://ithelp.ithome.com.tw/upload/images/20200915/20119608oQz63W0FND.jpg)

以上製作簡易相簿只能算是半成品，因為還少了載入資料夾的按鍵。

實際上載入圖片資料夾的功能已經寫在上面模組裡面了，layout上的按鍵我沒有寫在模組上，寫在主程式面板上，切換(switch)四個不同資料夾的radiobutton也是寫在主程式面板上。

![https://ithelp.ithome.com.tw/upload/images/20200924/20119608TfCPtF6jUa.jpg](https://ithelp.ithome.com.tw/upload/images/20200924/20119608TfCPtF6jUa.jpg)

其實我的目標是想完成以下的功能，一個版面同時可以撥放四個資料夾:

![https://ithelp.ithome.com.tw/upload/images/20200924/20119608ADtFHKYGIW.png](https://ithelp.ithome.com.tw/upload/images/20200924/20119608ADtFHKYGIW.png)

在面板上施作物鍵配置時，我使用grid方法。

    def init_ImgViewer(self):
        self.init_ImgViewer_tab = tk.Frame(self.notebook)
        self.init_ImgViewer_tab.pack(side = tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        self.notebook.add(self.init_ImgViewer_tab, text="init_ImgViewer")
        self.ImgSwitch = tk.StringVar()
        
   Channel 1:
        
        ivfram1 = tk.Frame(self.init_ImgViewer_tab )
        ivfram1.grid(row =0, column = 0, sticky = tk.E+tk.W)
        self.iv1 = IV.ImageViewer(ivfram1)
        ivfram1_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram1_2.grid(row =0, column = 1, sticky = tk.E+tk.W)
        opendir1 = tk.Button(ivfram1_2, 
                             text = "Open\n dir 1",
                             font=('Courier', 9),
                             command = self.iv1.open_dir)
        opendir1.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
        switch1 = tk.Radiobutton(ivfram1_2,
                                 text = "Img\n Switch 1",
                                 font=('Courier', 9),
                                 variable = self.ImgSwitch,
                                 value = "Img Switch 1",
                                 command = self.imgswitch)
        switch1.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)

   Channel 3:

        ivfram3 = tk.Frame(self.init_ImgViewer_tab )
        ivfram3.grid(row =0, column = 2, sticky = tk.E+tk.W)
        self.iv3 = IV.ImageViewer(ivfram3)
        ivfram3_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram3_2.grid(row =0, column = 3, sticky = tk.E+tk.W)
        opendir3 = tk.Button(ivfram3_2,
                             text = "Open\n dir 3",
                             font=('Courier', 9),
                             command = self.iv3.open_dir)
        opendir3.pack(side=tk.TOP, expand=tk.NO, fill = tk.X)
        switch3 = tk.Radiobutton(ivfram3_2, 
                                 text = "Img\n Switch 3",
                                 font=('Courier', 9), 
                                 variable = self.ImgSwitch, 
                                 value = "Img Switch 3",
                                 command = self.imgswitch)
        switch3.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)

   Channel 2:

        ivfram2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram2.grid(row =1, column = 0, sticky = tk.E+tk.W)
        self.iv2 = IV.ImageViewer(ivfram2)
        ivfram2_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram2_2.grid(row =1, column = 1, sticky = tk.E+tk.W)
        opendir2 = tk.Button(ivfram2_2,
                             text = "Open\n dir 2",
                             font=('Courier', 9),
                             command = self.iv2.open_dir)
        opendir2.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
        switch2 = tk.Radiobutton(ivfram2_2,
                                 text = "Img\n Switch 2",
                                 font=('Courier', 9),
                                 variable = self.ImgSwitch,
                                 value = "Img Switch 2",
                                 command = self.imgswitch)
        switch2.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
  
  Channel 4:
  
        ivfram4 = tk.Frame(self.init_ImgViewer_tab )
        ivfram4.grid(row =1, column = 2, sticky = tk.E+tk.W)
        self.iv4 = IV.ImageViewer(ivfram4)
        ivfram4_2 = tk.Frame(self.init_ImgViewer_tab )
        ivfram4_2.grid(row =1, column = 3, sticky = tk.E+tk.W)
        opendir1 = tk.Button(ivfram4_2,
                             text = "Open\n dir 4",
                             font=('Courier', 9),
                             command = self.iv4.open_dir)
        opendir1.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)
        switch4 = tk.Radiobutton(ivfram4_2,
                                 text = "Img\n Switch 4",
                                 font=('Courier', 9),
                                 variable = self.ImgSwitch,
                                 value = "Img switch 4",
                                 command = self.imgswitch)
        switch4.pack(side=tk.TOP, expand=tk.YES, fill = tk.X)

切換功能(switch):

    def imgswitch(self):
        if self.ImgSwitch.get() =="Img Switch 1":
            imageFile = self.iv1.image_paths[self.iv1.image_idx]
        elif self.ImgSwitch.get() =="Img Switch 2":
            imageFile = self.iv2.image_paths[self.iv2.image_idx]
        elif self.ImgSwitch.get() =="Img Switch 3":
            imageFile = self.iv3.image_paths[self.iv3.image_idx]
        elif self.ImgSwitch.get() =="Img Switch 4":
            imageFile = self.iv4.image_paths[self.iv4.image_idx]
 imageFile的功能像是一個指標，指標指向切換到該channel內部的image_idx變數，這樣做的原因是因應將來切換資料夾的功能可以串接到不同圖像偵測應用程式。
 
