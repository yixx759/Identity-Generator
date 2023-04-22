
from PIL import Image

from Inference import StyleCLIP

#%%


class ImageEditorFunctions():  #Controller
    '''
    followed Model View Controller Design Pattern
    
    controller, model, view
    '''
    def __init__(self,dataset_name='ffhq'):

        self.img_ratio=2
        self.style_clip=StyleCLIP(dataset_name)

        self.drawn  = None
        self.ident = []
        
    def close(self):
        #closing the current session and clears memory being used.
        #If you have alot of OOM errors using this can alleviate the problem.

        self.style_clip.close()




        
    def changeLatent(self, path ="" ,num = 0, norm=1):
        #Allows a new latent to be loaded and used to edit.
        #By pointing to its w_plus.npy

        #The norm paramater tells which path it will take.
        # 1 - For Playinteractivley and takes its default path.
        # 2 - GenerateDataset pathset created with random latents.
        # 3 - CustomiseCharacter pathset for each identity.
        # 4 - True path takes the string passed in.

        # num is used in 2 and 3. Eg num = 3 and norm = 3.
        # Inside custom identities it selects the latent in  Identity3

        #Path is used in True path and allows the user to pass in the path to be used.


        #Loading latent files takes a long time so try to limit this to 1 load at the start..

        self.style_clip.LoadData('ffhq',path,num,norm)


    #save with default saver prompt and give


    def SetBaseCode(self, codes=None):
        # Assigns the latent codes to edit from.
        # When starting the first set of codes are gathered from the latent files.
        # But we can save our own from the edits we make.
        # If nothing is provided in the codes parameter then the current code will be saved
        # and used as the base to edit from.
        # If one is provided it is the base used to edit off of.

        # The attribute ident can be used to saves these codes throughout use of the session.



        if(codes == None):
            codes=self.style_clip.GetCode()
        self.style_clip.M.dlatent_tmp=[tmp[:,0] for tmp in codes]
        print('set init ')
        return codes
    
    def ChangeStrength(self, StrengthFactor=7.0):
        # This changes the Strength of the modification.
        # For example the prompt to make the picture Smile with a input of 1 will have a smirk
        # whereas an input value of 10 is a full teeth smile




        self.style_clip.M.alpha=[float(StrengthFactor)]
        print(self.style_clip.M.alpha)
        img=self.style_clip.GetImg()
        arr = img
        print('manipulate one Alpha')
        img=Image.fromarray(img)

        return img ,arr
        
    def ChangeAreaAffected(self, DisentanglementFactor=20):
        # This changes the Disentanglement of the modification.
        # This number defines the amount of channels that will be modified.
        # Make sure to note it's the lower the number the more channels modified.
        # The more channels available to be edited means generally
        # the more parts of the face will be affected.


        self.style_clip.beta= float(DisentanglementFactor) / 100
        print("Here " + str(DisentanglementFactor))
        print(str(self.style_clip.beta))
        img=self.style_clip.GetImg()
        arr = img
        print('manipulate one Beta')
        img=Image.fromarray(img)

        return img, arr

    
    def TargetEdit(self, DesiredEdit):
        # This function changes the "target" to edit too.
        # This input is the affect we want to make or the result we want to see of th the image.

        self.style_clip.target= DesiredEdit
        self.style_clip.ApplyChanges()
        img=self.style_clip.GetImg()
        arr = img
        print('manipulate one')
        img=Image.fromarray(img)
        print(self.style_clip.M.alpha)
        print(self.style_clip.beta)
        return img, arr
        
        
    def NeutralForm(self, BaseForm="Face with hair"):
        # This is the base from which we edit from.
        # The input should be a description of what the image without editing looks like.
        # Make note that similar phrases have diffrent effects eg person with x vs face with x


        self.style_clip.neutral= BaseForm
    def EditImage(self, NeutralPoint, TargetEdit, Strength, Disentanglement, savechange, savecode):

        self.NeutralForm(NeutralPoint)
        self.TargetEdit(TargetEdit)
        self.ChangeStrength(Strength)
        img , arr  = self.ChangeAreaAffected(Disentanglement)

        if(savecode == True):
            self.ident.append(self.SetBaseCode())

        elif (savechange == True):
            self.SetBaseCode()

        return img, arr


    

    

        
    #%%
if __name__ == "__main__":
    
    dataset_name="ffhq"
    
    self=ImageEditorFunctions(dataset_name)
    self.run()
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
