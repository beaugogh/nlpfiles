##  Run a Jupyter notebook remotely and access it locally

#### Step 1: Run Jupyter notebook from remote machine:
It is recommended to run the notebook 
within a virtual environment on you remote machine. 
If you haven't installed notebook, install it:
```shell script
(venv) $ pip install notebook
```
Give your remote notebook a port number of your choice, and
(optionally) specify your server ip if you don't want to do the forwarding in step 2:
```shell script
(venv) $ jupyter notebook --no-browser --ip=xx.xx.xx.xx --port=XXXX
```
e.g. 
```shell script
(venv) $ jupyter notebook --no-browser --ip=10.206.41.17 --port=1234
```

#### Step 2 (optional): Forward port XXXX to YYYY and listen to it
On you local terminal, do
```shell script
ssh -N -f -L localhost:YYYY:localhost:XXXX remoteuser@remotehost
```
e.g.
```shell script
ssh -N -f -L localhost:1234:localhost:1234 b00563677@10.206.41.17
```

* ssh: your handy ssh command. See man page for more info
* -N: suppresses the execution of a remote command. 
Pretty much used in port forwarding.
* -f: this requests the ssh command to go to background before execution.
* -L: this argument requires an input in the form of 
local_socket:remote_socket. 
Here, we’re specifying our port as YYYY 
which will be binded to the port XXXX 
from your remote connection.

Remark: when the notebook is run with explicitly specified IP, the localhost to localhost forward wouldn't work

#### Step 3: Fire-up Jupyter Notebook
Copy and paste the notebook URL printed 
in the remote machine terminal, with its token,
into your local browser:

If you forwarded the remote port to your local in step 2:
`http://localhost:YYYY/?token=...`

If you skipped step 2, directly go to the remote notebook, e.g.
`10.206.41.17:1234`, you'd be prompted to input your token the first time, 
which you can find in the remote shell log.

Now you should have the notebook running locally, of which
the interpreter is sitting in the remote.
