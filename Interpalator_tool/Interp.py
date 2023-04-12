from PIL import Image
import numpy



def main(start, end,savename):

    def makegif(frames):
        frameone = frames[0]
        frameone.save(savename+".gif", format="GIF", append_images = frames, save_all=True ,duration = 100, quality = 50, optimize = True )

    def lerp(pix, pix2, interp):
        newarray = pix[:] + (pix2[:] - pix[:])*interp

        return newarray


    newimg = Image.open(start)

    othernewimg = Image.open(end)


    pixels = numpy.array(newimg, dtype=float)
    pixels2 =numpy.array(othernewimg, dtype=float)

    vals = [0,0.4,0.7,1]



    gifpics = []
    for i in vals:
        a = lerp(pixels, pixels2, i)
        img = Image.fromarray(a.astype(numpy.uint8))
        gifpics.append(img)



    makegif(gifpics)

  

if (__name__ == "__main__"):
    main("Images/0.jpg", "Images/1.jpg", "Images/blink")
    main("Images/1.jpg", "Images/0.jpg", "Images/open")


