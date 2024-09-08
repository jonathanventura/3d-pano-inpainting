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

WORKDIR "/inpainting"
COPY . ./
RUN sh download.sh
RUN chmod -R a+rwX ./
