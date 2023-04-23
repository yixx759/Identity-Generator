from PIL import Image
import numpy


# When provided with two images it will generate a gif interpolating or "Fading" between the two
# This can be used with match finder in Customise character to creat diffrent animation for all instances of a change.
# eg all diffrent blink combinations for all diffrent faces.

def main(start, end,savename, picslist):
    # start - Image to begin
    # end - Image to face to
    # savename - Image save location

    def makegif(frames):
        frameone = frames[0]
        frameone.save(savename+".gif", format="GIF", append_images = frames, save_all=True ,duration = 230, quality = 20, optimize = True, loop = 0 )

    def lerp(pix, pix2, interp):
        #Interpolates the pixel color value of the two images give a middle value.
        newarray = pix[:] + (pix2[:] - pix[:])*interp

        return newarray




    vals = [0,0.2,0.4,0.6,0.8,1,1]



    gifpics = []
    for i2 in range(len(picslist)):


        if (i2 ==  len(picslist)-1):
            break

        newimg = Image.open(picslist[i2]).convert("RGB")

        othernewimg = Image.open(picslist[i2+1]).convert("RGB")

        pixels = numpy.array(newimg, dtype=float)
        pixels2 = numpy.array(othernewimg, dtype=float)

        for i in vals:
            a = lerp(pixels, pixels2, i)
            img = Image.fromarray(a.astype(numpy.uint8))
            gifpics.append(img)



    makegif(gifpics)

  

if (__name__ == "__main__"):
    list = ["Images/0.jpg","Images/3.jpg"]

    main("Images/0.jpg", "Images/1.jpg", "Images/blink", list)
    #main("Images/1.jpg", "Images/0.jpg", "Images/open")


