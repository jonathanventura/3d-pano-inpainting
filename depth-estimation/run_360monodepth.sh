docker build -t 360monodepth depth-estimation/.
docker run -u $(id -u):$(id -g) -e USER=$USER -e XDG_CACHE_HOME=$XDG_CACHE_HOME -it --rm -e CUDA_VISIBLE_DEVICES=0 -v ./data:/monodepth/data -v ./results:/monodepth/results -v $XDG_CACHE_HOME/huggingface/hub:/cache 360monodepth sh -c "cd /monodepth/code/python/src; python3 main.py --expname test_experiment --blending_method frustum --grid_size 8x7"

