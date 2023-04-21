import os
import shutil
from argparse import Namespace
import requests
from GetLatentInfo import main as GetLatentData
from copy import deepcopy
import tensorflow as tf

testgroup = 10
#CustomIdentities



# Non permanent change
Changeurl = "http://localhost:5000/ChangeIdentity"
# Permanent change and saves codes for later
ChangePermurl = "http://localhost:5000/ChangeIdentityPerm"
# Permanent change and dose not save codes for later
ChangePermOtherurl = "http://localhost:5000/ChangeIdentityPermOther"
# Close current session
close = "http://localhost:5000/close"

# Return to previously saved code on top of identity list.
returncode = "http://localhost:5000/bringback"
# Removes top code on identity list
popcode = "http://localhost:5000/pop"


# Classes goal to manage different sets of prompts to add.
# This means for each set added it will go through every combination.
# Creating a consistent file structure which can be used with match finder.
# Similar to a linked list.

class Identity():

    # IdentityPath - the base directory the results will be saved too.
    # Next - the next set of identity's
    # prev - the previous set of identity's
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

        # If this is the last link then a new identity is made the new next identity
        # and this link no longer last.
        # If it is not the last link it will recursively call the next link and add it there.

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

    def matchfinder(self, target:str, filenames = [], path = None):
        if (path == None):
                path = self.IdentityPath

        #loop through input list and through file structure to find match

        for files in os.listdir(path):
            filepath = os.path.join(path, files)
            if (os.path.isdir(filepath)):

                filenames = self.matchfinder(target,filenames, filepath)


            if (files.endswith(".jpg") and files == target+".jpg"):

                filenames.append(filepath)

        # Will return a list of paths to matching identitys images.
        return filenames


    def callprompts(self, promlist = []):
        identcopy = deepcopy(self.ident)

        # Loops through each combination of identitys in the link.
        # Save path for first identity is equal to IdentityPath attribute
        # The next set adds its name to the previous identitys path.
        # Prompt 1 -> .\CustomIdentities\Identity1\NewIdentitys\Short hair.jpg
        # Prompt 2 -> .\CustomIdentities\Identity1\NewIdentitys\Short hair\brown.jpg

        # As it goes from one prompt list to another recursively,
        # it will save the code of the edit to return to without having to reload the latent.
        # As it executes through the list it will stop saving at the second last.
        # At the last set of prompts it will loop through the list without saving as their are no further edits from that point.
        # This saves time from reloading the code.

        # After it loops through the last set of prompts it then pops the last saved code and reloads the code before that.
        # EG short hair -> brown -> no bangs(saved) -> big lips -> (closed eyes - open eyes - natural eyes)
        # Instead of re doing hair -> brown -> no bangs, we can jump to no bangs be reloading the code:
        # short hair -> brown -> no bangs
        # then -> thin lips and looping through closed eyes - open eyes - natural eyes

        #This is done recursivley so after each prompt in the list is done it will pop again
        # Reloading to the one before that just popped one.

        if (self.first == True):
            temp = deepcopy(self.ident[0])
            temp['strength'] = '0'
            temp['save'] = self.IdentityPath + '/' + temp['save']
            r = requests.get(ChangePermurl, params=temp)
            if not os.path.exists(self.IdentityPath):
                os.makedirs(self.IdentityPath)

        if self.last == True and self.first == True:
            # If only one set of prompts it will loop through without saving anything.
            for num, identitys in enumerate(self.ident):
                self.ident[num]['save']= self.IdentityPath + '/' + self.ident[num]['save']
                r = requests.get(Changeurl, params=identitys)


        elif self.last == True:
            for num, identitys in enumerate(self.ident):
                #Loops through without saving to save time.
                self.ident[num]['save'] = promlist[len(promlist) - 1]['save'] + '/' + self.ident[num]['save']
                r = requests.get(Changeurl, params=identitys)

            promlist.pop()
            self.ident = identcopy

        else:
            for i in range(len(self.ident)):
                if (self.first == True):
                    self.ident[i]['save']= self.IdentityPath + '/' + self.ident[i]['save']
                else:
                    # Using previous save location to save from.
                    self.ident[i]['save'] = promlist[len(promlist) - 1]['save'] + '/' + self.ident[i]['save']

                promlist.append(self.ident[i])

                if(self.next.last == False):

                    r = requests.get(ChangePermurl, params=self.ident[i])

                else:

                    r = requests.get(ChangePermOtherurl, params=self.ident[i])


                if not os.path.exists(self.ident[i]['save']):
                    os.makedirs(self.ident[i]['save'])
                self.next.callprompts(promlist)

                r = requests.get(returncode)



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
def main():
    hair = [

        {'natural': 'face with no hair', 'target': 'face with short hair', 'strength': '10', 'disentanglment': '18',
         'save': 'short hair'},
        {'natural': 'face with no hair', 'target': 'face with long hair', 'strength': '7', 'disentanglment': '18',
         'save': 'long hair'},
        {'natural': 'face with no hair', 'target': 'face with bowlcut hair', 'strength': '5', 'disentanglment': '18',
         'save': 'bowlcut hair'},
        {'natural': 'face with no hair', 'target': 'face with comb over hair', 'strength': '16', 'disentanglment': '18',
         'save': 'comb over hair'},
        {'natural': 'face with no hair', 'target': 'face with afro hair', 'strength': '10', 'disentanglment': '18',
         'save': 'afro hair'},
        {'natural': 'face with no hair', 'target': 'face with haircut', 'strength': '5', 'disentanglment': '18',
         'save': 'haircut hair'},
        {'natural': 'face with no hair', 'target': 'face with curly hair', 'strength': '5.5', 'disentanglment': '18',
         'save': 'curly hair'},
    ]

    hair2 = [{'natural': 'face with hair', 'target': 'face with brown hair', 'strength': '3', 'disentanglment': '14',
              'save': 'brown'},
             {'natural': 'face with hair', 'target': 'face with blonde hair', 'strength': '2', 'disentanglment': '14',
              'save': 'blonde'},
             {'natural': 'face with hair', 'target': 'face with grey hair', 'strength': '3', 'disentanglment': '14',
              'save': 'grey'},
             {'natural': 'face with hair', 'target': 'face with white hair', 'strength': '5', 'disentanglment': '14',
              'save': 'white'},
             {'natural': 'face with hair', 'target': 'face with red hair', 'strength': '3', 'disentanglment': '14',
              'save': 'red'},
             {'natural': 'face with hair', 'target': 'face with ginger hair', 'strength': '5', 'disentanglment': '14',
              'save': 'ginger'},

             ]

    hair3 = [
        {'natural': 'face with hair', 'target': 'face with bangs', 'strength': '-3', 'disentanglment': '16',
         'save': 'no bangs'},

        {'natural': 'face with hair', 'target': 'face with fringe', 'strength': '3', 'disentanglment': '18',
         'save': 'fringe'},
        {'natural': 'face with hair', 'target': 'face with no hair', 'strength': '0', 'disentanglment': '18',
         'save': 'none'},
        {'natural': 'face with hair', 'target': 'face with hairline', 'strength': '-3', 'disentanglment': '18',
         'save': 'better hairline'},
        {'natural': 'face with hair', 'target': 'face with bangs', 'strength': '4', 'disentanglment': '18',
         'save': 'bangs'},
    ]

    hair4 = [
        {'natural': 'face', 'target': 'facial hair', 'strength': '15', 'disentanglment': '14.6', 'save': 'beard'},
        {'natural': 'face', 'target': 'facial hair', 'strength': '12', 'disentanglment': '14.6',
         'save': 'strong facial hair'},
        {'natural': 'face', 'target': 'facial hair', 'strength': '9', 'disentanglment': '14.6',
         'save': 'medium facial hair'},
        {'natural': 'face', 'target': 'facial hair', 'strength': '7.5', 'disentanglment': '14.6',
         'save': 'light facial hair'},
        {'natural': 'face', 'target': 'facial hair', 'strength': '6', 'disentanglment': '14.6',
         'save': 'very light facial hair'},
        {'natural': 'face', 'target': 'facial hair', 'strength': '0', 'disentanglment': '14.6', 'save': 'no facial hair'},
        {'natural': 'face', 'target': 'face with stubble', 'strength': '6', 'disentanglment': '11', 'save': 'stubble'},
        {'natural': 'face', 'target': 'face with stubble', 'strength': '9', 'disentanglment': '11',
         'save': 'heavy stubble'},
    ]

    hair5 = [
        {'natural': 'face', 'target': 'face big lips', 'strength': '5', 'disentanglment': '13', 'save': 'big lips'},
        {'natural': 'face', 'target': 'face big lips', 'strength': '-5', 'disentanglment': '13', 'save': 'thin lips'},
        {'natural': 'no eyebrows', 'target': 'eyebrows', 'strength': '0', 'disentanglment': '13',
         'save': 'neutral lips'},

    ]

    hair6 = [
        {'natural': 'face', 'target': 'face shut eyes', 'strength': '6.28', 'disentanglment': '10',
         'save': 'closed eyes'},
        #{'natural': 'face', 'target': 'face left winking eye', 'strength': '13', 'disentanglment': '10',
         #'save': 'left winking eye'},
        {'natural': 'face', 'target': 'face wide eyes', 'strength': '8', 'disentanglment': '10', 'save': 'wide eyes'},
        {'natural': 'face', 'target': 'face left winking eye', 'strength': '0', 'disentanglment': '10',
         'save': 'normal eyes'},

    ]
    hair7 = [
        {'natural': 'no eyebrows', 'target': 'eyebrows', 'strength': '1', 'disentanglment': '17',
         'save': 'thick eyebrows'},
        {'natural': 'no eyebrows', 'target': 'eyebrows', 'strength': '-1', 'disentanglment': '17',
         'save': 'no eyebrows'},
        {'natural': 'no eyebrows', 'target': 'eyebrows', 'strength': '0', 'disentanglment': '17',
         'save': 'neutral eyebrows'},

    ]
    hair8 = [
        {'natural': 'face', 'target': 'face big ears', 'strength': '4', 'disentanglment': '12', 'save': 'big ears'},
        {'natural': 'face', 'target': 'face big ears', 'strength': '-3', 'disentanglment': '12', 'save': 'small ears'},
        {'natural': 'face', 'target': 'face big ears', 'strength': '0', 'disentanglment': '12', 'save': 'neutral ears'},

    ]
    hair9 = [
        {'natural': 'no nose', 'target': 'thin nose', 'strength': '-6', 'disentanglment': '9.5', 'save': 'wide nose'},
        {'natural': 'no nose', 'target': 'thin nose', 'strength': '6', 'disentanglment': '9.5', 'save': 'thin nose'},
        {'natural': 'no nose', 'target': 'thin nose', 'strength': '0', 'disentanglment': '9.5', 'save': 'neutral nose'},

    ]

    # defined nose

    hair10 = [
        {'natural': 'face', 'target': 'face 50 years old', 'strength': '5', 'disentanglment': '13',
         'save': '50 years old'},
        {'natural': 'face', 'target': 'face 10 years old', 'strength': '4', 'disentanglment': '13',
         'save': '10 years old'},
        {'natural': 'face', 'target': 'face 20 years old', 'strength': '5', 'disentanglment': '13',
         'save': '20 years old'},
        {'natural': 'face', 'target': 'face 30 years old', 'strength': '5', 'disentanglment': '13',
         'save': '30 years old'},
        {'natural': 'face', 'target': 'face 40 years old', 'strength': '5', 'disentanglment': '13',
         'save': '40 years old'},

        {'natural': 'face', 'target': 'face 60 years old', 'strength': '6', 'disentanglment': '13',
         'save': '60 years old'},
        {'natural': 'face', 'target': 'face 70 years old', 'strength': '8', 'disentanglment': '13',
         'save': '70 years old'},
    ]

    hair11 = [
        {'natural': 'face', 'target': 'happy', 'strength': '3', 'disentanglment': '10', 'save': 'happy expression'},
        {'natural': 'face', 'target': 'sad', 'strength': '3', 'disentanglment': '10', 'save': 'sad expression'},
        {'natural': 'face', 'target': 'angry', 'strength': '3', 'disentanglment': '10', 'save': 'angry expression'},
        {'natural': 'face', 'target': 'shocked', 'strength': '4', 'disentanglment': '10', 'save': 'shocked expression'},
        {'natural': 'face', 'target': 'scared', 'strength': '3.5', 'disentanglment': '10', 'save': 'scared expression'},
        {'natural': 'face', 'target': 'disgust', 'strength': '3', 'disentanglment': '10', 'save': 'disgust expression'},
        {'natural': 'face', 'target': 'neutral', 'strength': '0', 'disentanglment': '10', 'save': 'neutral expression'},
    ]

    # add stright white teeth

    # fat thi5
    hair12 = [
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

    # glasses and sunglassses
    hair13 = [
        {'natural': 'face', 'target': 'earings', 'strength': '9', 'disentanglment': '9.2', 'save': 'earings'},
        {'natural': 'face', 'target': 'earings', 'strength': '0', 'disentanglment': '10.4', 'save': 'no earings'},
        {'natural': 'face', 'target': 'face with glasses', 'strength': '6.47', 'disentanglment': '10.8',
         'save': 'glasses'},

    ]

    for i in range(testgroup):

        # Defines save location using iterator
        current = i+1
        changelatent = "http://localhost:5000/changerIdent/"+str(current)
        path = "./CustomIdentities/Identity" + str(current)
        if not os.path.exists(path):
             os.makedirs(path)
        basepath = path+"/BaseIdentity"
        if not os.path.exists(basepath):
             os.makedirs(basepath)

        #Copies matching normalized result into identities latent info file.
        shutil.copy("./static/Dataset Tester"+str(i)+"/finallatent.pt",basepath+"/latents.pt")
        ex = Namespace(real=True, dataset_name="ffhq", IdentityNum=str(i+1), Loadtype=3)
        GetLatentData(ex)

        # Loads latent to be used
        requests.get(changelatent)
        print("using this")
        hairpath = path + "/NewIdentitys"


        # Deep copy as not to bring identity 1's file path into identity 2's
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

        # Switching latents can be memory intensive so freeing this memory avoids OOM's
        requests.get(close)

if __name__ == "__main__":
    main()