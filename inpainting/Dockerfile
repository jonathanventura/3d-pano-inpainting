FROM nvidia/cuda:12.3.0-devel-ubuntu20.04
RUN apt-get update

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/London

RUN apt-get install --no-install-recommends -y \
        git \
        wget \
        python3 \
        python3-pip

RUN pip install torch torchvision opencv-python-headless transforms3d networkx scikit-image tqdm pyyaml matplotlib
RUN pip install "jax[cuda12_pip]==0.4.13" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
RUN pip install -qq -U diffusers==0.11.1 transformers ftfy gradio accelerate

WORKDIR "/inpainting"
COPY . ./
RUN sh download.sh
RUN chmod -R a+rwX ./
