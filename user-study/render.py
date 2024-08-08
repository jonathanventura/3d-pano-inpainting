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
    c = np.array([radius * np.sin(theta),0,radius * np.cos(theta)])
    R = Rotation.from_euler('Y',theta).as_matrix()

    pose = np.eye(4)
    pose[:3,:3] = R
    pose[:3,3] = c
    return pose

def main():
    # set the environment to use egl for offscreen rendering
    os.environ["PYOPENGL_PLATFORM"] = "egl"

    parser = argparse.ArgumentParser()
    parser.add_argument('--mesh', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--distance', type=float, default = 2)
    args = parser.parse_args()

    scene = pyrender.Scene()

    print('loading ply')
    tri = trimesh.load(args.mesh)
    if type(tri) is trimesh.Scene:
        tri = tri.geometry[next(iter(tri.geometry))]

    print('from_trimesh')
    mesh = pyrender.Mesh.from_trimesh(tri)

    pose = np.eye(4)

    print('making renderer')
    width = 2048
    height = width*9//16
    r = pyrender.OffscreenRenderer(width, height)

    # add mesh to scene to render
    print('add mesh to scene')
    mesh_node = scene.add(mesh)

    # sphere to double check if I'm looking at center of screen
    # sphere = trimesh.creation.icosphere(subdivisions=4, radius=0.2)
    # sphere_mesh = pyrender.Mesh.from_trimesh(sphere)
    # scene.add(sphere_mesh, pose=np.eye(4))

    # set up camera
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 2.0, aspectRatio=width/height, znear=.01, zfar=100)

    #angles = [np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5 * np.pi/3, 2 * np.pi]
    angles = np.linspace(0,2*np.pi,10,endpoint=False)#[np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5 * np.pi/3, 2 * np.pi]

    for i,x in enumerate(angles):
        camera_pose = get_pose(radius=np.float64(args.distance), theta=x)

        camera_node = scene.add(camera, pose=camera_pose)

        color, depth = r.render(scene, flags=pyrender.constants.RenderFlags.FLAT)
        # color = np.rot90(color, k=1)
        imageio.imwrite(f"{args.out}_{args.distance}_{i}.png", color)

        print(f"Saved view {i} to {args.out}_{args.distance}_{i}.png")

        scene.remove_node(camera_node)


if __name__ == '__main__':
    main()