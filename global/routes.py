from PIL import Image
from flask import Flask, request,render_template
import Auto3
import numpy as np

app = Flask(__name__)

arr = []


@app.before_first_request
def before_first_request():
    # Initializes tensorflow session so that it can be used by the functions.
    global master
    master = Auto3.ImageEditorFunctions()





def CreateJPGUncompressedImage(pil_img, saveto):

    pil_img.save('./'+saveto+'.JPG', 'JPEG')


def CreatePNGforDataset(pil_img, saveto):

    pil_img.save('./static/'+saveto+'.png')


def CreateTIFFTimeline(pil_img, saveto):

    pil_img.save('./static/'+saveto+'.tiff', compression='jpeg')

def CreateCompressedJPG(pil_img, saveto):

    pil_img.save(saveto+'.jpg', compression='jpeg', quality=90, optimize = True)




@app.route('/changer/<int:num>')
def changeDatasetLatent(num):
    # Select the dataset latent corresponding with the num parameter.
    # .\Dataset\W_plus\w_plus(num).npy
    master.changeLatent("",num, 2)

@app.route('/changerIdent/<int:num>')
def changeIdentityLatent(num):
    # Select the identity latent corresponding with the num parameter.
    # .\CustomIdentities\Identity(num)\BaseIdentity\w_plus.npy
    master.changeLatent('',num, 3)

@app.route('/changerTrue/<path:path>')
def changeLatent(path):
    # Select the latent found in path.
    master.changeLatent(path,0, 4)




@app.route('/', methods=['GET', 'POST'])
def index():


    global start
    global master
    if request.method == 'POST':
        text = request.form["text"]
        text2 = request.form["neutral"]
        num1 = request.form["Strength"]
        num2 = request.form["Disentangle"]
        print(text)

        master.NeutralForm(text2)
        img2, _ = master.TargetEdit(text)
        img2, _ = master.ChangeAreaAffected(num2)
        img2, _ = master.ChangeStrength(num1)

        CreatePNGforDataset(img2, "1")
    return render_template("hello.html")



@app.route('/bringback')
def bringback():
    # Take the last identity in the identity list and use that to edit.
    global master
    master.SetBaseCode(master.ident[len(master.ident) - 1])
    return 'returned'

@app.route('/pop')
def pop():
    # Take the last Identity off the list.
    global master
    master.ident.pop()
    print("\n\n\n\n\n")
    print(str(len(master.ident)))
    return 'returned'


@app.route('/result')
def result():
    global master
    text = request.args.get('target')
    text2 = request.args.get('natural')
    num1 = request.args.get('strength')
    num2 = request.args.get('disentanglment')
    saveloc = request.args.get('save')

    img2, _ = master.EditImage(text2, text, num1, num2, True, False )

    CreatePNGforDataset(img2, saveloc)

    return render_template("hello.html")








@app.route('/dataset')
def dataset():
    # Generate changes for a dataset and normalises the face.
    # After the image is generated it is added onto an array so a timeline of the changes
    # at each stage can be scrolled through.
    global master
    global arr
    target = request.args.get('target')
    naturalPoint = request.args.get('natural')
    strength = request.args.get('strength')
    disentanglment = request.args.get('disentanglment')
    saveloc = request.args.get('save')
    print(target)
    img2, tmp = master.EditImage(naturalPoint, target, strength, disentanglment, True, False)
    arr.append(tmp)
    CreatePNGforDataset(img2, saveloc)
    return render_template("hello.html")

@app.route('/initdataset')
def initdataset():
    # Used for initializing an image to be used for normalization.
    # It also adds these results to the timeline array.
    global master
    global arr
    target = request.args.get('target')
    naturalPoint = request.args.get('natural')
    strength = request.args.get('strength')
    disentanglment = request.args.get('disentanglment')
    saveloc = request.args.get('save')
    img2, tmp = master.EditImage(naturalPoint, target, strength, disentanglment, True, False)
    arr.append(tmp)
    CreateCompressedJPG(img2, saveloc)
    return render_template("hello.html")

@app.route('/ChangeIdentity')
def ChangeIdentity():
    # Used to change Identity.
    # Saves as a compressed jpg and can be saved anywhere.
    # Does not contribute to the normalization timeline.

    # This function is unique as it doesn't save the codes after execution.
    # For example going from brown hair -> blonde. The next edit to ginger
    # will be brown -> ginger and not blonde -> ginger.

    #This also dose not save the identity to be used later.

    global master


    global arr

    target = request.args.get('target')
    naturalPoint = request.args.get('natural')
    strength = request.args.get('strength')
    disentanglment = request.args.get('disentanglment')
    saveloc = request.args.get('save')
    print(target)


    img2, _ = master.EditImage(naturalPoint, target, strength, disentanglment, False, False)

    CreateCompressedJPG(img2, saveloc)


    return render_template("hello.html")

@app.route('/ChangeIdentityPermOther')
def ChangeIdentityPermOther():

    # Used to change Identity.
    # Saves as a compressed jpg and can be saved anywhere.
    # Does not contribute to the normalization timeline.

    # This function saves the code to be used in the next edit.
    # For example going from brown hair -> blonde. The next edit to ginger
    # will be blonde -> ginger and not brown -> ginger.

    # This also dose not save the identity to be used later.

    global master
    global arr

    target = request.args.get('target')
    naturalPoint = request.args.get('natural')
    strength = request.args.get('strength')
    disentanglment = request.args.get('disentanglment')
    saveloc = request.args.get('save')
    print(target)


    img2, _ = master.EditImage(naturalPoint, target, strength, disentanglment, True, False)

    CreateCompressedJPG(img2, saveloc)


    return render_template("hello.html")





@app.route('/ChangeIdentityPerm')
def ChangeIdentityPerm():

    # Used to change Identity.
    # Saves as a compressed jpg and can be saved anywhere.
    # Does not contribute to the normalization timeline.

    # This function saves the code to be used in the next edit.
    # For example going from brown hair -> blonde. The next edit to ginger
    # will be blonde -> ginger and not brown -> ginger.

    # This also dose save the identity to be used later and adds to the list.


    global master
    global arr

    target = request.args.get('target')
    naturalPoint = request.args.get('natural')
    strength = request.args.get('strength')
    disentanglment = request.args.get('disentanglment')
    saveloc = request.args.get('save')
    print(target)


    img2, _ = master.EditImage(naturalPoint, target, strength, disentanglment, False, True)


    CreateCompressedJPG(img2, saveloc)


    return render_template("hello.html")













@app.route('/datasetresult')
def datasetresult():
    # This will convert our array into one large vertical image the user
    # that means the user can scroll down and view the changes as they are done in stages.

    global master
    global arr

    outputarr = arr[0]
    for i in range(len(arr)-1):
        print(outputarr)
        print(arr[i+1])
        outputarr = np.concatenate([outputarr,arr[i+1]])
    print(outputarr)
    img = Image.fromarray(outputarr)





    CreateTIFFTimeline(img, "Dataset Tester/result")
    master.SetBaseCode()
    return render_template("hello.html")



@app.route('/close')
def close():
    # Closes session freeing memory.
    global master
    master.close()





if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True, threaded=False)
# Threading would mean multiple sessions are created causing errors.



