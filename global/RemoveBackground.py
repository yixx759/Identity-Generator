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


    backpath = "./static/Background/white.png"

    background = Image.open(backpath).convert("RGBA")

    #background.save(output)
    print("Heeere")
    im = Image.open(filename).convert("RGBA")
    # background = Image.new("RGBA", im.size)
    # background.alpha_composite(temp)
    #background.alpha_composite(im)
    #im = im.convert("RGBA")
    #im.save(output)
    #background.paste(im, (0,0))

    background.paste(im, (0,0), im)

    #background.save(output)
    #remove alpha for encodeing
    background.convert("RGB").save(output)

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



    main(".\here\yum.png","./here/newyum.jpg")

