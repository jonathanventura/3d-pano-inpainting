import os
import cv2
import imageio
import numpy as np

def dataset(data_dir, hw=(256, 384)):
    """
    Load data from the specified dataset directory.

    Args:
        data_dir (str): Path to the dataset directory.
        hw (tuple): Height and width of the images to resize to. Default is (256, 384).

    Yields:
        dict: A dictionary containing data for each scene.
    """
    H, W = hw
    for scene_dir in os.listdir(data_dir):
        scene_path = os.path.join(data_dir, scene_dir)
        if not os.path.isdir(scene_path):
            continue
        
        data = {}

        # Load source image
        src_img_path = os.path.join(scene_path, 'src.png')
        if os.path.exists(src_img_path):
            src_img = imageio.imread(src_img_path)
            if src_img is not None:
                src_img = cv2.resize(src_img, hw)
                data['src_img'] = src_img

        # Load source depth map
        # src_depth_path = os.path.join(scene_path, 'src_depth.png')
        # if os.path.exists(src_depth_path):
        #     src_depth = cv2.imread(src_depth_path, cv2.IMREAD_UNCHANGED)
        #     if src_depth is not None:
        #         src_depth = cv2.resize(src_depth, hw)
        #         data['src_depth'] = src_depth

	    # Load source disparity map
        src_disp_path = os.path.join(scene_path, 'src_depth.png')
        if os.path.exists(src_disp_path):
            src_disp = cv2.imread(src_disp_path, cv2.IMREAD_UNCHANGED)
            if src_disp is not None:
                src_disp = cv2.resize(src_disp, hw)
                data['src_disp'] = src_disp

        # Load scene name
        data['scene'] = scene_dir

        # Load camera matrix K
        K_path = os.path.join(scene_path, 'K.json')
        if os.path.exists(K_path):
            with open(K_path, 'r') as f:
                K_data = json.load(f)
                K = np.array(K_data)
                data['K'] = K
        else:
            default_K = np.array([[max(H, W), 0, W//2], 
                                [0, max(H, W), H//2], 
                                [0, 0, 1]]).astype(np.float32)
            data['K'] = default_K
        if data['K'].max() > 1:
            data['K'][0, :] = data['K'][0, :] / float(W)
            data['K'][1, :] = data['K'][1, :] / float(H)

        # Load target images and transformation matrices
        tgt_list = []
        tgt_dir = os.path.join(scene_path, 'tgt')
        if os.path.exists(tgt_dir) and os.path.isdir(tgt_dir):
            for tgt_file in os.listdir(tgt_dir):
                tgt_path = os.path.join(tgt_dir, tgt_file)
                if os.path.isfile(tgt_path):
                    tgt_img = cv2.imread(tgt_path)
                    if tgt_img is not None:
                        tgt_img = cv2.resize(tgt_img, hw)
                        tgt_info = {'trans_mtx': np.eye(4)}  # Placeholder for transformation matrix
                        tgt_list.append(tgt_info)
        data['tgt'] = tgt_list

        # Additional data loading or processing steps
        # ...

        yield data

