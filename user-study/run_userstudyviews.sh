#!/bin/bash

while read -r line; do
    echo "Creating $line views"
    mkdir $line
    python render.py --mesh "../results/${line}_DA_p2m.glb" --distance 0.5 --out "$line/$line-p2m"
    python render.py --mesh "../results/${line}_DA_p2m.glb" --distance 1 --out "$line/$line-p2m"
    python render.py --mesh "../results/${line}_DA_p2m.glb" --distance 2 --out "$line/$line-p2m"
    python render.py --mesh "../results/${line}_DA_p2m.glb" --distance 4 --out "$line/$line-p2m"
    python render.py --mesh "../results/${line}_DA_p2m.glb" --distance 8 --out "$line/$line-p2m"
    python render.py --mesh "../results/${line}_DA_ip.glb" --distance 0.5 --out "$line/$line-ip"
    python render.py --mesh "../results/${line}_DA_ip.glb" --distance 1 --out "$line/$line-ip"
    python render.py --mesh "../results/${line}_DA_ip.glb" --distance 2 --out "$line/$line-ip"
    python render.py --mesh "../results/${line}_DA_ip.glb" --distance 4 --out "$line/$line-ip"
    python render.py --mesh "../results/${line}_DA_ip.glb" --distance 8 --out "$line/$line-ip"
done < scenes.txt