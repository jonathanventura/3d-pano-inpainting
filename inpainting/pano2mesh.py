import numpy as np
import argparse
import glob
import os
from functools import partial
#import vispy
import scipy.misc as misc
from tqdm import tqdm
import yaml
import time
import sys
from mesh import  write_ply_no_inpainting
from utils import get_MiDaS_samples, read_MiDaS_depth, read_real_depth
import torch
import cv2
from skimage.transform import resize
import imageio
import copy
from MiDaS.run import run_depth
from boostmonodepth_utils import run_boostmonodepth
from MiDaS.monodepth_net import MonoDepthNet
import MiDaS.MiDaS_utils as MiDaS_utils
from bilateral_filtering import sparse_bilateral_filtering
from skimage import color


parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, default='argument_p2m.yml',help='Configure of post processing')
args = parser.parse_args()
config = yaml.load(open(args.config, 'r'), Loader=yaml.Loader)
#if config['offscreen_rendering'] is True:
    #vispy.use(app='egl')
os.makedirs(config['mesh_folder'], exist_ok=True)
os.makedirs(config['video_folder'], exist_ok=True)
os.makedirs(config['depth_folder'], exist_ok=True)
sample_list = get_MiDaS_samples(config['src_folder'], config['depth_folder'], config, config['specific'])
normal_canvas, all_canvas = None, None

if isinstance(config["gpu_ids"], int) and (config["gpu_ids"] >= 0):
    device = config["gpu_ids"]
else:
    device = "cpu"

print(f"running on device {device}")

for idx in tqdm(range(len(sample_list))):
    depth = None
    sample = sample_list[idx]
    print("Current Source ==> ", sample['src_pair_name'])
    mesh_fi = os.path.join(config['mesh_folder'], sample['src_pair_name'] + "_p2m" +'.ply')
    image = imageio.imread(sample['ref_img_fi'])[:,:,:3]

    print(f"Running depth extraction at {time.time()}")
    if config['use_boostmonodepth'] is True:
        run_boostmonodepth(sample['ref_img_fi'], config['src_folder'], config['depth_folder'])
    elif config['require_midas'] is True:
        run_depth([sample['ref_img_fi']], config['src_folder'], config['depth_folder'],
                  config['MiDaS_model_ckpt'], MonoDepthNet, MiDaS_utils, target_w=640)
    print(sample['depth_fi'])
    print("Depth shape", np.load(sample['depth_fi']).shape)

    if 'npy' in config['depth_format']:
        config['output_h'], config['output_w'] = np.load(sample['depth_fi']).shape[:2]
    else:
        config['output_h'], config['output_w'] = imageio.imread(sample['depth_fi']).shape[:2]
    frac = config['longer_side_len'] / max(config['output_h'], config['output_w'])
    config['output_h'], config['output_w'] = int(config['output_h'] * frac), int(config['output_w'] * frac)
    config['original_h'], config['original_w'] = config['output_h'], config['output_w']
    if image.ndim == 2:
        image = image[..., None].repeat(3, -1)
    if np.sum(np.abs(image[..., 0] - image[..., 1])) == 0 and np.sum(np.abs(image[..., 1] - image[..., 2])) == 0:
        config['gray_image'] = True
    else:
        config['gray_image'] = False
    print("Width, height:", config['output_w'],config['output_h'])
    image = cv2.resize(image, (config['output_w'], config['output_h']), interpolation=cv2.INTER_AREA)
    if config["use_real_depth"] is False:
        depth = read_MiDaS_depth(sample['depth_fi'], 3.0, config['output_h'], config['output_w'])
    else:
        depth = read_real_depth(sample['depth_fi'], h=config["output_h"], w=config['output_w'])
    mean_loc_depth = depth[depth.shape[0]//2, depth.shape[1]//2]
    if not(config['load_ply'] is True and os.path.exists(mesh_fi)):
        vis_photos, vis_depths = sparse_bilateral_filtering(depth.copy(), image.copy(), config, num_iter=config['sparse_iter'], spdb=False)
        depth = vis_depths[-1]
        model = None
        torch.cuda.empty_cache()
        print("Start Running Pano2Mesh ...")
        print(f"Writing depth ply (and basically doing everything) at {time.time()}")
        rt_info = write_ply_no_inpainting(image,
                              depth,
                              sample['int_mtx'],
                              mesh_fi,
                              config)

      

        # if rt_info is False:
        #     continue
        # rgb_model = None
        # color_feat_model = None
        # depth_edge_model = None
        # depth_feat_model = None
        # torch.cuda.empty_cache()
    #if config['save_ply'] is True or config['load_ply'] is True:
        #verts, colors, faces, Height, Width, hFov, vFov = read_ply(mesh_fi)
    #else:
        #verts, colors, faces, Height, Width, hFov, vFov = rt_info


    # print(f"Making video at {time.time()}")
    # videos_poses, video_basename = copy.deepcopy(sample['tgts_poses']), sample['tgt_name']
    # top = (config.get('original_h') // 2 - sample['int_mtx'][1, 2] * config['output_h'])
    # left = (config.get('original_w') // 2 - sample['int_mtx'][0, 2] * config['output_w'])
    # down, right = top + config['output_h'], left + config['output_w']
    # border = [int(xx) for xx in [top, down, left, right]]
    # normal_canvas, all_canvas = output_3d_photo(verts.copy(), colors.copy(), faces.copy(), copy.deepcopy(Height), copy.deepcopy(Width), copy.deepcopy(hFov), copy.deepcopy(vFov),
    #                     copy.deepcopy(sample['tgt_pose']), sample['video_postfix'], copy.deepcopy(sample['ref_pose']), copy.deepcopy(config['video_folder']),
    #                     image.copy(), copy.deepcopy(sample['int_mtx']), config, image,
    #                     videos_poses, video_basename, config.get('original_h'), config.get('original_w'), border=border, depth=depth, normal_canvas=normal_canvas, all_canvas=all_canvas,
    #                     mean_loc_depth=mean_loc_depth)
