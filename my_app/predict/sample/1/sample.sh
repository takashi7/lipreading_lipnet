 #!/bin/bash

cd ~/try/lipnet/LipNet
./my_predict.sh evaluation/models/overlapped-weights368.h5 /home/takashi/try/honnda/predict/sample/sbia1a.mpg
cd ~/try/honnda/predict/
mv result_split.npy video_face.npy ./sample