from skimage import measure, filters, color
import matplotlib.pyplot as plt
import numpy as np
import os
import PyTexturePacker
import plistlib
from PIL import Image
import trimesh
import re
import pandas as pd
from trimesh.exchange.ply import _parse_header
from scipy import stats as st

# .ply filepath
fp2 = './starter_meshes/braunschweig_altstadt_panorama.ply'

H, W = 1024, 2048

# texture pack info placeholder, will update later
TPACK_H, TPACK_W = 0, 0

# load data from .ply file
with open(fp2, 'rb') as f:
    elements, is_ascii, image_name = _parse_header(f)
    #print(is_ascii)
    vertex_data = np.loadtxt(f, max_rows=elements['vertex']['length'])
    face_data = np.loadtxt(f, dtype='int32')[:, 1:]

# Extract vertex data
xyz = vertex_data[:, :3]                  # 3D position
rgb = vertex_data[:, 3:6].astype('uint8') # color
idx = vertex_data[:, 6].astype('int32')   # layer index
pix = vertex_data[:, 7:9].astype('int32') # 2D pixel location in panorama (row, col order)

num_layers = idx.max() + 1

# Ensure all vertices of a face are in the same layer
# Initialize lists to hold the new vertices and their corresponding attributes
new_xyz = []
new_rgb = []
new_idx = []
new_pix = []
new_face_data = face_data.copy()

for i in range(face_data.shape[0]):
    face = face_data[i]
    layers = idx[face]
    
    # Check if vertices are in different layers
    if len(np.unique(layers)) > 1:
        # Determine the target layer by mode
        target_layer = st.mode(layers)
        if target_layer[1] == 1:
            target_layer = max(layers)  # will choose maximum layer number in the case of 3 way tie
        else:
            target_layer = target_layer[0]

        for j, vertex in enumerate(face):
            vertex_layer = layers[j]
            if vertex_layer != target_layer:
                new_xyz.append(xyz[vertex])
                new_rgb.append(rgb[vertex])
                new_idx.append(target_layer)
                new_pix.append(pix[vertex])
                
                
                new_vertex_index = len(xyz) + len(new_xyz) - 1
                
                # remap vertex reference
                new_face_data[i, j] = new_vertex_index

new_xyz = np.array(new_xyz)
new_rgb = np.array(new_rgb)
new_idx = np.array(new_idx)
new_pix = np.array(new_pix)

# Extending original arrays (vstack to preserve shape)
xyz = np.vstack((xyz, new_xyz))
rgb = np.vstack((rgb, new_rgb))
idx = np.concatenate((idx, new_idx))
pix = np.vstack((pix, new_pix))

face_data = new_face_data

# Initialize dataframe to store pixel information
pixel_info = pd.DataFrame({
    'row': pix[:, 0],
    'col': pix[:, 1],
    'layer': idx
})

print('made data frame')

output_folder = "./connected_comps"
os.makedirs(output_folder, exist_ok=True)

blob_folder = "./blob_maps"
os.makedirs(blob_folder, exist_ok=True)

uv_folder = "./uv_images"
os.makedirs(uv_folder, exist_ok=True)

