import numpy as np
import pyrender
import trimesh
import imageio
from scipy.spatial.transform import Rotation
import argparse
import os

def get_pose(radius, theta):
    print("radius:", radius)
    print("theta: ", theta)

    # rotation matrix around the y-axis, translational shift
    rot_y = np.array([
        [np.cos(theta), 0, np.sin(theta), radius * np.sin(theta)],
        [0,             1, 0,             0],
        [-np.sin(theta),0, np.cos(theta), radius * np.cos(theta)],
        [0,             0, 0,             1]
    ])

    # initial pose (identity matrix)
    pose = np.eye(4)

    new_pos = rot_y[:3, 3]
    initial_pos = pose[:3, 3]

    check = np.linalg.norm(new_pos - initial_pos)
    print("check radius:", check)

    cam_pose_rotated = np.dot(rot_y, pose)
    print(cam_pose_rotated)

    return cam_pose_rotated

def main():
    # set the environment to use egl for offscreen rendering
    os.environ["PYOPENGL_PLATFORM"] = "egl"

    parser = argparse.ArgumentParser()
    parser.add_argument('--mesh', required=True)
    # parser.add_argument('--source', required=True)
    # parser.add_argument('--target', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--distance', default = 1)
    args = parser.parse_args()

    scene = pyrender.Scene()

    print('loading ply')
    tri = trimesh.load(args.mesh)

    print('rendering mesh')
    mesh = pyrender.Mesh.from_trimesh(tri)

    # tgt_matrix = np.loadtxt(args.target)
    # src_matrix = np.loadtxt(args.source)
    # pose = tgt_matrix @ np.linalg.inv(src_matrix)  # object
    # print('tgt @ inv(src):')
    # print("mesh pose:", pose)

    pose = np.eye(4)

    size = 1024
    r = pyrender.OffscreenRenderer(size, size)

    # add mesh to scene to render
    print('add mesh to scene')
    mesh_node = scene.add(mesh)

    # sphere to double check if I'm looking at center of screen
    # sphere = trimesh.creation.icosphere(subdivisions=4, radius=0.2)
    # sphere_mesh = pyrender.Mesh.from_trimesh(sphere)
    # scene.add(sphere_mesh, pose=np.eye(4))

    # set up camera
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 2.0, aspectRatio=1.0, znear=.01, zfar=100)

    angles = [np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5 * np.pi/3, 2 * np.pi]

    i = 0
    for x in angles:
        i += 1

        camera_pose = get_pose(radius=np.float64(args.distance), theta=x)

        camera_node = scene.add(camera, pose=camera_pose)

        color, depth = r.render(scene, flags=pyrender.constants.RenderFlags.FLAT)
        # color = np.rot90(color, k=1)
        imageio.imwrite(f"{args.out}_{args.distance}_{i}.png", color)

        print(f"Saved view {i} to {args.out}_{args.distance}_{i}.png")

        scene.remove_node(camera_node)


if __name__ == '__main__':
    main()