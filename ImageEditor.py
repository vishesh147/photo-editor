import tkinter as tk
from tkinter import Toplevel, simpledialog
from tkinter import Label
import tkinter.filedialog as tkfd
from tkinter.colorchooser import askcolor
from tkinter.constants import CENTER, COMMAND, HORIZONTAL, LEFT, N, NW, RIGHT
from typing import Container
from PIL import ImageTk, Image,  ImageEnhance, ImageDraw, ImageFont, ImageFilter, ImageOps
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN
)
import tkinter.messagebox as Msg
from tkinter.font import Font
from tkinter.messagebox import askyesno

root = tk.Tk()
root.title('Image Editor')
width= root.winfo_screenwidth() 
height= root.winfo_screenheight()
root.geometry("%dx%d" %(width, height))
black_whiteFrame = tk.Frame(root,bd=0)
CropFrame = tk.Frame(root,bd=0)
FlipHFrame = tk.Frame(root,bd=0)
FlipVFrame = tk.Frame(root,bd=0)
RotateFrame = tk.Frame(root,bd=0)
SaturationFrame = tk.Frame(root,bd=0)
SharpnessFrame = tk.Frame(root,bd=0)
ExposureFrame = tk.Frame(root,bd=0)
ContrastFrame = tk.Frame(root,bd=0)
HighlightFrame = tk.Frame(root,bd=0)
TextonImageFrame = tk.Frame(root,bd=0)
FileFrame = tk.Frame(root, bd=0)

def ResizeImg(img):
    ar = img.width/img.height
    if img.width > 1200 and img.height > 700 :
        if int(1200/ar) < 700:
            img = img.resize((1200, int(1200/ar)))
        else:
            img = img.resize((int(700*ar), 700))
    elif img.width > 1200 :
        img = img.resize((1200, int(1200/ar)))
    elif img.height > 700 :
        img = img.resize((int(700*ar), 700))
    return img

canvas = tk.Canvas(root, height = 700, width = 1200, bg="black", bd = 0)
canvas.place(relx=0, rely = 0.05, anchor=NW)
image = Image.open("default.jpg")
imgtk = ImageTk.PhotoImage(ResizeImg(image))
container = canvas.create_image(600, 350, anchor = CENTER, image=imgtk)


def PrintonCanvas(File):
    global imgtk, image
    print(File)
    image1 = Image.open(File)
    imgtk = ImageTk.PhotoImage(ResizeImg(image1))
    container = canvas.create_image(600, 350, anchor = CENTER, image=imgtk)
    image = image1

def update_image(image_container, new_image):
   canvas.itemconfig(image_container,image=new_image)

def Save(file):
    global image
    image.save(file)
    Msg.showinfo("Save File", "File Saved Successfully.")

def saveImage():
    data = [('JPG', '*.jpg')]
    file = tkfd.asksaveasfilename(filetypes=data, defaultextension=data)
    Save(file)

def openImage():
    file = tkfd.askopenfilename()
    PrintonCanvas(file)

def blackWhite():
    global image, imgtk
    ans = askyesno(title='Convert Image ?', message='Are you sure you want to convert image to grayscale?')
    if (ans):
        image = image.convert('L')
        imgtk = ImageTk.PhotoImage(ResizeImg(image))
        update_image(container, imgtk)   
        Msg.showinfo("Edit Successful", "Image converted to Grayscale.")

rect = None

def onclick(e):    
    global rect, startx, starty
    startx = canvas.canvasx(e.x) 
    starty = canvas.canvasy(e.y)
    if rect:
        canvas.tag_raise(rect)
        canvas.itemconfigure(rect, state='normal')    
    if not rect:
        rect = canvas.create_rectangle(e.x, e.y, 1, 1, outline='red')

def onhold(e):
    global startx, starty, rect
    curx = canvas.canvasx(e.x) 
    cury = canvas.canvasy(e.y)
    canvas.coords(rect, startx, starty, curx, cury)

def onrelease(e):
    global endx, endy
    endx = canvas.canvasx(e.x)
    endy = canvas.canvasy(e.y)
    Crop['state'] = 'active'
    pass

