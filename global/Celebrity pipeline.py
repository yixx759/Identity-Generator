import os
from argparse import Namespace

import requests
from GetLatentInfo import main as GetGUIData
from GetLatent import main as GetLatent
from CustomiseCharacter import Identity
from copy import deepcopy


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

express3 = [
        {'natural': 'face', 'target': 'earings', 'strength': '11', 'disentanglment': '12.4', 'save': 'earings'},
        {'natural': 'face', 'target': 'earings', 'strength': '0', 'disentanglment': '10.4', 'save': 'no earings'},
        {'natural': 'face', 'target': 'face with glasses', 'strength': '6.47', 'disentanglment': '14.8',
         'save': 'glasses'},
]

express4 = [{'natural': 'face with hair', 'target': 'face with brown hair', 'strength': '7', 'disentanglment': '13',
              'save': 'brown'},
             {'natural': 'face with hair', 'target': 'face with blonde hair', 'strength': '4', 'disentanglment': '25',
              'save': 'blonde'},
             {'natural': 'face with hair', 'target': 'face with grey hair', 'strength': '8', 'disentanglment': '20',
              'save': 'grey'},
             {'natural': 'face with hair', 'target': 'face with white hair', 'strength': '10', 'disentanglment': '10',
              'save': 'white'},
             {'natural': 'face with hair', 'target': 'face with red hair', 'strength': '5', 'disentanglment': '15',
              'save': 'red'},
             {'natural': 'face with hair', 'target': 'face with ginger hair', 'strength': '8', 'disentanglment': '25',
              'save': 'ginger'},

             ]

express5 = [
        {'natural': 'person', 'target': 'fat person', 'strength': '1.5', 'disentanglment': '19.3',
         'save': 'fat person'},
        {'natural': 'person', 'target': 'fat person', 'strength': '0.5', 'disentanglment': '19.3',
         'save': 'more overwieght person'},
        {'natural': 'person', 'target': 'fat person', 'strength': '0.25', 'disentanglment': '19.3',
         'save': 'overwieght person'},
        {'natural': 'person', 'target': 'fat person', 'strength': '0', 'disentanglment': '19.3',
         'save': 'neutral weight person'},
        {'natural': 'person', 'target': 'fat person', 'strength': '-0.25', 'disentanglment': '19.3',
         'save': 'underwieght person'},
        {'natural': 'person', 'target': 'fat person', 'strength': '-0.75', 'disentanglment': '19.3',
         'save': 'more underwieght person'},
        {'natural': 'person', 'target': 'fat person', 'strength': '-1', 'disentanglment': '19.3',
         'save': 'skinny person'},
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
        requests.get(changelatent)
        expressPath = path + "/baseExpressions"
        master = Identity(expressPath,deepcopy(express5),None,None )
        master.add(deepcopy(express4))
        master.add(deepcopy(express1))
        master.add(deepcopy(express2))
        master.callprompts()








if __name__ == "__main__":
     CelebName = ["Beyonce" ]
     #createFiles(CelebName)
     main(CelebName)