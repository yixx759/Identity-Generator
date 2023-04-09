import os
import shutil
from argparse import Namespace
import requests
from GetGUIDataNewIdentity import main as GetGUIData
from copy import deepcopy
import tensorflow as tf

testgroup = 10
#CustomIdentities

hair = [

            {'natural':'face with no hair', 'target':'face with short hair','strength':'10','disentanglment':'18','save':'short hair'},
            {'natural':'face with no hair', 'target':'face with long hair','strength':'7','disentanglment':'18','save':'long hair'},
            {'natural':'face with no hair', 'target':'face with bowlcut hair','strength':'5','disentanglment':'18','save':'bowlcut hair'},
            {'natural':'face with no hair', 'target':'face with comb over hair','strength':'16','disentanglment':'18','save':'comb over hair'},
            {'natural':'face with no hair', 'target':'face with afro hair','strength':'10','disentanglment':'18','save':'afro hair'},
            {'natural':'face with no hair', 'target':'face with haircut','strength':'5','disentanglment':'18','save':'haircut hair'},
            {'natural':'face with no hair', 'target':'face with curly hair','strength':'5.5','disentanglment':'18','save':'curly hair'},
        ]


hair2 = [{'natural':'face with hair', 'target':'face with brown hair','strength':'3','disentanglment':'14','save':'brown'},
            {'natural':'face with hair', 'target':'face with blonde hair','strength':'2','disentanglment':'14','save':'blonde'},
            {'natural':'face with hair', 'target':'face with grey hair','strength':'3','disentanglment':'14','save':'grey'},
            {'natural':'face with hair', 'target':'face with white hair','strength':'5','disentanglment':'14','save':'white'},
            {'natural':'face with hair', 'target':'face with red hair','strength':'3','disentanglment':'14','save':'red'},
            {'natural':'face with hair', 'target':'face with ginger hair','strength':'5','disentanglment':'14','save':'ginger'},

            ]

hair3 =[
        {'natural':'face with hair', 'target':'face with bangs','strength':'-3','disentanglment':'16','save':'no bangs'},

        {'natural':'face with hair', 'target':'face with fringe','strength':'3','disentanglment':'18','save':'fringe'},
        {'natural':'face with hair', 'target':'face with no hair','strength':'0','disentanglment':'18','save':'none'},
        {'natural':'face with hair', 'target':'face with hairline','strength':'-3','disentanglment':'18','save':'better hairline'},
        {'natural':'face with hair', 'target':'face with bangs','strength':'4','disentanglment':'18','save':'bangs'},
        ]

hair4 =[
        {'natural':'face without facial hair', 'target':'face with with beard','strength':'13','disentanglment':'22','save':'beard'},
        {'natural':'face without facial hair', 'target':'face with with beard','strength':'10','disentanglment':'22','save':'strong facial hair'},
        {'natural':'face without facial hair', 'target':'face with with beard','strength':'8','disentanglment':'22','save':'medium facial hair'},
        {'natural':'face without facial hair', 'target':'face with with beard','strength':'7.5','disentanglment':'22','save':'light facial hair'},
        {'natural':'face without facial hair', 'target':'face with with beard','strength':'7','disentanglment':'22','save':'very light facial hair'},
        {'natural':'face without facial hair', 'target':'face with with beard','strength':'0','disentanglment':'22','save':'no facial hair'},
        {'natural':'face', 'target':'face with stubble','strength':'6','disentanglment':'11','save':'stubble'},
        {'natural':'face', 'target':'face with stubble','strength':'9','disentanglment':'11','save':'heavy stubble'},
        ]

hair5 =[
        {'natural':'face', 'target':'face big lips','strength':'5','disentanglment':'13','save':'big lips'},
        {'natural':'face', 'target':'face big lips','strength':'-5','disentanglment':'13','save':'thin lips'},
        {'natural':'no eyebrows', 'target':'eyebrows','strength':'0','disentanglment':'13','save':'neutral lips'},

        ]

hair6 =[
        {'natural':'face', 'target':'face shut eyes','strength':'6.28','disentanglment':'10','save':'closed eyes'},
        {'natural':'face', 'target':'face left winking eye','strength':'13','disentanglment':'10','save':'left winking eye'},
        {'natural':'face', 'target':'face wide eyes','strength':'8','disentanglment':'10','save':'wide eyes'},
        {'natural':'face', 'target':'face left winking eye','strength':'0','disentanglment':'10','save':'normal eyes'},

        ]
