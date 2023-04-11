import os
from argparse import Namespace

import requests
from GetGUIData import main as GetGUIData
from GetLatent import main as GetLatent
from CustomiseCharacter import Identity
from copy import deepcopy
from Interpalator_tool.Interp import main as GetGif

express1 =[
        {'natural':'face', 'target':'happy','strength':'3','disentanglment':'10','save':'happy expression'},
        {'natural':'face', 'target':'sad','strength':'3','disentanglment':'10','save':'sad expression'},
        {'natural':'face', 'target':'angry','strength':'3','disentanglment':'10','save':'angry expression'},
        {'natural':'face', 'target':'shocked','strength':'4','disentanglment':'10','save':'shocked expression'},
        {'natural':'face', 'target':'scared','strength':'3.5','disentanglment':'10','save':'scared expression'},
        {'natural':'face', 'target':'disgust','strength':'3','disentanglment':'10','save':'disgust expression'},
        {'natural':'face', 'target':'neutral','strength':'0','disentanglment':'10','save':'neutral expression'},
        ]

express2 =[
        {'natural':'face', 'target':'face shut eyes','strength':'6.28','disentanglment':'10','save':'closed eyes'},
        #{'natural':'face', 'target':'face left winking eye','strength':'13','disentanglment':'10','save':'left winking eye'},
        {'natural':'face', 'target':'face wide eyes','strength':'8','disentanglment':'10','save':'wide eyes'},
        {'natural':'face', 'target':'face left winking eye','strength':'0','disentanglment':'10','save':'normal eyes'},

        ]


def createFiles(list):

     start = "./Celebrities/"
     if not os.path.exists(start):
          os.makedirs(start)

     for names in list:
          path = os.path.join(start,names)
          print(path)
          if not os.path.exists(path):
               os.makedirs(path)
          basepath = os.path.join(path,"BaseIdentity")
          if not os.path.exists(basepath):
               os.makedirs(basepath)




def main(namelist):

     for name in namelist:


        start = "./Celebrities/"
        path = os.path.join(start, name)

        basepath = os.path.join(path,"BaseIdentity")



        changelatent = "http://localhost:5000/changerTrue/"+basepath

        GetLatent(basepath+"/latents.pt",basepath+"/0.jpg", basepath+"/1.jpg")

        ex = Namespace(real=True, dataset_name="ffhq", IdentityPath=basepath, Loadtype=4)
        GetGUIData(ex)




        #    print("using this")
        requests.get(changelatent)

        expressPath = path + "/baseExpressions"
        print("\n\n\n\n\n\nHEEEEEEEEEEEEEEEERRRRRRRRRRRRRRREEEEEEEEEE\n\n\n\n\n\n\n\n")
        master = Identity(expressPath,deepcopy(express1),None,None )
        master.add(deepcopy(express2))
        master.callprompts()
        list1 = master.matchfinder("closed eyes",[])
        list2 = master.matchfinder("normal eyes", [])
        print(list1)
        print(list2)
        for i in range(len(list2)):
            getpath = os.path.dirname(list1[i])
            print(getpath)
            GetGif(list2[i],list1[i], getpath+"/blink")
            GetGif(list1[i],list2[i], getpath+"/open")






if __name__ == "__main__":
     CelebName = ["Kanye", "Taylor", "GAGA"]
     #createFiles(CelebName)
     main(CelebName)