def selectArea():
    global startx, starty, rect, endx, endy
    canvas.bind("<ButtonPress-1>", onclick)
    canvas.bind("<B1-Motion>", onhold)
    canvas.bind("<ButtonRelease-1>", onrelease)
    Msg.showinfo("Select Area", "Select area by dragging your mouse over the image.")

def crop():
    global image, imgtk, startx, starty, endx, endy, rect
    img = ResizeImg(image)
    w, h = 600-img.width/2, 350-img.height/2                        #NW co-ordinates of imgtk
    ratio = image.width/img.width
    image = image.crop((ratio*(startx-w), ratio*(starty-h), ratio*(endx-w), ratio*(endy-h)))
    imgtk = ImageTk.PhotoImage(ResizeImg(image))
    update_image(container, imgtk)
    canvas.coords(rect, endx, endy, endx, endy)          
    canvas.itemconfigure(rect, state='hidden')                      #Red-dot
    Crop['state'] = 'disabled'
    canvas.unbind("<ButtonPress-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    Msg.showinfo("Edit Successful", "Image cropped successfully.")


def rotateL():
    global image, imgtk
    image = image.rotate(90, expand="True")
    imgtk = ImageTk.PhotoImage(ResizeImg(image))
    update_image(container, imgtk)
    
def rotateR():
    global image, imgtk
    image = image.rotate(-90, expand="True")
    imgtk = ImageTk.PhotoImage(ResizeImg(image))
    update_image(container, imgtk)

def FlipH():
    global image, imgtk
    image = image.transpose(Image.FLIP_LEFT_RIGHT)
    imgtk = ImageTk.PhotoImage(ResizeImg(image))
    update_image(container, imgtk)

def FlipV():
    global image, imgtk
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    imgtk = ImageTk.PhotoImage(ResizeImg(image))
    update_image(container, imgtk)

def Sharpness():
    ans = askyesno(title='Apply Edit ?', message='Are you sure that you want to apply the changes made to the image?')
    if (ans):
        factor = float(ScrollSharpness.get())
        global image, imgtk
        image = ImageEnhance.Sharpness(image).enhance(1 + factor*0.2)
        imgtk = ImageTk.PhotoImage(ResizeImg(image))
        update_image(container, imgtk)
        ScrollSharpness.set(0)
        Msg.showinfo("Edit Successful", "Sharpness edited successfully.")

def LiveSharpness(f):
    factor = float(ScrollSharpness.get())
    global image, imgtk  
    imgtk = ImageTk.PhotoImage(ResizeImg(ImageEnhance.Sharpness(image).enhance(1 + factor*0.2)))
    update_image(container, imgtk)

def Exposure():
    ans = askyesno(title='Apply Edit ?', message='Are you sure that you want to apply the changes made to the image?')
    if (ans):
        factor = float(ScrollExposure.get())
        global image, imgtk
        image = ImageEnhance.Brightness(image).enhance(1 + factor*0.0075)
        imgtk = ImageTk.PhotoImage(ResizeImg(image))
        update_image(container, imgtk)
        ScrollExposure.set(0)
        Msg.showinfo("Edit Successful", "Exposure edited successfully.")

def LiveExposure(f):
    factor = float(ScrollExposure.get())
    global image, imgtk  
    imgtk = ImageTk.PhotoImage(ResizeImg(ImageEnhance.Brightness(image).enhance(1 + factor*0.0075)))
    update_image(container, imgtk)


def Saturation():
    ans = askyesno(title='Apply Edit ?', message='Are you sure that you want to apply the changes made to the image?')
    if (ans):
        factor = float(ScrollSaturation.get())
        global image, imgtk
        image = ImageEnhance.Color(image).enhance(1 + factor*0.01)
        imgtk = ImageTk.PhotoImage(ResizeImg(image))
        update_image(container, imgtk)
        ScrollSaturation.set(0)
        Msg.showinfo("Edit Successful", "Saturation edited successfully.")

def LiveSaturation(f):
    factor = float(ScrollSaturation.get())
    global image, imgtk  
    imgtk = ImageTk.PhotoImage(ResizeImg(ImageEnhance.Color(image).enhance(1 + factor*0.01)))
    update_image(container, imgtk)


def Contrast():
    ans = askyesno(title='Apply Edit ?', message='Are you sure that you want to apply the changes made to the image?')
    if (ans):
        factor = float(ScrollContrast.get())
        global image, imgtk
        image = ImageEnhance.Contrast(image).enhance(1 + factor*0.0075)
        imgtk = ImageTk.PhotoImage(ResizeImg(image))
        update_image(container, imgtk)
        ScrollContrast.set(0)
        Msg.showinfo("Edit Successful", "Contrast edited successfully.")

def LiveContrast(f):
    factor = float(ScrollContrast.get())
    global image, imgtk  
    imgtk = ImageTk.PhotoImage(ResizeImg(ImageEnhance.Contrast(image).enhance(1 + factor*0.0075)))
    update_image(container, imgtk)

def HighlightBorders():
    ans = askyesno(title='Apply Edit ?', message='Are you sure you want to apply this filter ?')
    if ans :
        global image, imgtk
        image = image.filter(DETAIL)
        image = image.filter(FIND_EDGES)
        image = image.filter(SHARPEN)
        image = image.convert('L')
        #image = ImageOps.invert(image)
        imgtk = ImageTk.PhotoImage(ResizeImg(image))
        update_image(container, imgtk)
        Msg.showinfo("Edit Successful", "Borders highlighted successfully.")

def move(e):
    global txt
    x, y = canvas.coords(txt)
    x, y = e.x - x, e.y - y
    canvas.move(txt, x, y)

def TextonImage():
    global image, imgtk
    text_on_image['state'] = tk.DISABLED
    if(TextEntry.get()==""):
        Msg.showinfo("Error", "No text was entered!")
        text_on_image['state'] = tk.NORMAL
        return
    colour = askcolor(title="Choose text color", color=None)
    fontsize = simpledialog.askstring("Font size", "Enter font size", parent=root)
    global txt
    txt = canvas.create_text(600, 350, text=TextEntry.get(), anchor=NW, fill=colour[1], font=("Impact", int(fontsize), "normal"))
    canvas.bind('<B1-Motion>', move)
    fixpos.wait_variable(var)
    x, y = canvas.coords(txt)
    img = ResizeImg(image)
    w, h = 600-img.width/2, 350-img.height/2                           #NW co-ordinates of imgtk
    ratio = image.width/img.width
    draw = ImageDraw.Draw(image)
    Font = ImageFont.truetype("impact.ttf", int(1.35*ratio*int(fontsize)))
    draw.text(((x-w)*ratio, (y-h)*ratio), TextEntry.get(), fill=colour[1], font=Font)
    imgtk = ImageTk.PhotoImage(ResizeImg(image))
    update_image(container, imgtk)
    canvas.delete(txt)
    text_on_image['state'] = tk.NORMAL
    TextEntry.delete(0, 'end')
    Msg.showinfo("Edit Successful", "Text inserted successfully.")



SharpnessCount = tk.DoubleVar()
ScrollSharpness = tk.Scale(SharpnessFrame, variable= SharpnessCount, from_=0, to= 100, orient=HORIZONTAL, command=LiveSharpness)
ExposureCount = tk.DoubleVar()
ScrollExposure = tk.Scale(ExposureFrame, variable= ExposureCount, from_=-100, to= 100, orient=HORIZONTAL, command=LiveExposure)
ContrastCount = tk.DoubleVar()
ScrollContrast = tk.Scale(ContrastFrame, variable= ContrastCount, from_=-100, to= 100, orient=HORIZONTAL, command=LiveContrast)
SaturationCount = tk.DoubleVar()
ScrollSaturation = tk.Scale(SaturationFrame, variable= SaturationCount, from_=-100, to= 100, orient=HORIZONTAL, command=LiveSaturation)
TextVariable = tk.StringVar()
TextEntry = tk.Entry(TextonImageFrame,  textvariable = TextVariable, font=('calibre',10,'normal'), width=40)


black_white = tk.Button(black_whiteFrame, text = "Convert to Black & White", command= blackWhite)
select = tk.Button(CropFrame, text="Select area to crop", command=selectArea)
Crop = tk.Button(CropFrame, text = "Apply Crop", command= crop, state='disabled')
flipH = tk.Button(FlipHFrame, text = "Flip Horizontally", command= FlipH)
flipV = tk.Button(FlipVFrame, text = "Flip Vertically", command= FlipV)
rotateLeft = tk.Button(RotateFrame, text = "Rotate Left", command= rotateL)
rotateRight = tk.Button(RotateFrame, text = "Rotate Right", command= rotateR)
saturation = tk.Button(SaturationFrame, text = "Apply Saturation", command= Saturation)
sharpness = tk.Button(SharpnessFrame, text = "Apply Sharpness", command= Sharpness)
exposure = tk.Button(ExposureFrame, text = "Apply Exposure", command= Exposure)
contrast = tk.Button(ContrastFrame, text = "Apply Contrast", command= Contrast)
highlight_border = tk.Button(HighlightFrame, text = "Highlight Border", command= HighlightBorders)
text_on_image = tk.Button(TextonImageFrame, text = "Insert Text", command= TextonImage)
var = tk.IntVar()
fixpos = tk.Button(TextonImageFrame, text="Fix Position", command=lambda: var.set(1))
quit = tk.Button(root, text = "Quit", command=root.destroy)
OpenFile = tk.Button(FileFrame, text = "OpenFile", command=openImage)
SaveFile = tk.Button(FileFrame, text = "SaveFile", command=saveImage)


OpenFile.pack(side= LEFT)

SaveFile.pack(side = LEFT)

black_white.pack()
 
select.place(relx = 0.1, rely = 0.3) 
Crop.place(relx = 0.62, rely = 0.3)

flipH.place(relx = 0.2, rely = 0.3) 
flipV.place(relx = 0.2, rely = 0.3)

rotateLeft.place(relx = 0.2, rely = 0.3) 
rotateRight.place(relx = 0.6, rely = 0.3)

ScrollSaturation.pack(side = LEFT)
saturation.pack(side = RIGHT)

ScrollSharpness.pack(side = LEFT)
sharpness.pack(side = RIGHT)

ScrollExposure.pack(side = LEFT)
exposure.pack(side = RIGHT)

ScrollContrast.pack(side = LEFT)
contrast.pack(side = RIGHT)

highlight_border.pack()

TextEntry.place(relx = 0, rely = 0) 
text_on_image.place(relx = 0.4, rely = 0.4)
fixpos.place(relx = 0.7, rely = 0.4)


#quit.pack()
FileFrame.pack()
FileFrame.place(rely=0.01,relx=0.01)
black_whiteFrame.pack()
black_whiteFrame.place(relheight=0.09,relwidth=0.195,relx=0.8,rely=0.09)
CropFrame.pack()
CropFrame.place(relheight=0.09,relwidth=0.195,relx=0.8,rely=0.18)
FlipHFrame.pack()
FlipHFrame.place(relheight=0.05,relwidth=0.1,relx=0.8,rely=0.27)
FlipVFrame.pack()
FlipVFrame.place(relheight=0.05,relwidth=0.1,relx=0.9,rely=0.27)
RotateFrame.pack()
RotateFrame.place(relheight=0.09,relwidth=0.195,relx=0.8,rely=0.36)
SaturationFrame.pack()
SaturationFrame.place(relheight=0.09,relwidth=0.17,relx=0.815,rely=0.45)
SharpnessFrame.pack()
SharpnessFrame.place(relheight=0.09,relwidth=0.17,relx=0.815,rely=0.51)
ExposureFrame.pack()
ExposureFrame.place(relheight=0.09,relwidth=0.17,relx=0.815,rely=0.57)
ContrastFrame.pack()
ContrastFrame.place(relheight=0.09,relwidth=0.17,relx=0.815,rely=0.63)
HighlightFrame.pack()
HighlightFrame.place(relheight=0.09,relwidth=0.195,relx=0.8,rely=0.75)
TextonImageFrame.pack()
TextonImageFrame.place(relheight=0.09,relwidth=0.195,relx=0.8,rely=0.82)
root.mainloop()

