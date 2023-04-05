import argparse
import math
import os

import torch
import torchvision
from torch import optim
from tqdm import tqdm

from criteria.clip_loss import CLIPLoss
from models.stylegan2.model import Generator
import clip
from utils import ensure_checkpoint_exists



def get_lr(t, initial_lr, rampdown=0.25, rampup=0.05):
    lr_ramp = min(1, (1 - t) / rampdown)
    lr_ramp = 0.5 - 0.5 * math.cos(lr_ramp * math.pi)
    lr_ramp = lr_ramp * min(1, t / rampup)

    return initial_lr * lr_ramp


def main(args):
    ensure_checkpoint_exists(args.ckpt)
    #text_inputs = torch.cat([clip.tokenize(args.description)]).cuda()
    os.makedirs(args.results_dir, exist_ok=True)

    g_ema = Generator(args.stylegan_size, 512, 8)
    g_ema.load_state_dict(torch.load(args.ckpt)["g_ema"], strict=False)
    g_ema.eval()
    g_ema = g_ema.cuda()
    mean_latent = g_ema.mean_latent(4096)
    new = mean_latent.detach().clone().repeat(1, 18, 1)
    print(new.size())
    # if args.latent_path:
    #     latent_code_init = torch.load(args.latent_path).cuda()
    # elif args.mode == "edit":
    latent_code_init_not_trunc = torch.randn(1, 512).cuda()
    print(latent_code_init_not_trunc.size())

    with torch.no_grad():
        _, latent_code_init = g_ema([latent_code_init_not_trunc], return_latents=True,
                                    truncation=args.truncation, truncation_latent=mean_latent)
        #latent_code_init.
        print(latent_code_init.size())
    # else:

    print(latent_code_init[0][:2][:].size())
    print(latent_code_init[0].size())
    #latent_code_init[0] = torch.cat((latent_code_init[0],latent_code_init[0][:2][:]),-1)
    new[0] = torch.cat((latent_code_init[0],latent_code_init[0][:2][:]))
    #latent_code_init = latent_code_init.detach().clone().repeat(1, 18, 1)
    print(latent_code_init.size())
    print(latent_code_init)
    print(new)
    latent = new.detach().clone()
    latent.requires_grad = True

    #return latent
    # clip_loss = CLIPLoss(args)
    #
    # optimizer = optim.Adam([latent], lr=args.lr)
    #
    # pbar = tqdm(range(args.step))

    # for i in pbar:
    #     t = i / args.step
    #     lr = get_lr(t, args.lr)
    #     optimizer.param_groups[0]["lr"] = lr
    #
    #     img_gen, _ = g_ema([latent], input_is_latent=True, randomize_noise=False)
    #
    #     c_loss = clip_loss(img_gen, text_inputs)
    #
    #     if args.mode == "edit":
    #         l2_loss = ((latent_code_init - latent) ** 2).sum()
    #         loss = c_loss + args.l2_lambda * l2_loss
    #     else:
    #         loss = c_loss
    #
    #     optimizer.zero_grad()
    #     loss.backward()
    #     optimizer.step()
    #
    #     pbar.set_description(
    #         (
    #             f"loss: {loss.item():.4f};"
    #         )
    #     )
        # if args.save_intermediate_image_every > 0 and i % args.save_intermediate_image_every == 0:
        #     with torch.no_grad():
        #         img_gen, _ = g_ema([latent], input_is_latent=True, randomize_noise=False)
        #
        #     torchvision.utils.save_image(img_gen, f"results/{str(i).zfill(5)}.png", normalize=True, range=(-1, 1))

    if args.mode == "edit":
        with torch.no_grad():

            img_orig, gr = g_ema([new], input_is_latent=True, randomize_noise=False)

        print("\n\n\n\n\n\nheeeeeeeeeeeeeee")
        print(gr)
        print(gr[0][0])
        print(gr.size())
        torch.save(gr, args.latent_dir)
        print("\n\n\n\n\n\n")

        #final_result = torch.cat([img_orig, img_gen])
        final_result = img_orig

    #else:
        #final_result = img_gen


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


