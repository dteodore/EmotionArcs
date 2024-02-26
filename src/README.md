This code is based on the [Emotion Dynamics](https://github.com/Priya22/EmotionDynamics/tree/master) codebase by Krishnapriya Vishnubhotla.
Slight modifications were made to allow for how to treat out-of-vocabulary (OOV) terms.

* dataPath: path to csv file containing utterances. This file should contain the columns 'text' with the utterances ordered temporarily 
* lexPath: path to the lexicon file
* lexNames: name of the emotion category or dimension an emotion arc is being created for
* savePath: path to the output folder
* NA: how to treat OOV words. Choices are to either ignore OOV terms (present) or to include them and assign a neutral score (none)

The python package [Twokenize](https://github.com/myleott/ark-twokenize-py) is used to help preprocess the text. This repository should be cloned in the folder where you are running the script.
  
To run:
```
python avgEmoValues.py --dataPath <path to utterances> --lexPath <path to lexicon file> --lexNames <emotion> --savePath <path to output folder> --NA <ignore OOV terms or assign neutral score [none,present]>

python eval_emo_arc.py --manual_dataPath <path to manually annotated utterances> --automatic_dataPath <path to automatically annotated output>
```
