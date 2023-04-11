import os
from argparse import Namespace
import shutil
import requests

CelebName = "Kanye"
wpath = "./CustomIdentities/Identity' + str(num) +'/BaseIdentity/w_plus.npy'"



changelatent = "http://localhost:5000/changerTrue/"+wpath


path = "./"+CelebName+"/"
if not os.path.exists(path):
     os.makedirs(path)
basepath = path+"/BaseIdentity"
if not os.path.exists(basepath):
     os.makedirs(basepath)

shutil.copy("./static/Dataset Tester"+str(i)+"/finallatent.pt",basepath+"/latents.pt")
ex = Namespace(real=True, dataset_name="ffhq", IdentityNum=str(i+1))
GetGUIData(ex)
#    print("using this")
requests.get(changelatent)
print("using this")
hairpath = path + "/NewIdentitys"
##'./CustomIdentities/Identity' + str(num) + '/BaseIdentity/w_plus.npy'



#add crawler and decorator to class