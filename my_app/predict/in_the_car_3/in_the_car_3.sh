#!/bin/bash

cd ~/try/lipnet/LipNet
./my_predict.sh evaluation/models/unseen-weights178.h5 /home/takashi/try/honnda/predict/in_the_car_3/in_the_car3.mp4
cd ~/try/honnda/predict/
mv result_split.npy video_face.npy ./in_the_car_3
cd ./in_the_car_3