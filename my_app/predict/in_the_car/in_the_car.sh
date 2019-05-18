#!/bin/bash

cd ~/try/lipnet/LipNet
./my_predict.sh evaluation/models/overlapped-weights368.h5 /home/takashi/try/honnda/predict/in_the_car/in_the_car.mp4
cd ~/try/honnda/predict/
mv result_split.npy video_face.npy ./in_the_car
cd ./in_the_car