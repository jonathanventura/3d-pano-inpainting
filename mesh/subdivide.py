#import xatlas
import numpy as np
import trimesh
from trimesh.scene.scene import Scene
#from sklearn.cluster import KMeans
#from matplotlib import pyplot as plt
from argparse import ArgumentParser
import math


def fibonacci_sphere(samples=1000):

    points = []
    phi = math.pi * (math.sqrt(5.) - 1.)  # golden angle in radians

    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        radius = math.sqrt(1 - y * y)  # radius at y

        theta = phi * i  # golden angle increment

        x = math.cos(theta) * radius
        z = math.sin(theta) * radius

        points.append((x, y, z))

    return np.array(points)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input',help='path to input mesh')
    parser.add_argument('output',help='output path for scaled mesh')
    parser.add_argument('--num',type=int,default=20,help='number of models to divide into')
    args = parser.parse_args()

    print('loading mesh...')
    mesh = trimesh.load(args.input)
    if type(mesh) is Scene:
        mesh = mesh.geometry.popitem()[-1]
        print(type(mesh))
    print('done.')

    print(f'mesh has {len(mesh.vertices)} vertices, {len(mesh.faces)} faces')
    
    print('centering vertices...')
    verts = mesh.vertices - np.mean(mesh.vertices,axis=0,keepdims=True)

    print('calculating centroids...')
    face_verts = np.stack([
        verts[mesh.faces[:,0]],
        verts[mesh.faces[:,1]],
        verts[mesh.faces[:,2]]
    ],axis=0)
    centroids = np.mean(face_verts,axis=0) # [N,3]
    #centroids = centroids/np.sqrt(np.sum(centroids**2,axis=1,keepdims=True))
    print('done.')
    
    #label = KMeans(args.num).fit_predict(centroids)
    #plt.hist(label)
    #plt.show()

    vecs = fibonacci_sphere(args.num) # [M,3]
    #print(vecs)
    dots = []
    for vec in vecs:
        dots.append(np.sum(centroids*vec[None,:],axis=1))
    dots = np.array(dots)
    #print('dots',dots.shape)
    
    labels = np.argmax(dots,axis=0)
    #plt.hist(labels)
    #plt.show()
    
    meshes = []
    for label in range(args.num):
        label_mesh = mesh.copy()
        label_mesh.update_faces( (labels==label) )
        label_mesh.remove_unreferenced_vertices()

        print(f'mesh {label} has {len(label_mesh.vertices)} vertices, {len(label_mesh.faces)} faces')
        
        #print('running xatlas...')
        #vmapping, indices, uvs = xatlas.parametrize(label_mesh.vertices, label_mesh.faces)
        #print('done.')
        
        #new_mesh = trimesh.Trimesh( label_mesh.vertices[vmapping], indices)
        #new_mesh.visual = trimesh.visual.texture.TextureVisuals(uv=uvs)

        #new_mesh.export(f'mesh{label}.ply')
        #meshes.append(new_mesh)
        
        #label_mesh.export(f'mesh{label}.glb')
        meshes.append(label_mesh)
    scene = Scene(meshes)
    scene.export(args.output)

