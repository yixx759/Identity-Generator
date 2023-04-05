
import os
import shutil
def main(saveloc, imgeloc):
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
    #//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/imagefrom
    shutil.move(imgeloc, "//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/imagefrom/")
    os.system('wsl ~ -e sh -c ". ~/miniconda3/etc/profile.d/conda.sh; conda activate e4e_env;  cd encoder4editing; ~/miniconda3/envs/e4e_env/bin/python scripts/inference.py --align --images_dir=imagefrom --save_dir=output check/e4e_ffhq_encode.pt"')
    #os.rename(source,newsource )
    shutil.move(source, saveloc)
    shutil.copy("//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/output/inversions/00001.jpg", imgeloc)

#//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/output/latents.pt

if (__name__ == "__main__"):
    #main("//wsl.localhost/Ubuntu-20.04/home/m/encoder4editing/output/latents.pt")
    os.system('wsl ~ -e sh -c ". ~/miniconda3/etc/profile.d/conda.sh; conda activate e4e_env;  cd encoder4editing; ~/miniconda3/envs/e4e_env/bin/python scripts/inference.py --align --images_dir=imagefrom --save_dir=output check/e4e_ffhq_encode.pt"')