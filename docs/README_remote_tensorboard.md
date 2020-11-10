### Remote tensorboard

reference: https://blog.yyliu.net/remote-tensorboard/

1. (on your local PC) `ssh -L 16006:127.0.0.1:6006 bo@10.206.41.17`
2. (on the remote server) `tensorboard --logdir='~/workspace/questition-answering/ssrc/training/runs' --port=6006`
3. (on your local PC) open your browser, go to `localhost:16006`
