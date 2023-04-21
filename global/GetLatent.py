
import os
import shutil
def main(saveloc, imgeloc, dest = None):

    # saveloc - Where the latent will be moved too.
    # imgloc - Where the image to be encoded is located.
    # dest - Where the new image will be moved too. If no value is provided it will be the same as source.
    # This module will take the image into the encoder file path.
    # Then have the encoder create and return the latents and new image.

    if(dest == None):
        dest = imgeloc

    source = "//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/output/latents.pt"

    if  os.path.exists("//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/output/latents.pt"):
        os.remove("//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/output/latents.pt")
    if  os.path.exists("//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/output/inversions"):
        if os.path.exists("//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/output/inversions/00001.jpg"):
            os.remove("//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/output/inversions/00001.jpg")
        os.rmdir("//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/output/inversions")

    files = os.listdir("//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/imagefrom")
    for names in files:
        os.remove("//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/imagefrom/"+names)

    shutil.copy(imgeloc, "//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/imagefrom/")
    os.system('wsl ~ -e sh -c ". ~/miniconda3/etc/profile.d/conda.sh; conda activate e4e_env;  cd encoder4editing; ~/miniconda3/envs/e4e_env/bin/python scripts/inference.py --align --images_dir=imagefrom --save_dir=output check/e4e_ffhq_encode.pt"')

    shutil.move(source, saveloc)
    shutil.copy("//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/output/inversions/00001.jpg", dest)



if (__name__ == "__main__"):

    os.system('wsl ~ -e sh -c ". ~/miniconda3/etc/profile.d/conda.sh; conda activate e4e_env;  cd encoder4editing; ~/miniconda3/envs/e4e_env/bin/python scripts/inference.py --align --images_dir=imagefrom --save_dir=output check/e4e_ffhq_encode.pt"')