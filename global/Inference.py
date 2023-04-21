import enum
from manipulate import Manipulator
import tensorflow as tf
import numpy as np 
import torch
import clip
from MapTS import GetBoundary,GetDt


class loadtype(enum.Enum):
    Play = 1
    DataNorm = 2
    Customident = 3
    Truecustom = 4


class StyleCLIP():
    
    def __init__(self,dataset_name='ffhq'):
        print('load clip')
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, preprocess = clip.load("ViT-B/32", device=device)
        self.LoadData(dataset_name)



    def reset(self):
        # Clears memory used by previous models

        tf.keras.backend.clear_session()

    def close(self):
        # Closes the current gpu session in tensorflow freeing up recources.
        # Although it will take time to reset.

        self.M.closesession()


    def LoadData(self, dataset_name, place = "", num=0, norm = 1):
        # Loads latent data from specified path below.
        # This is using the above parameters.

        newnorm = loadtype(norm)

        tf.keras.backend.clear_session()

        M=Manipulator(dataset_name=dataset_name)

        np.set_printoptions(suppress=True)
        fs3=np.load('./npy/'+dataset_name+'/fs3.npy')

        self.M=M
        self.fs3=fs3

        if newnorm == loadtype.Play:

            w_plus=np.load('./data/'+dataset_name+'/w_plus.npy')

        elif newnorm == loadtype.DataNorm:
            w_plus = np.load('./Dataset/W_plus/w_plus'+ str(num)+'.npy')
        elif newnorm == loadtype.Customident:
            w_plus = np.load('./CustomIdentities/Identity' + str(num) +'/BaseIdentity/w_plus.npy')
        elif newnorm == loadtype.Truecustom:
            w_plus = np.load(place+"/w_plus.npy")

        self.M.dlatents=M.W2S(w_plus)






        # print(self.M.dlatents)
        # print(len(self.M.dlatents))
        # self.Generaterand(self.M.dlatents)

        if dataset_name=='ffhq':
            self.c_threshold=20
        else:
            self.c_threshold=100
        self.SetBaseCodesP()
    
    def SetBaseCodesP(self):
        # Assigns the latent codes to edit from.




        self.M.alpha=[3]
        self.M.num_images=1
        
        self.target=''
        self.neutral=''
        self.ApplyChanges()
        img_index=0
        self.M.dlatent_tmp=[tmp[img_index:(img_index+1)] for tmp in self.M.dlatents]
        
        
    def ApplyChanges(self):

        # When the target is changed and the edit needs to be made use this function to apply the change to get the correct codes.

        classnames=[self.target,self.neutral]
        dt=GetDt(classnames,self.model)
        
        self.dt=dt



        num_cs=[]
        betas=np.arange(0.1,0.3,0.01)
        for i in range(len(betas)):
            boundary_tmp2,num_c=GetBoundary(self.fs3,self.dt,self.M,threshold=betas[i])
            print(betas[i])
            num_cs.append(num_c)



        num_cs=np.array(num_cs)




        select=num_cs>self.c_threshold
        
        if sum(select)==0:
            self.beta=0.1
        else:
            self.beta=betas[select][-1]
        
    
    def GetCode(self):
        # Generating codes that define what a face looks like, and its position in latent space.
        # From the variables defined before strength disentanglement neutral position target position.
        boundary_tmp2, num_c = GetBoundary(self.fs3, self.dt, self.M, self.beta)
        codes=self.M.MSCode(self.M.dlatent_tmp,boundary_tmp2)


        return codes




    def GetImg(self):
        # From the codes which define what the face looks like we can generate
        # an array to convert to an image.

        codes=self.GetCode()


        out=self.M.GenerateImg(codes)

        img=out[0,0]
        return img


#%%
if __name__ == "__main__":
    style_clip=StyleCLIP()
    self=style_clip
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
