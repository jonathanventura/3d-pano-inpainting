python3 inpainting/time.py
docker build -t 3d-photo-inpainting inpainting/. 
python3 inpainting/time.py
docker run --runtime=nvidia -u $(xid -u):$(id -g) -e USER=$USER -it --rm -e CUDA_VISIBLE_DEVICES=3 -e HF_HOME=/inpainting/checkpoint -v ./data:/inpainting/data -v ./results:/inpainting/results 3d-photo-inpainting sh -c "cd /inpainting; python3 main.py"
python3 inpainting/time.py