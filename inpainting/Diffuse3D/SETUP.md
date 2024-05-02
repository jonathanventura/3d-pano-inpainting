## Run this to setup the depthaware stuff
```
conda create -n d3d pytorch==1.8.0 torchvision==0.9.0 torchaudio==0.8.0 cudatoolkit=10.1 -c hcc  -c pytorch
conda activate d3d

conda install tqdm scipy -y
conda install gxx_linux-64=7.2 -y
pip install tensorboardX
pip install dominate
pip install opencv-python-headless transforms3d networkx scikit-image pyyaml matplotlib vispy moviepy omegaconf einops pytorch_lightning==1.4.2 torchmetrics==0.5.0 taming-transformers-rom1504
```
## To setup depthconv
clone https://github.com/crmauceri/DepthAwareCNN-pytorch1.5
```
cd depthaware/models/ops/depthconv/
python setup.py install
cd ../depthavgpooling/
python setup.py install
cd ../../../../
pip install -e .
```

## Run by going to Diffuse3D/
run `python inference.py --data_dir dataset --output_dir output`