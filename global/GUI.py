

from tkinter import Tk,Frame ,Label,Button,messagebox,Canvas,Text,Scale
from tkinter import  HORIZONTAL

class View():
    def __init__(self,master):
        
        self.width=600
        self.height=600
        
        
        self.root=master
        self.root.geometry("600x600")
        
        self.left_frame=Frame(self.root,width=600)
        self.left_frame.pack_propagate(0)
        self.left_frame.pack(fill='both', side='left', expand='True')
        
        self.retrieval_frame=Frame(self.root,bg='snow3')
        self.retrieval_frame.pack_propagate(0)
        self.retrieval_frame.pack(fill='both', side='right', expand='True')
        
        self.bg_frame=Frame(self.left_frame,bg='snow3',height=600,width=600)
        self.bg_frame.pack_propagate(0)
        self.bg_frame.pack(fill='both', side='top', expand='True')
        
        self.command_frame=Frame(self.left_frame,bg='snow3')
        self.command_frame.pack_propagate(0)
        self.command_frame.pack(fill='both', side='bottom', expand='True')
#        self.command_frame.grid(row=1, column=0,padx=0, pady=0)
        
        self.bg=Canvas(self.bg_frame,width=self.width,height=self.height, bg='gray')
        self.bg.place(relx=0.5, rely=0.5, anchor='center')
        
        self.mani=Canvas(self.retrieval_frame,width=1024,height=1024, bg='gray') 
        self.mani.grid(row=0, column=0,padx=0, pady=42)
        

        
        
        
    
    def run(self):
        self.root.mainloop()
    
    def helloCallBack(self):
        category=self.set_category.get()
        messagebox.showinfo( "Hello Python",category)
    


#%%
if __name__ == "__main__":
    master=Tk()
    self=View(master)
    self.run()
    
    
    
    
    
    
    
