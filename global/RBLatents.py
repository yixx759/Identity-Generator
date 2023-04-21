import subprocess

import requests

from RemoveBackground import main as remove
from GetLatent import main as getlatent


testgroup = 10
promptcount = 15

# This program will remove the background of the last image to be edited.
# Adding a white background.
# Then encodes the image which has the affect of generating the latent while also making the face more normalised
# fixing the artifacts.



# This batch file will activate the stable diffusion api

subprocess.Popen("start Activate.bat", shell=True)



while True:
        try:
            r = requests.get(url=f"http://127.0.0.1:7860/")
            print(r)
            if (r.status_code == 200):
                break
        except:
            print("no connection")



for i2 in range(testgroup):


        target = "F:/Challenges/StyleCLIP/global/static/Dataset Tester" + str(i2) + "/" + str(promptcount)+".png"
        newtarget = "F:/Challenges/StyleCLIP/global/static/Dataset Tester" + str(i2) + "/" + str(promptcount+1)+".png"
        remove(target, newtarget)
        getlatent("F:/Challenges/StyleCLIP/global/static/Dataset Tester" + str(i2) + "/" + "finallatent.pt",newtarget)