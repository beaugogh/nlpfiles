### How to manually download and use Stanza models
reference: https://github.com/stanfordnlp/stanza/issues/275

* Go to the the stanza model history and note the latest model version:
    - https://stanfordnlp.github.io/stanza/model_history.html
    - Note that the model version is not necessary the same the the Stanza release version, for example, 
      currently Stanza is released under version 1.1.1, but its corresponding model release version is 1.1.0.

* Download the resource JSON file according to the model version of your choosing:
    - https://raw.githubusercontent.com/stanfordnlp/stanza-resources/master/resources_1.1.0.json
    - And rename it to just `resources.json`
    
* Download Stanza models manually according to the model version and language(s) of your choosing:
    - https://nlp.stanford.edu/software/stanza/1.1.0/en/default.zip
    - If you don't want to download the default model, consult this page for alternatives:
      https://stanfordnlp.github.io/stanza/available_models.html

* Create the folder `stanza` and its sub-folder corresponding to your language, e.g. `stanza/en`:
    - unzip the model files into this sub-folder
    - move the `resources.json` file into the `stanza` folder

* Now you may be "Stanza" this way:
    - `stanza.Pipeline('en', dir='/path/to/stanza')`
