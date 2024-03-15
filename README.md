<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
# 3D Panorama Inpainting

<!-- ABOUT THE PROJECT -->

![image](docs/assets/model.png)

3D Pano Inpainting: Building a VR Environment from a Single Input Panorama<br>
Shivam Asija, Edward Du, Nam Nguyen, Stefanie Zollmann, Jonathan Ventura<br>
2024 IEEE Conference on Virtual Reality and 3D User Interfaces Abstracts and Workshops (VRW)

Abstract:
Creating 360-degree 3D content is challenging because it requires either a multi-camera rig or a collection of many images taken from different perspectives. Our approach aims to generate a 360◦ VR scene from a single panoramic image using a learning-based inpainting method adapted for panoramic content. We introduce a pipeline capable of transforming an equirectangular panoramic RGB image into a complete 360◦ 3D virtual reality scene represented as a textured mesh, which is easily rendered on a VR headset using standard graphics rendering pipelines. We qualitatively evaluate our results on a synthetic dataset consisting of 360 panoramas in indoor scenes.


<!-- GETTING STARTED -->

## Getting Started

To get a local copy of the project up and running on your machine, follow these simple steps:

### Prerequisites

Before attempting to build this project, make sure you have [Docker Engine](https://docs.docker.com/engine/install/) installed on your machine.

### Installation

Clone the repository
```
git clone https://github.com/jonathanventura/3d-pano-inpainting.git
cd 3d-pano-inpainting
```

### Processing panoramic images

2. Place your panoramic images in the ```data``` directory.  The images should be in equirectangular format and the width of each image should be twice the height.  You will also need to update the filenames in ```data/data.txt```.
3. Execute the depth estimation step
```
sh depth-estimation/run_360monodepth.sh
```   
5. Execute the meshing and inpainting step
```
sh inpainting/run_3d_photo_inpainting.sh
```
6. The results are placed in the ```results``` directory.
7. Re-scale the mesh according to the known height of the camera off of the ground:
```
python mesh/estimate_scale_histogram.py <input mesh> <output mesh> [--camera_height <height>]
```

#### Notes ####

The inpainting code will resize the images to a fixed maximum side length determined by the ```longer_side_len``` parameter in ```inpainting/argument.yml```.

### Running the renderer in a web browser ###

Copy the resulting ```.glb``` file into ```docs/assets``` and update the path in ```docs/renderer.html``` accordingly.

To start the renderer you can use
```
python -m http.server
```

and then navigate to ```localhost:8000/renderer.html```.

<!-- LICENSE -->
<!-- https://choosealicense.com/ -->

## License

This project is distributed under the terms of the  MIT license. See [LICENSE](LICENSE) for details and more information.
