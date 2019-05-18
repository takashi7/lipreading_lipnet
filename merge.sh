#!/bin/bash

repo=lipnet/LipNet

git remote add ${repo} /home/takashi/try/lipreading_lipnet/${repo}
git fetch ${repo}
git read-tree --prefix=${repo} ${repo}/master
git checkout -- .
git add .
git commit -m 'add in lipnet repo'
git merge -s subtree ${repo}/master --allow-unrelated-histories

