import argparse
from optimization.run_optimization import main
import torchvision
import os
from argparse import Namespace
import GetGUIData


def mainhere(results_dir, latent_dir, photo_dir):
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

    torchvision.utils.save_image(result_image.detach().cpu(), os.path.join(args["results_dir"], args["photo_dir"]),
                                 normalize=True, scale_each=True, range=(-1, 1))





if __name__ == "__main__":
    mainhere("./data/ffhq","./data/ffhq/latents.pt","0.jpg")


    ex = Namespace(real=True, dataset_name="ffhq", Loadtype = 1)
    GetGUIData.main(ex)





