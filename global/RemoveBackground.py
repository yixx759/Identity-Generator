import requests
import base64
from PIL import Image
import subprocess

def main(input, output):


    #"F:/Challenges/StableTest/0.jpg"
    with open(input, "rb") as imgfile:
        my_string = base64.b64encode(imgfile.read())

    my_string = my_string.decode('UTF-8')

    my_string = "data:image/png;base64," + my_string

    prompt = {

        "image": my_string,
        "remove_background": "u2net_human_seg"
    }
    r = requests.post(url=f"http://127.0.0.1:7860/sdapi/v1/extra-single-image", json=prompt)



    f = base64.b64decode(r.json()["image"])

    filename = output

    with open(filename, "wb") as a:
        a.write(f)

    im = Image.open(output)
    jpg = im.convert('RGB')
    jpg.save(output)


if __name__ == "__main__":
    subprocess.Popen("start Activate.bat", shell=True)



    while True:
        try:
            r = requests.get(url=f"http://127.0.0.1:7860/")
            print(r)
            if (r.status_code == 200):
                break
        except:
            r = 0



    main(".\here\yum.jpg","./here/newyum.jpg")