hair7 =[
        {'natural':'no eyebrows', 'target':'eyebrows','strength':'1','disentanglment':'17','save':'thick eyebrows'},
        {'natural':'no eyebrows', 'target':'eyebrows','strength':'-1','disentanglment':'17','save':'no eyebrows'},
        {'natural':'no eyebrows', 'target':'eyebrows','strength':'0','disentanglment':'17','save':'neutral eyebrows'},

        ]
hair8 =[
        {'natural':'face', 'target':'face big ears','strength':'4','disentanglment':'12','save':'big ears'},
        {'natural':'face', 'target':'face big ears','strength':'-3','disentanglment':'12','save':'small ears'},
        {'natural':'face', 'target':'face big ears','strength':'0','disentanglment':'12','save':'neutral ears'},

        ]
hair9 =[
        {'natural':'no nose', 'target':'thin nose','strength':'-6','disentanglment':'9.5','save':'wide nose'},
        {'natural':'no nose', 'target':'thin nose','strength':'6','disentanglment':'9.5','save':'thin nose'},
        {'natural':'no nose', 'target':'thin nose','strength':'0','disentanglment':'9.5','save':'neutral nose'},

        ]

#defined nose


hair10 =[
        {'natural':'face', 'target':'face 50 years old','strength':'5','disentanglment':'13','save':'50 years old'},
        {'natural':'face', 'target':'face 10 years old','strength':'4','disentanglment':'13','save':'10 years old'},
        {'natural':'face', 'target':'face 20 years old','strength':'5','disentanglment':'13','save':'20 years old'},
        {'natural':'face', 'target':'face 30 years old','strength':'5','disentanglment':'13','save':'30 years old'},
        {'natural':'face', 'target':'face 40 years old','strength':'5','disentanglment':'13','save':'40 years old'},

        {'natural':'face', 'target':'face 60 years old','strength':'6','disentanglment':'13','save':'60 years old'},
        {'natural':'face', 'target':'face 70 years old','strength':'8','disentanglment':'13','save':'70 years old'},
        ]

hair11 =[
        {'natural':'face', 'target':'happy','strength':'3','disentanglment':'10','save':'happy expression'},
        {'natural':'face', 'target':'sad','strength':'3','disentanglment':'10','save':'sad expression'},
        {'natural':'face', 'target':'angry','strength':'3','disentanglment':'10','save':'angry expression'},
        {'natural':'face', 'target':'shocked','strength':'4','disentanglment':'10','save':'shocked expression'},
        {'natural':'face', 'target':'scared','strength':'3.5','disentanglment':'10','save':'scared expression'},
        {'natural':'face', 'target':'disgust','strength':'3','disentanglment':'10','save':'disgust expression'},
        {'natural':'face', 'target':'neutral','strength':'0','disentanglment':'10','save':'neutral expression'},
        ]

#add stright white teeth

#fat thi5
hair12 =[
        {'natural':'person', 'target':'fat person','strength':'5','disentanglment':'18.4','save':'fat person'},
        {'natural':'person', 'target':'fat person','strength':'4.5','disentanglment':'18.4','save':'more overwieght person'},
        {'natural':'person', 'target':'fat person','strength':'4.2','disentanglment':'18.4','save':'overwieght person'},
        {'natural':'person', 'target':'fat person','strength':'0','disentanglment':'18.4','save':'neutral weight person'},
        {'natural':'person', 'target':'fat person','strength':'-4.2','disentanglment':'18.4','save':'underwieght person'},
        {'natural':'person', 'target':'fat person','strength':'-4.5','disentanglment':'18.4','save':'more underwieght person'},
        {'natural':'person', 'target':'fat person','strength':'-5.3','disentanglment':'18.4','save':'skinny person'},
        ]

#glasses and sunglassses
hair13 = [
        {'natural':'face', 'target':'earings','strength':'5','disentanglment':'12.4','save':'earings'},
        {'natural':'face', 'target':'earings','strength':'0','disentanglment':'18.4','save':'no earings'},
        {'natural':'face', 'target':'face with glasses','strength':'6.47','disentanglment':'14.8','save':'glasses'},



]


#by either creating a 0 strength prompt or saving code using init of default starting image and add at first node


