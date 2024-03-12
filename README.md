<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
# 3d-pano-inpainting

<!-- ABOUT THE PROJECT -->

3D Panorama Inpainting, IEEE VR 2024

<!-- GETTING STARTED -->

## Getting Started

To get a local copy of the project up and running on your machine, follow these simple steps:

### Prerequisites

Before attempting to build this project, make sure you have [Docker Engine](https://docs.docker.com/engine/install/) and [pnpm](https://pnpm.io/) installed on your machine.

### Installation

To get a local copy of the project up and running on your machine, follow these simple steps:

1. Clone the repository
   ```sh
   git clone https://github.com/jonathanventura/3d-pano-inpainting.git
   cd 3d-pano-inpainting
   ```
2. Execute the depth estimation
   ```sh
   cd depth-estimation
   sh ./run_360monodepth.sh
   ```
