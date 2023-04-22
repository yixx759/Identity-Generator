import requests
import base64
from PIL import Image
import subprocess

def main(input, output):
    # This program will use stable diffusion to remove the background
    # then add this image with a transparent image to a white background.
    # It is saved as RGB vs RGBA as any transparency information will cause the encoder not to work.
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
    print("Heeere")
    im = Image.open(filename).convert("RGBA")
    background.paste(im, (0,0), im)
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

