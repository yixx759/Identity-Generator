from GenerateRand import mainhere
import requests
import GetGUIDataDataset
from argparse import Namespace
import os
import tensorflow as tf
from GetLatent import main as getnewlatent
#from RemoveBackground import main as remove


# target = "F:/Challenges/StyleCLIP/global/static/Dataset Tester" + "0" + "/" + str(14)+".png"
# newtarget = "F:/Challenges/StyleCLIP/global/static/Dataset Tester" + "0" + "/" + str(15)+".png"
# remove(target, newtarget)






Testgroup= 10
for i in range(Testgroup):
    filename = "Latent" + str(i)+".pt"
    photoname = str(i) +".jpg"
    mainhere("./Dataset/Photos/","./Dataset/Latents/"+filename,photoname)
    path ="./static/Dataset Tester"+str(i)
    if not (os.path.exists(path)):
        os.mkdir(path)











params2 = [{'natural':'person with clothes ', 'target':'person with white shirt','strength':'4','disentanglment':'10','save':'2'},

{'natural':'face with hair', 'target':'face without hair','strength':'6.52','disentanglment':'13.9','save':'2'},
{'natural':'face with hair', 'target':'face without hair','strength':'8','disentanglment':'20.9','save':'2'},
    {'natural':'person ', 'target':'person with beard','strength':'-1','disentanglment':'9','save':'2'},
{'natural':'person ', 'target':'person clean shaven','strength':'-2','disentanglment':'8','save':'2'},
    {'natural':'Makeup', 'target':'no makeup','strength':'3','disentanglment':'3','save':'4'},

{'natural':'Person with glasses', 'target':'Person with no glasses','strength':'5','disentanglment':'11','save':'2'},
{'natural':'Person with glasses', 'target':'Person with no glasses','strength':'3','disentanglment':'11','save':'2'},
 {'natural':'overweight person', 'target':'skinny person ','strength':'1','disentanglment':'9','save':'2'},
{'natural':'hair', 'target':'tidy dark hair ','strength':'3','disentanglment':'13','save':'2'},
{'natural':'person', 'target':'person  smiling','strength':'-3','disentanglment':'10','save':'7'},
{'natural':'person open mouth', 'target':'person  closed mouth','strength':'2','disentanglment':'10','save':'2'},
{'natural':'child', 'target':'adult','strength':'2','disentanglment':'5','save':'2'},
{'natural':'busy background', 'target':'simple background','strength':'3.619','disentanglment':'10','save':'2'},
{'natural':'colored background', 'target':'white background','strength':'2.65','disentanglment':'10','save':'2'}]

parmas3 = {'natural':'face side view', 'target':'face front view','strength':'20','disentanglment':'7','save':'2'}
#parmas3 = {'natural':'face with hair', 'target':'face with long hair','strength':'20','disentanglment':'8.6','save':'2'}
#face front view  20 8.6

url = "http://localhost:5000/dataset"
url5 = "http://localhost:5000/initdataset"
url4= "http://localhost:5000/close"
for i2 in range(Testgroup):
    filenamel = "F:\Challenges\StyleCLIP\global\Dataset\Latents\Latent"+str(i2)+".pt"
    photofile = "F:/Challenges/StyleCLIP/global/Dataset/Photos/"+str(i2) +".jpg"
    ex = Namespace(real=True, dataset_name="ffhq", LatentNum=str(i2))
    GetGUIDataDataset.main(ex)
    getnewlatent(filenamel,photofile)
    GetGUIDataDataset.main(ex)
    url2 = "http://localhost:5000/change/"+str(i2)
    url3 = "http://localhost:5000/changer/" + str(i2)

    requests.get(url2)
    requests.get(url3)
    parmas3['save'] = "F:/Challenges/StyleCLIP/global/Dataset/Photos/"+str(i2)
    for i in range(3):
        r = requests.get(url5, params=parmas3)

    getnewlatent(filenamel, photofile)
    GetGUIDataDataset.main(ex)
    for i in range(len(params2)):
        params2[i]['save'] = str(i+1)
        #params2[i]['save'] = "Dataset Tester"+ str(i2)+"/"+params2[i]['save']
        params2[i]['save'] = "Dataset Tester"+ str(i2)+"/"+params2[i]['save']
        r = requests.get(url, params=params2[i])
        print(r.url)
        tf.reset_default_graph()

    requests.get(url4)
    tf.reset_default_graph()

url = "http://localhost:5000/datasetresult"
r = requests.get(url)

print(r)
requests.get(url4)

# for i in range(len(params2)):
#
#     target = "F:/Challenges/StyleCLIP/global/static/Dataset Tester" + str(i) + "/" + str(len(params2))+".png"
#     newtarget = "F:/Challenges/StyleCLIP/global/static/Dataset Tester" + str(i) + "/" + str(len(params2)+1)+".png"
#     remove(target, newtarget)