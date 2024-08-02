import sklearn
import numpy as np
import trimesh
from argparse import ArgumentParser
from matplotlib import pyplot as plt

parser = ArgumentParser()
parser.add_argument('input',help='path to input mesh')
parser.add_argument('output',help='output path for scaled mesh')
parser.add_argument('--bins',default=500,help='number of bins in histogram')
parser.add_argument('--camera_height',default=2,help='camera height in meters')
args = parser.parse_args()

print('loading mesh...')
mesh = trimesh.load(args.input)
vertices = mesh.vertices
X = vertices[:, 0]
Y = vertices[:, 1]
plane = vertices[:, :2]

print(f'building histogram with {args.bins} bins...')
hist, bin_edges = np.histogram(Y, bins=args.bins)

plt.bar(bin_edges[:-1], hist, width=np.diff(bin_edges), edgecolor='black')
plt.savefig("new_hist")
plt.show()

print(hist)
max_bin_index = np.argmax(hist)


Y_max_bin = Y[(Y>bin_edges[max_bin_index])&(Y<=bin_edges[max_bin_index+1])]

cluster_height = np.mean(Y_max_bin)

print(f'height of largest cluster: {cluster_height}')

translated = Y - cluster_height

vertices[:, 1] = translated

mesh.vertices = vertices * 2 / abs(cluster_height)

print('exporting mesh...')
mesh.export(args.output)
