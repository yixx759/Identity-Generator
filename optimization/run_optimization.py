import argparse
import math
import os

import torch
import torchvision

from models.stylegan2.model import Generator

from utils import ensure_checkpoint_exists



def get_lr(t, initial_lr, rampdown=0.25, rampup=0.05):
    lr_ramp = min(1, (1 - t) / rampdown)
    lr_ramp = 0.5 - 0.5 * math.cos(lr_ramp * math.pi)
    lr_ramp = lr_ramp * min(1, t / rampup)

    return initial_lr * lr_ramp


def main(args):

    ensure_checkpoint_exists(args.ckpt)
    os.makedirs(args.results_dir, exist_ok=True)
    g_ema = Generator(args.stylegan_size, 512, 8)
    g_ema.load_state_dict(torch.load(args.ckpt)["g_ema"], strict=False)
    g_ema.eval()
    g_ema = g_ema.cuda()
    mean_latent = g_ema.mean_latent(4096)
    new = mean_latent.detach().clone().repeat(1, 18, 1)
    latent_code_init_not_trunc = torch.randn(1, 512).cuda()


    with torch.no_grad():
        _, latent_code_init = g_ema([latent_code_init_not_trunc], return_latents=True,
                                    truncation=args.truncation, truncation_latent=mean_latent)


    new[0] = torch.cat((latent_code_init[0],latent_code_init[0][:2][:]))
    latent = new.detach().clone()
    latent.requires_grad = True

    if args.mode == "edit":
        with torch.no_grad():

            img_orig, gr = g_ema([new], input_is_latent=True, randomize_noise=False)

        torch.save(gr, args.latent_dir)
        final_result = img_orig

    return final_result





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--description", type=str, default="a person with purple hair", help="the text that guides the editing/generation")
    parser.add_argument("--ckpt", type=str, default="./stylegan2-ffhq-config-f.pt", help="pretrained StyleGAN2 weights")
    parser.add_argument("--stylegan_size", type=int, default=1024, help="StyleGAN resolution")
    parser.add_argument("--lr_rampup", type=float, default=0.05)
    parser.add_argument("--lr", type=float, default=0.1)
    parser.add_argument("--step", type=int, default=300, help="number of optimization steps")
    parser.add_argument("--mode", type=str, default="edit", choices=["edit", "free_generation"], help="choose between edit an image an generate a free one")
    parser.add_argument("--l2_lambda", type=float, default=0.008, help="weight of the latent distance (used for editing only)")
    parser.add_argument("--latent_path", type=str, default=None, help="starts the optimization from the given latent code if provided. Otherwose, starts from"
                                                                      "the mean latent in a free generation, and from a random one in editing. "
                                                                      "Expects a .pt format")
    parser.add_argument("--truncation", type=float, default=0.7, help="used only for the initial latent vector, and only when a latent code path is"
                                                                      "not provided")
    parser.add_argument("--save_intermediate_image_every", type=int, default=0, help="if > 0 then saves intermidate results during the optimization")
    parser.add_argument("--results_dir", type=str, default="results")
    parser.add_argument("--latent_dir", type=str, default="./data/ffhq/latents.pt")
    parser.add_argument("--photo_dir", type=str, default="0.jpg")
    args = parser.parse_args()

    result_image = main(args)

    torchvision.utils.save_image(result_image.detach().cpu(), os.path.join(args.results_dir, args.photo_dir), normalize=True, scale_each=True, range=(-1, 1))


