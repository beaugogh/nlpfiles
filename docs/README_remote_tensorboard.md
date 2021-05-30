### Remote tensorboard

reference: https://blog.yyliu.net/remote-tensorboard/

1. (on your local PC) `ssh -L 16006:127.0.0.1:6006 bo@7.191.137.117`
2. (on the remote server) `tensorboard --logdir='~/workspace/question-answering/src/training/runs' --port=6006`
3. (on your local PC) open your browser, go to `localhost:16006`
