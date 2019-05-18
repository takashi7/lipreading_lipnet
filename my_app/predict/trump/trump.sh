#!/bin/bash

cd ~/try/lipnet/LipNet
./my_predict.sh evaluation/models/overlapped-weights368.h5 ~/try/honnda/predict/trump/output2.mp4
cd ~/try/honnda/predict/
mv result_split.npy video_face.npy ./trump
cd ./trump