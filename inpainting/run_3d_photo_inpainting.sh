docker build -t 3d-photo-inpainting inpainting/. && \
docker run -u $(id -u):$(id -g) -e USER=$USER -it --rm -e CUDA_VISIBLE_DEVICES=0 -v ./data:/inpainting/data -v ./results:/inpainting/results 3d-photo-inpainting sh -c "cd /inpainting; python3 main.py"

