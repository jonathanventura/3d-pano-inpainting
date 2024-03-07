docker build -t 360monodepth .
docker run -u $(id -u):$(id -g) -e USER=$USER -it --rm -e CUDA_VISIBLE_DEVICES=0 -v ./data:/monodepth/data -v ./results:/monodepth/results 360monodepth sh -c "cd /monodepth/code/python/src; python3 main.py --expname test_experiment --blending_method all --grid_size 8x7"

