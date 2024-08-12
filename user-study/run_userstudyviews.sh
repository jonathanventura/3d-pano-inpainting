#!/bin/bash

while read -r line; do
    # split line into parts
    read -ra parts <<< "$line"
    #store scene name
    scene="${parts[0]}"
    # set rotation if specified
    if [ "${#parts[@]}" -gt 1 ]; then
        rotation="${parts[1]}"
    else
        rotation=0
    fi
    echo "Creating ${scene} views"
    echo "Rotation at ${rotation}"

    mkdir "../../../../data2/3d-pano-user-study/${scene}"
    python render.py --mesh "../results/${scene}_DA_p2m.glb" --distance 0.5 --rotation ${rotation} --out "../../../../data2/3d-pano-user-study/${scene}/${scene}_p2m"
    python render.py --mesh "../results/${scene}_DA_p2m.glb" --distance 1 --rotation ${rotation} --out "../../../../data2/3d-pano-user-study/${scene}/${scene}_p2m"
    python render.py --mesh "../results/${scene}_DA_p2m.glb" --distance 2 --rotation ${rotation} --out "../../../../data2/3d-pano-user-study/${scene}/${scene}_p2m"
    python render.py --mesh "../results/${scene}_DA_p2m.glb" --distance 4 --rotation ${rotation} --out "../../../../data2/3d-pano-user-study/${scene}/${scene}_p2m"
    python render.py --mesh "../results/${scene}_DA_ip.glb" --distance 0.5 --rotation ${rotation} --out "../../../../data2/3d-pano-user-study/${scene}/${scene}_ip"
    python render.py --mesh "../results/${scene}_DA_ip.glb" --distance 1 --rotation ${rotation} --out "../../../../data2/3d-pano-user-study/${scene}/${scene}_ip"
    python render.py --mesh "../results/${scene}_DA_ip.glb" --distance 2 --rotation ${rotation} --out "../../../../data2/3d-pano-user-study/${scene}/${scene}_ip"
    python render.py --mesh "../results/${scene}_DA_ip.glb" --distance 4 --rotation ${rotation} --out "../../../../data2/3d-pano-user-study/${scene}/${scene}_ip"
done < scenes.txt