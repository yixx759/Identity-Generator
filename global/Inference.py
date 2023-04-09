
from manipulate import Manipulator
import tensorflow as tf
import numpy as np 
import torch
import clip
from MapTS import GetBoundary,GetDt
from argparse import Namespace
import gc

class StyleCLIP():
    
    def __init__(self,dataset_name='ffhq'):
        print('load clip')
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, preprocess = clip.load("ViT-B/32", device=device)
        self.LoadData(dataset_name)


    def reset(self):
        tf.keras.backend.clear_session()

    def close(self):
        self.M.closesession()


    def LoadData(self, dataset_name,num=0, norm = True):
        tf.keras.backend.clear_session()

        M=Manipulator(dataset_name=dataset_name)

        np.set_printoptions(suppress=True)
        fs3=np.load('./npy/'+dataset_name+'/fs3.npy')

        self.M=M
        self.fs3=fs3

        if norm:

            #w_plus=np.load('./data/'+dataset_name+'/w_plus.npy')


            w_plus = np.load('./Dataset/W_plus/w_plus'+ str(num)+'.npy')
        else:
            w_plus = np.load('./CustomIdentities/Identity' + str(num) +'/BaseIdentity/w_plus.npy')


        self.M.dlatents=M.W2S(w_plus)






        # print(self.M.dlatents)
        # print(len(self.M.dlatents))
        # self.Generaterand(self.M.dlatents)

        if dataset_name=='ffhq':
            self.c_threshold=20
        else:
            self.c_threshold=100
        self.SetInitP()
    
    def SetInitP(self):
        self.M.alpha=[3]
        self.M.num_images=1
        
        self.target=''
        self.neutral=''
        self.GetDt2()
        img_index=0
        self.M.dlatent_tmp=[tmp[img_index:(img_index+1)] for tmp in self.M.dlatents]
        
        
    def GetDt2(self):
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
        #boundary_tmp2,num_c=GetBoundary(self.fs3,self.dt,self.M,threshold=self.beta)
        boundary_tmp2, num_c = GetBoundary(self.fs3, self.dt, self.M, self.beta)
        codes=self.M.MSCode(self.M.dlatent_tmp,boundary_tmp2)


        return codes

    # def Generaterand(self,codes):
    #     for i2 in range(len(codes)):
    #         for i in range(len(codes[i2][0])):
    #
    #             codes[i2][0][i] = random.uniform(-5.1,5.1)
    #
    #
    #     for i in codes:
    #         print(i)
    #         print(len(i))
    #         print(i[0][0])


    def GetImg(self):


        codes=self.GetCode()


        out=self.M.GenerateImg(codes)

        img=out[0,0]
        return img

    def spit_latent(self):
        out = torch.zeros((1,18,512))
        for i in range(18):
            out[0][i] = torch.tensor(self.dt)

        print("\n\n\n\n\n\n")
        print(out)
        print("\n\n\n\n\n\n")
        torch.save(out, "./test/latents.pt")
#%%
if __name__ == "__main__":
    style_clip=StyleCLIP()
    self=style_clip
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
