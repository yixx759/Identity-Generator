


from tkinter import Tk 
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
#from GUI import View
from GUI import View
#from Inference import StyleCLIP
from Inference import StyleCLIP
import argparse
#%%


class PlayInteractively():  #Controller
    '''
    followed Model View Controller Design Pattern
    
    controller, model, view
    '''
    def __init__(self,dataset_name='ffhq'):
        
        self.root = Tk()
        self.view=View(self.root)
        self.img_ratio=2
        self.style_clip=StyleCLIP(dataset_name)
        
##        self.view.neutral.bind("<Return>", self.text_n)
##        self.view.target.bind("<Return>", self.text_t)
##        self.view.alpha.bind('<ButtonRelease-1>', self.ChangeAlpha)
##        self.view.beta.bind('<ButtonRelease-1>', self.ChangeBeta)
##        self.view.set_init.bind('<ButtonPress-1>', self.SetInit) 
##        self.view.reset.bind('<ButtonPress-1>', self.Reset)
        self.open_img()
       # self.text_n()
      #  self.text_t()
       # self.ChangeAlpha()
        #self.view.bg.bind('<Double-1>', self.open_img)
        
        
        self.drawn  = None
        self.ident = []
       # self.view.target.delete(1.0, "end")
       # self.view.target.insert("end", self.style_clip.target)
#        
       # self.view.neutral.delete(1.0, "end")
       # self.view.neutral.insert("end", self.style_clip.neutral)
        
    def close(self):
        self.style_clip.close()


    def Reset(self,event):
        self.style_clip.GetDt2()
        self.style_clip.M.alpha=[0]
        
       # self.view.beta.set(self.style_clip.beta)
        #self.view.alpha.set(0)
        
        img=self.style_clip.GetImg()
        img=Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.addImage_m(img)
        
    def changeLatent(self, num, norm=True):
        self.style_clip.LoadData('ffhq',num,norm)


    #save with default saver prompt and give


    def SetInit(self, codes=None):
        if(codes == None):
            codes=self.style_clip.GetCode()
        self.style_clip.M.dlatent_tmp=[tmp[:,0] for tmp in codes]
        print('set init ')
        return codes
    
    def ChangeAlpha(self, input=7.0):
        #tmp=self.view.alpha.get()
        #self.style_clip.M.alpha=[float(tmp)]
        self.style_clip.M.alpha=[float(input)]
        print(self.style_clip.M.alpha)
        img=self.style_clip.GetImg()
        print('manipulate one Alpha')
        img=Image.fromarray(img)
        ##img = ImageTk.PhotoImage(img)
        self.addImage_m(img)
        return img
        
    def ChangeBeta(self,input=20):
        #tmp=self.view.beta.get()
        self.style_clip.beta=float(input)/100
        print("Here "+input)
        print(str(self.style_clip.beta))
        img=self.style_clip.GetImg()
        print('manipulate one Beta')
        img=Image.fromarray(img)
        #img = ImageTk.PhotoImage(img)
        self.addImage_m(img)
        return img

    def ChangeDataset(self,event):
        
        dataset_name=self.view.set_category.get()
        
        self.style_clip.LoadData(dataset_name)
        
        self.view.target.delete(1.0, "end")
        self.view.target.insert("end", self.style_clip.target)
        
        self.view.neutral.delete(1.0, "end")
        self.view.neutral.insert("end", self.style_clip.neutral)
    
    def text_t(self, input):
        #tmp=self.view.target.get("1.0",'end')
        
        #tmp=tmp.replace('\n','')
        
       # self.view.target.delete(1.0, "end")
       # self.view.target.insert("end", tmp)
        
       # print('target',tmp,'###')
        self.style_clip.target= input
        self.style_clip.GetDt2()
       # self.view.beta.set(self.style_clip.beta)
       # self.view.alpha.set(3)
        #self.style_clip.M.alpha=[3]
        
        img=self.style_clip.GetImg()
        arr = img
        print('manipulate one')
        img=Image.fromarray(img)
       ## img = ImageTk.PhotoImage(img)
        self.addImage_m(img)
        print(self.style_clip.M.alpha)
        print(self.style_clip.beta)
        return img, arr
        
        
    def text_n(self, input="Face with hair"):
       # tmp=self.view.neutral.get("1.0",'end')
        #tmp=tmp.replace('\n','')
        
        #self.view.neutral.delete(1.0, "end")
        #self.view.neutral.insert("end", tmp)
        
       # print('neutral',tmp,'###')
        self.style_clip.neutral= input
        #self.view.target.delete(1.0, "end")
       # self.view.target.insert("end", tmp)

        
    def run(self):
        self.root.mainloop()
    
    def addImage(self,img):
       # self.view.bg.create_image(self.view.width/2, self.view.height/2, image=img, anchor='center')
        self.image=img #save a copy of image. if not the image will disappear
        
    def addImage_m(self,img):
        #self.view.mani.create_image(512,512, image=img, anchor='center')
        self.image2=img
        
    
    def openfn(self, input):
        #filename = askopenfilename(title='open',initialdir='./data/'+self.style_clip.M.dataset_name+'/',filetypes=[("all image format", ".jpg"),("all image format", ".png")])
       
        filename = "./Dataset/Photos/"+ input +".jpg"
        return filename
    
    def open_img(self):
        x = self.openfn("0")
        print(x)
        
        
        img = Image.open(x)
        img2 = img.resize(( 512,512), Image.ANTIALIAS)
        #img2 = ImageTk.PhotoImage(img2)
        self.addImage(img2)
        
        #img = ImageTk.PhotoImage(img)
        self.addImage_m(img)
        
        img_index=x.split('/')[-1].split('.')[0]
        img_index=int(img_index)
        print(img_index)
        self.style_clip.M.img_index=img_index
        self.style_clip.M.dlatent_tmp=[tmp[img_index:(img_index+1)] for tmp in self.style_clip.M.dlatents]
        
        
        self.style_clip.GetDt2()
        #self.view.beta.set(self.style_clip.beta)
       # self.view.alpha.set(3)
        
    #%%
if __name__ == "__main__":
    
    dataset_name="ffhq"
    
    self=PlayInteractively(dataset_name)
    self.run()
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
