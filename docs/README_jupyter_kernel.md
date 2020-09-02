------
### 使用 Jupyter Notebook, add current venv as kernel

* 添加笔记本核心 Add virtual kernel to Jupyter notebook:

First activate the virtual environment, in the venv:
```
$ pip install ipykernel 
$ python -m ipykernel install --user --name=qsegmt-venv
```
Then launch Jupyter notebook, select the kernel 'q-seg-venv'

* 显示核心列表 Show list of Jupiter kernels:
```
$ jupyter kernelspec list
```
* 移除核心 Remove kernel from Jupyter notebook: 
```
$ jupyter kernelspec uninstall unwanted-kernel
```
