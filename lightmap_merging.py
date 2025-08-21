import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os

class lightmap_merge():
    def __init__(self, texture_file, x, y , lightmap_file, output_file, paksize):
        self.texture=texture_file
        self.x=int(x)
        self.y=int(y)
        self.lightmap=lightmap_file
        self.output=output_file
        self.paksize=int(paksize)
    def flag(self):
        if os.path.isfile(self.texture)==False or os.path.isfile(self.lightmap)==False:
            return 0
        else:
            imge = Image.open(self.texture)
            print(imge.mode)
            im = np.array(imge)
            image_lightmap=Image.open(self.lightmap)
            im_lightmap=np.array(image_lightmap, dtype = "float64")
            print(im.shape)
            imX = im.shape[0]
            imY = im.shape[1]
            modemode=0
            print(image_lightmap.mode,im_lightmap.shape)
            if image_lightmap.mode == "RGBA":
                #f=open("img.txt","w")
                #for i in range(self.before):
                #    f.write("[")
                #    for j in range(self.before):
                #        f.write(str(im[i,j])+",")
                #    f.write("]\n")
                #f.close()
                #return 2
                modemode+=1
            if imge.mode=="RGBA":
                modemode+=2
            #if imge.mode=="P":
            #    modemode=1
            # print(im[0,0])
            if imX % self.paksize == 0 and imY % self.paksize == 0 and self.paksize>0 and imX >= self.paksize*(self.x+1) and imY >= self.paksize*(self.y+1):
                output=Image.fromarray(lightmap_merge_program(im,self.x,self.y,im_lightmap,self.paksize,modemode))
                output.save(self.output)
                return 1
            else: 
                return 2

def lightmap_merge_program(intexture,x,y,inimg,paksize,mode):
    def def_bg_color(mode):
        if mode == 0:
            return np.array([231,255,255])
        elif mode == 1:
            return np.array([231,255,255,255])
    def resize_color(input,mode):
        if mode==0 or mode==3:
            return input
        elif mode == 2:
            return np.append(input,128)
        else:
            return np.delete(input,3)
    bgcolor=def_bg_color(mode%2)
    imX=inimg.shape[0]
    imY=inimg.shape[1]
    temp_list=np.zeros((imX,imY,(3+mode//2)))
    print(temp_list)
    def change_size():
        for i in range(imX):
            for j in range(imY):
                if np.array_equal(inimg[i,j],bgcolor)or np.array_equal(inimg[i,j],np.zeros(3+mode%2)):
                    # print(i,j,inimg[i,j])
                    temp_list[i,j]=def_bg_color(mode//2)
                else:
                    temp_list[i,j]=intexture[i%paksize+x*paksize,j%paksize+y*paksize]*resize_color(inimg[i,j],mode)/128
                    print(i,j,resize_color(inimg[i,j],mode),intexture[i%paksize+x*paksize,j%paksize+y*paksize],temp_list[i,j])
    change_size()
    temp_list[temp_list>255]=255
    outimg=temp_list.astype(np.uint8)
    # print(outimg)
    # print(outimg.shape)
    return outimg




def make_window():
    def ask_files():
        path=filedialog.askopenfilename()
        file_path.set(path)
    def ask_texture_files():
        path=filedialog.askopenfilename()
        texture_file_path.set(path)

    def app():
        beforesize=(input_pak_box.get())
        input_file = file_path.get()
        x = texture_x.get()
        y=texture_y.get()
        texture_file = texture_file_path.get()
        output_file = filedialog.asksaveasfilename(
            filetype=[("PNG Image Files","*.png")],defaultextension=".png"
        )
        print(output_file)
        if not input_file or not output_file or not beforesize:
            return
        afterfile = lightmap_merge(texture_file,x,y,input_file,output_file,beforesize)
        if afterfile.flag() ==0:
            messagebox.showinfo("エラー","画像がありません")
        elif afterfile.flag() ==1:
            messagebox.showinfo("完了","完了しました。")
        elif afterfile.flag() ==2:
            messagebox.showinfo("エラー","画像サイズが正しくありません")
    main_win = tk.Tk()
    main_win.title("lightmap merging")
    main_win.geometry("500x200")
    main_frm = ttk.Frame(main_win)
    main_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=5, pady=10)
    file_path=tk.StringVar()
    texture_file_path=tk.StringVar()
    texture_folder_label = ttk.Label(main_frm, text="気候ファイルを選択")
    texture_folder_box = ttk.Entry(main_frm,textvariable=texture_file_path)
    texture_folder_btn = ttk.Button(main_frm, text="選択",command=ask_texture_files)
    folder_label = ttk.Label(main_frm, text="ライトマップファイルを選択")
    folder_box = ttk.Entry(main_frm,textvariable=file_path)
    folder_btn = ttk.Button(main_frm, text="選択",command=ask_files)
    input_pak_label = ttk.Label(main_frm, text="pakサイズ")
    input_pak_box = ttk.Entry(main_frm)
    texture_label=ttk.Label(main_frm,text='テクスチャファイルの画像位置(縦、横)')
    texture_x=ttk.Entry(main_frm)
    texture_y=ttk.Entry(main_frm)
    app_btn=ttk.Button(main_frm, text="変換を実行",command=app)
    texture_folder_label.grid(column=0,row=1,pady=10)
    texture_folder_box.grid(column=1,row=1,sticky=tk.EW, padx=5)
    texture_folder_btn.grid(column=2,row=1)
    folder_label.grid(column=0,row=0,pady=10)
    folder_box.grid(column=1,row=0,sticky=tk.EW, padx=5)
    folder_btn.grid(column=2,row=0)
    texture_label.grid(column=0,row=2,pady=10)
    texture_x.grid(column=1,row=2,sticky=tk.EW, padx=5)
    texture_y.grid(column=2,row=2,sticky=tk.EW, padx=5)
    input_pak_box.grid(column=1,row=3,sticky=tk.EW, padx=5)
    input_pak_label.grid(column=0,row=3)
    app_btn.grid(column=1,row=4)
    #main_win.columnconfigure(0, wieght=1)
    #main_win.rowconfigure(0, wieght=1)
    #main_frm.columnconfigure(1, wieght=1)
    main_win.mainloop()
if __name__=="__main__":  
    make_window()