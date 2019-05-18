 #!/bin/bash

cd ~/try/lipnet/LipNet
./my_predict.sh evaluation/models/overlapped-weights368.h5 /home/takashi/try/honnda/framework/video/5.mp4
cd ~/try/honnda/predict/
mv result_split.npy video_face.npy /home/takashi/try/honnda/framework/npy/5