# #use get dt2 codes load codes instead of latents
#
# #facial hair add to the end of bangs and no bangs and one that has no cahanges already
#
Changeurl = "http://localhost:5000/ChangeIdentity"
ChangePermurl = "http://localhost:5000/ChangeIdentityPerm"
ChangePermOtherurl = "http://localhost:5000/ChangeIdentityPermOther"
close = "http://localhost:5000/close"

returncode = "http://localhost:5000/bringback"
popcode = "http://localhost:5000/pop"

#maybe have last set of prompt not permchange just temporary

class Identity():
    def __init__(self, IdentityPath, ident, next: 'Identity', prev: 'Identity'):
        self.ident = ident

        self.prev = prev
        self.next = next
        if (prev == None):
            self.first = True
            self.IdentityPath = IdentityPath
        else:
            self.first = False
        self.last = True


    def add(self, newident ):
        if self.next == None:
            self.next = Identity(None,newident,None, self)
            self.last = False
        else:
            self.next.add(newident)

    def testprint(self, previous = "Here:"):

        if self.next == None:
            print(previous + str(self.ident))
        else:
            newprev = previous + str(self.ident)
            self.next.testprint(newprev)

    def callprompts(self, promlist = []):
        identcopy = deepcopy(self.ident)
        #
        #
        # #to refactor if last node then 2 diffrent loops if not normal loop, if last do non perm change on every identity
        # #go through each prompt using a loop and each one added is nested in the next, except the last one gose though all at once
        # #see if codes or dt can be saved and cached
        #
        if (self.first == True):
            temp = deepcopy(self.ident[0])
            temp['strength'] = '0'
            temp['save'] = self.IdentityPath + '/' + temp['save']
            r = requests.get(ChangePermurl, params=temp)
            if not os.path.exists(self.IdentityPath):
                os.makedirs(self.IdentityPath)

        if self.last == True:
            for num, identitys in enumerate(self.ident):
                print("Entred")
                self.ident[num]['save'] = promlist[len(promlist) - 1]['save'] + '/' + self.ident[num]['save']
                r = requests.get(Changeurl, params=identitys)
                print(r.url)

            print(promlist)
            #
            #print('reset')
            #tf.reset_default_graph()
            #print("new session")
            #requests.get(close)
            #requests.get(changelatent)
            promlist.pop()
            self.ident = identcopy
        else:
            for i in range(len(self.ident)):

                if (self.first == True):
                    self.ident[i]['save']= self.IdentityPath + '/' + self.ident[i]['save']
                else:

                    self.ident[i]['save'] = promlist[len(promlist) - 1]['save'] + '/' + self.ident[i]['save']
                promlist.append(self.ident[i])


                if(self.next.last == False):
                    print("\n\n\n\npromptlist")
                    print(promlist)
                    r = requests.get(ChangePermurl, params=self.ident[i])
                    print(self.ident[i]['target'])
                    print(r.url)
                else:
                    print(promlist)
                    r = requests.get(ChangePermOtherurl, params=self.ident[i])
                    print(self.ident[i]['target'])
                    print(r.url)

                if not os.path.exists(self.ident[i]['save']):
                    os.makedirs(self.ident[i]['save'])
                self.next.callprompts(promlist)

                r = requests.get(returncode)

                print(r.url)


#applying twice maybe pop twice short hair is beinng applied twice
            #add pop url

            r = requests.get(popcode)
            print("popped")
            if(len(promlist)>0):
                promlist.pop()

            self.ident = identcopy











#create last bool to optamise

#deep copy before sending in as well
#
#
for i in range(testgroup):

#
    current = i+1
    changelatent = "http://localhost:5000/changerIdent/"+str(current)
    path = "./CustomIdentities/Identity" + str(current)
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
    #check if codes is only thing needed
    # deep copy before prompts sending in as well
    # hairtemp = deepcopy hair if way to avoid find in class
    master = Identity(hairpath,deepcopy(hair), None, None)

    master.add(deepcopy(hair2))
    master.add(deepcopy(hair3))

    master.add(deepcopy(hair5))
    master.add(deepcopy(hair6))
    master.add(deepcopy(hair7))
    master.add(deepcopy(hair8))
    master.add(deepcopy(hair9))
    master.add(deepcopy(hair10))
    master.add(deepcopy(hair11))
    master.add(deepcopy(hair12))
    master.add(deepcopy(hair13))
    master.add(deepcopy(hair4))

    master.callprompts()


    requests.get(close)