# Create binary maps layer by layer
blob_info = []
for i in range(num_layers):
    sel = (idx == i)  # sel is a binary mask
    
    uv_map = np.zeros((H, W, 4), dtype='uint8')
    uv_map[:, :, 3] = 0

    uv_map[pix[sel, 0], pix[sel, 1], :3] = rgb[sel]
    uv_map[pix[sel, 0], pix[sel, 1], 3] = 255
    print(f'saving uv map {i}')
    uv_filename = os.path.join(uv_folder, f'uv_map_{i}.png')
    plt.imsave(uv_filename, uv_map)
    
    binary_map = np.zeros((H, W), dtype='bool')
    binary_map[pix[sel, 0], pix[sel, 1]] = True
    print(f'saving binary map {i}')
    binary_filename = os.path.join(blob_folder, f'binary_map_{i}.png')
    plt.imsave(binary_filename, binary_map)
    
    # Label blobs and extract properties
    blobs_labels = measure.label(binary_map)
    regions = measure.regionprops(blobs_labels)
    
    # Update dataframe for every region in the layer
    for region in regions:
        minr, minc, maxr, maxc = region.bbox
        blob_label = region.label
        
        # Identify pixels that belong to this blob
        blob_pixels = np.argwhere(blobs_labels == blob_label)
        
        # Find each pixel and populate with info about the blob it's in
        for pixel in blob_pixels:
            r, c = pixel
            blob_info.append({
                'row': r,
                'col': c,
                'layer': i,
                'minr': minr,
                'minc': minc,
                'maxr': maxr,
                'maxc': maxc,
                'blob': blob_label
            })
        
        # Save images to put into texture packer
        cropped_image = uv_map[minr:maxr, minc:maxc]
        cropped_image = np.ascontiguousarray(cropped_image)
        filename_full = os.path.join(output_folder, f'blob_{blob_label}layer{i}{minr}{minc}{maxr}{maxc}.png')
        plt.imsave(filename_full, cropped_image)

blob_info = pd.DataFrame(blob_info)
pixel_info = pixel_info.merge(blob_info, on=['row', 'col', 'layer'], how='left')

# Pack texture with WHITE background
packer = PyTexturePacker.Packer.create(
    enable_rotated=False, bg_color=0xffffffff, reduce_border_artifacts=True, inner_padding=10, border_padding=0, shape_padding=0
)
packer.pack("connected_comps/", "cc_map_%d")

texture_map_image = Image.open("cc_map_0.png")

# Set total texture pack dimensions
with open("cc_map_0.plist", "rb") as pf:
    metadata = plistlib.load(pf)
    size = metadata["metadata"]["size"].strip("{}").split(",")
    TPACK_H = float(size[1])
    TPACK_W = float(size[0])

# Map blobs to texture rects for quicker lookup
texture_rects = []
for region in metadata["frames"]:
    frame = metadata["frames"][region]
    texture_rect = frame["frame"]
    match = re.search(r'\{\{(\d+),(\d+)\}', texture_rect)
    if match:
        texture_rect = [int(match.group(1)), int(match.group(2))]
        texture_rects.append({
            'filename': region,
            'tx': texture_rect[0],
            'ty': texture_rect[1]
        })
texture_rects = pd.DataFrame(texture_rects)
pixel_info['filename'] = pixel_info.apply(
    lambda row: f'blob_{row["blob"]}layer{row["layer"]}{row["minr"]}{row["minc"]}{row["maxr"]}{row["maxc"]}.png',
    axis=1
)
pixel_info = pixel_info.merge(texture_rects, on='filename', how='left')
pixel_info['u'] = pixel_info['tx'] + (pixel_info['col'] - pixel_info['minc'])
pixel_info['v'] = TPACK_H - (pixel_info['ty'] + (pixel_info['row'] - pixel_info['minr']))
pixel_info['u'] = pixel_info['u'].astype('float64')
pixel_info['v'] = pixel_info['v'].astype('float64')

pixel_info['u'] = (pixel_info['u'] + 0.5) / TPACK_W
pixel_info['v'] = (pixel_info['v'] + 0.5) / TPACK_H
pixel_info.to_csv('pixel_info.csv')

uv_coordinates = pixel_info[['u','v']].to_numpy()

# Make the mesh and export
visuals = trimesh.visual.TextureVisuals(uv=uv_coordinates, image=texture_map_image)
mesh = trimesh.Trimesh(vertices=xyz, faces=face_data, visual=visuals)
mesh.export("uv_mesh.glb")

# Delete all files in connected_comps folder
for filename in os.listdir(output_folder):
    file_path = os.path.join(output_folder, filename)
    if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
    elif os.path.isdir(file_path):
        os.rmdir(file_path)

