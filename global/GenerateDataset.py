from GenerateRand import GetRandLatent
import requests
import GetLatentInfo
from argparse import Namespace
import os
import tensorflow as tf
from GetLatent import main as getnewlatent







Testgroup= 10
for i in range(Testgroup):
    # Generates new random latens
    filename = "Latent" + str(i)+".pt"
    photoname = str(i) +".jpg"
    GetRandLatent("./Dataset/Photos/", "./Dataset/Latents/" + filename, photoname)
    path ="./static/Dataset Tester"+str(i)
    # If files exist don't create a new a path but if it dost do.
    if not (os.path.exists(path)):
        os.mkdir(path)








# This is the list of prompts to nomalise a face

# natural - natural position
# target - what to edit to
# strength - change strength
# disentanglment - area affected (lower better)
# Save - save location


params2 = [{'natural':'person with clothes ', 'target':'person with white shirt','strength':'4','disentanglment':'11','save':'2'},

{'natural':'face with hair', 'target':'face without hair','strength':'9.52','disentanglment':'15.9','save':'2'},
{'natural':'face with hair', 'target':'face without hair','strength':'3','disentanglment':'17.3','save':'2'},
    {'natural':'person ', 'target':'person with beard','strength':'-2','disentanglment':'9','save':'2'},
    {'natural':'person ', 'target':'person with beard','strength':'-2','disentanglment':'11','save':'2'},

    {'natural':'Makeup', 'target':'no makeup','strength':'3','disentanglment':'13','save':'4'},

{'natural':'Person with glasses', 'target':'Person with no glasses','strength':'5','disentanglment':'13','save':'2'},
{'natural':'Person with glasses', 'target':'Person with no glasses','strength':'3','disentanglment':'14','save':'2'},

{'natural':'hair', 'target':'tidy dark hair ','strength':'3','disentanglment':'17','save':'2'},
{'natural':'person', 'target':'person  smiling','strength':'-3','disentanglment':'13','save':'7'},
{'natural':'person open mouth', 'target':'person  closed mouth','strength':'2','disentanglment':'10','save':'2'},
{'natural':'child', 'target':'adult','strength':'2','disentanglment':'15','save':'2'},
{'natural':'brown eyes', 'target':'blue eyes','strength':'-6','disentanglment':'19','save':'2'},
{'natural':'busy background', 'target':'simple background','strength':'3.619','disentanglment':'10','save':'2'},
{'natural':'colored background', 'target':'white background','strength':'2.65','disentanglment':'15','save':'2'}]

parmas3 = {'natural':'face side view', 'target':'face front view','strength':'25','disentanglment':'8','save':'2'}


url = "http://localhost:5000/dataset"
url5 = "http://localhost:5000/initdataset"
url4= "http://localhost:5000/close"
for i2 in range(Testgroup):
    # Iterated through the number of latents using the iterator i.


    filenamel = "F:\Challenges\StyleCLIP\global\Dataset\Latents\Latent"+str(i2)+".pt"
    photofile = "F:/Challenges/StyleCLIP/global/Dataset/Photos/"+str(i2) +".jpg"
    ex = Namespace(real=True, dataset_name="ffhq", LatentNum=str(i2), Loadtype=2)
    # This will generate the image information from the latent eg Image with correct color and w_plus.npy
    GetLatentInfo.main(ex)
    # This will generate the latent information from the now correct looking image.
    getnewlatent(filenamel,photofile)
    GetLatentInfo.main(ex)

    # This url will change the latent loaded into the gpu with the corresponding number in dataset files.
    url3 = "http://localhost:5000/changer/" + str(i2)


    requests.get(url3)
    # Changing this save location means the fixed images will re write the original.
    parmas3['save'] = "F:/Challenges/StyleCLIP/global/Dataset/Photos/"+str(i2)

    # This applies the head rotation prompt twice fixing the head rotaion.
    for i in range(2):
        r = requests.get(url5, params=parmas3)

    # To use the new rotated identity it will need to be encoded again as the agressive rotation usally generates artifacts
    # this will have a normalisation effect.
    getnewlatent(filenamel, photofile)
    GetLatentInfo.main(ex)
    # This simply applies the normalisation prompts to the new image saving a timeline along the way.
    for i in range(len(params2)):
        params2[i]['save'] = str(i+1)
        #params2[i]['save'] = "Dataset Tester"+ str(i2)+"/"+params2[i]['save']
        params2[i]['save'] = "Dataset Tester"+ str(i2)+"/"+params2[i]['save']
        r = requests.get(url, params=params2[i])
        print(r.url)

        tf.reset_default_graph()
    # Switching latents is memory intensive and its good to reset this.
    requests.get(url4)
    tf.reset_default_graph()

# After these prompts are executed the results are saved and combined into one timeline.
url = "http://localhost:5000/datasetresult"
r = requests.get(url)

print(r)
requests.get(url4)

