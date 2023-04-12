from PIL import Image
from flask import Flask, request,render_template
import Auto3
import numpy as np
from Inference import loadtype


app = Flask(__name__)
start = False
arr = []
First = True


@app.before_first_request
def before_first_request():
    global master
    master = Auto3.PlayInteractively()



def serve_pil_image(pil_img,saveto):
    print("here!!!!!!!!!!!!!!!")
    pil_img.save('./static/'+saveto+'.JPG', 'JPEG')
    img1 = Image.open('./data/ffhq/0.jpg')
    img1.save('./static/0.JPG', 'JPEG')

def serve_pil_image2(pil_img,saveto):
    print("here!!!!!!!!!!!!!!!")
    pil_img.save('./static/'+saveto+'.png')


def serve_pil_image3(pil_img,saveto):
    print("here!!!!!!!!!!!!!!!")
    pil_img.save('./static/'+saveto+'.tiff', compression='jpeg')
    #img1 = Image.open('./data/ffhq/0.jpg')
    #img1.save('./static/0.JPG', 'JPEG')
    #
def serve_pil_image4(pil_img,saveto):
    print("here!!!!!!!!!!!!!!!")
    pil_img.save(saveto+'.jpg', compression='jpeg', quality=78, optimize = True)
    #img1 = Image.open('./data/ffhq/0.jpg')
    #img1.save('./static/0.JPG', 'JPEG')

@app.route('/change/<int:num>')
def changephoto(num):
    master.openfn(str(num))

@app.route('/changer/<int:num>')
def changelatent(num):
    master.changeLatent("",num, 2)

@app.route('/changerIdent/<int:num>')
def changeIdentity(num):
    master.changeLatent('',num, 3)

@app.route('/changerTrue/<path:path>')
def changeTrue(path):
    print('\n\n\n')
    print('\n\n\nlabel')
    print(path)
    master.changeLatent(path,0, 4)





@app.route('/bringback')
def bringback():
    global master
    master.SetInit(master.ident[len(master.ident)-1])
    return 'returned'

@app.route('/pop')
def pop():
    global master
    master.ident.pop()
    print("\n\n\n\n\n")
    print(str(len(master.ident)))
    return 'returned'




@app.route('/result')
def result():
    global master
    #master = Auto2.PlayInteractively()
    text = request.args.get('target')
    text2 = request.args.get('natural')
    num1 = request.args.get('strength')
    num2 = request.args.get('disentanglment')
    saveloc = request.args.get('save')
    print(text)
    master.text_n(text2)
    img2 = master.ChangeAlpha(num1)
    img2 = master.ChangeBeta(num2)
    img2tmp = master.text_t(text)
    img2 = img2tmp[0]
    print("22here!!!!!!!!!!!!!!!")
    serve_pil_image(img2, saveloc)
    master.SetInit()
    return render_template("hello.html")

@app.route('/dataset')
def dataset():
    global master


    global arr
    #master = Auto2.PlayInteractively()
    text = request.args.get('target')
    text2 = request.args.get('natural')
    num1 = request.args.get('strength')
    num2 = request.args.get('disentanglment')
    saveloc = request.args.get('save')
    print(text)
    master.text_n(text2)

    img2, tmp = master.text_t(text)
    #take arr and add the results ontop of eachother caoncatanate then display to see full proggression
    img2 = master.ChangeAlpha(num1)
    img2 = master.ChangeBeta(num2)
    master.SetInit()
    arr.append(tmp)

    serve_pil_image2(img2, saveloc)

    return render_template("hello.html")

@app.route('/initdataset')
def initdataset():
    global master


    global arr
    #master = Auto2.PlayInteractively()
    text = request.args.get('target')
    text2 = request.args.get('natural')
    num1 = request.args.get('strength')
    num2 = request.args.get('disentanglment')
    saveloc = request.args.get('save')
    print(text)
    master.text_n(text2)

    img2, tmp = master.text_t(text)
    #take arr and add the results ontop of eachother caoncatanate then display to see full proggression
    img2 = master.ChangeAlpha(num1)
    img2 = master.ChangeBeta(num2)

    master.SetInit()
    arr.append(tmp)

    serve_pil_image4(img2, saveloc)
    serve_pil_image4(img2, "./here/yum")

    return render_template("hello.html")\

@app.route('/ChangeIdentity')
def ChangeIdentity():
    global master


    global arr
    #master = Auto2.PlayInteractively()
    text = request.args.get('target')
    text2 = request.args.get('natural')
    num1 = request.args.get('strength')
    num2 = request.args.get('disentanglment')
    saveloc = request.args.get('save')
    print(text)
    master.text_n(text2)
    img2 = master.ChangeAlpha(num1)
    img2 = master.ChangeBeta(num2)
    img2, _ = master.text_t(text)
    #take arr and add the results ontop of eachother caoncatanate then display to see full proggression


    serve_pil_image4(img2, saveloc)


    return render_template("hello.html")

@app.route('/ChangeIdentityPermOther')
def ChangeIdentityPermOther():
    global master


    global arr
    #master = Auto2.PlayInteractively()
    text = request.args.get('target')
    text2 = request.args.get('natural')
    num1 = request.args.get('strength')
    num2 = request.args.get('disentanglment')
    saveloc = request.args.get('save')
    print(text)
    master.text_n(text2)
    img2 = master.ChangeAlpha(num1)
    img2 = master.ChangeBeta(num2)
    img2, _ = master.text_t(text)
    #take arr and add the results ontop of eachother caoncatanate then display to see full proggression
    master.SetInit()

    serve_pil_image4(img2, saveloc)


    return render_template("hello.html")





@app.route('/ChangeIdentityPerm')
def ChangeIdentityPerm():
    global master


    global arr
    #master = Auto2.PlayInteractively()
    text = request.args.get('target')
    text2 = request.args.get('natural')
    num1 = request.args.get('strength')
    num2 = request.args.get('disentanglment')
    saveloc = request.args.get('save')
    print(text)
    master.text_n(text2)

    img2, _ = master.text_t(text)
    img2 = master.ChangeAlpha(num1)
    img2 = master.ChangeBeta(num2)
    #take arr and add the results ontop of eachother caoncatanate then display to see full proggression
    master.ident.append(master.SetInit())

    serve_pil_image4(img2, saveloc)


    return render_template("hello.html")













@app.route('/datasetresult')
def datasetresult():
    global master
    global arr

    outputarr = arr[0]
    for i in range(len(arr)-1):
        print(outputarr)
        print(arr[i+1])
        outputarr = np.concatenate([outputarr,arr[i+1]])
    print(outputarr)
    img = Image.fromarray(outputarr)





    serve_pil_image3(img, "Dataset Tester/result" )
    master.SetInit()
    return render_template("hello.html")

# @app.route('/reset')
# def reset():
#     global master
#     master.style_clip.reset()

@app.route('/close')
def close():
    global master
    master.close()





if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True, threaded=False)




