import argparse
from optimization.run_optimization import main
import torchvision
import os
from argparse import Namespace
import GetLatentInfo


def GetRandLatent(results_dir, latent_dir, photo_dir):
    # This will generate a random latent and corresponding image to be normalised.
    # This image will have darker colors and will need to be corrected with get gui data.

    args = {
        "description": 'A person with purple hair',
        "ckpt": "stylegan2-ffhq-config-f.pt",
        "stylegan_size": 512,
        "lr_rampup": 0.05,
        "lr": 0.1,
        "step": 300,
        "mode": "edit",
        "l2_lambda": 0.008,
        "id_lambda": 0.005,
        'work_in_stylespace': True,
        "latent_path": None,
        "truncation": 0.7,
        "save_intermediate_image_every": 0,
        "results_dir": results_dir,
        "ir_se50_weights": "model_ir_se50.pth",
        "latent_dir": latent_dir,
        "photo_dir": photo_dir
    }
    result_image = main(Namespace(**args))
    # This will save the random persons face as a picture
    torchvision.utils.save_image(result_image.detach().cpu(), os.path.join(args["results_dir"], args["photo_dir"]),
                                 normalize=True, scale_each=True, range=(-1, 1))





if __name__ == "__main__":
    GetRandLatent("./data/ffhq", "./data/ffhq/latents.pt", "0.jpg")


    ex = Namespace(real=True, dataset_name="ffhq", Loadtype = 1)
    GetLatentInfo.main(ex)





