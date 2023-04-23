
import os
import numpy as np
import argparse
from manipulate import Manipulator
import torch
from PIL import Image
from Inference import loadtype
#%%


def main(ags):

    # This will generate a W_plus file and image from a latent file.

    # Load type defines what path the latent will be found.
    try:

        loader = loadtype(ags.Loadtype)

    except:
        loader = loadtype.Play





    dataset_name = ags.dataset_name

    if not os.path.isdir('./data/' + dataset_name):
        os.system('mkdir ./data/' + dataset_name)
    # %%
    M = Manipulator(dataset_name=dataset_name)
    np.set_printoptions(suppress=True)
    print(M.dataset_name)
    # %%
    # remove all .jpg
    names = os.listdir('./data/' + dataset_name + '/')
    for name in names:
        if '.jpg' in name:
            os.remove('./data/' + dataset_name + '/' + name)

    # %%


    if(loader == loadtype.Play):

        latents = torch.load('./data/' + dataset_name + '/latents.pt')
    elif(loader == loadtype.DataNorm):
        latents = torch.load('./Dataset/Latents/Latent' + ags.LatentNum + '.pt')
    elif(loader == loadtype.Customident):
        latents = torch.load('./CustomIdentities/Identity' + ags.IdentityNum + '/BaseIdentity/latents.pt')
    elif(loader == loadtype.Truecustom):
        latents = torch.load(ags.IdentityPath+"/latents.pt")

    w_plus = latents.cpu().detach().numpy()


    if (loader == loadtype.Play):

        np.save('./data/' + dataset_name + '/w_plus.npy', w_plus)
    elif (loader == loadtype.DataNorm):
        np.save('./Dataset/W_plus/w_plus'+ags.LatentNum+'.npy', w_plus)
    elif (loader == loadtype.Customident):
        np.save('./CustomIdentities/Identity'+ags.IdentityNum+'/BaseIdentity/w_plus.npy', w_plus)
    elif (loader == loadtype.Truecustom):
        np.save(ags.IdentityPath+"/w_plus.npy", w_plus)


    # %%
    tmp = M.W2S(w_plus)
    M.dlatents = tmp

    M.img_index = 0
    M.num_images = len(w_plus)
    M.alpha = [0]
    M.step = 1
    lindex, bname = 0, 0

    M.manipulate_layers = [lindex]
    codes, out = M.EditOneC(bname)
    # %%
    if (loader == loadtype.Play):

        for i in range(len(out)):
            img = out[i, 0]
            img = Image.fromarray(img)
            img.save('./data/' + dataset_name + '/' + str(i) + '.jpg')

    elif (loader == loadtype.DataNorm):
        for i in range(len(out)):
            img = out[i, 0]
            img = Image.fromarray(img)
            img.save('./Dataset/Photos/' + ags.LatentNum + '.jpg')

    elif (loader == loadtype.Customident):
        for i in range(len(out)):
            img = out[i, 0]
            img = Image.fromarray(img)
            img.save('./CustomIdentities/Identity'+ags.IdentityNum+'/BaseIdentity/0.jpg')

    elif (loader == loadtype.Truecustom):
        for i in range(len(out)):
            img = out[i, 0]
            img = Image.fromarray(img)
            img.save(ags.IdentityPath+ '/1' + '.jpg')



    # %%
    M.closesession()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--dataset_name', type=str, default='ffhq',
                        help='name of dataset, for example, ffhq')

    parser.add_argument('--real', action='store_true')

    args = parser.parse_args()

    main(args)

    
    
