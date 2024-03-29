There are two files in ```src```:
* avgEmoValues.py -- computes emotion scores per instance
* eval_emo_arc.py -- evaluates the predicted arc by calculating the spearman correlation between the predicted arc and the manually annotated arc

The ```avgEmoValues.py``` script is based on the [Emotion Dynamics](https://github.com/Priya22/EmotionDynamics/tree/master) codebase by Krishnapriya Vishnubhotla.
Slight modifications were made to allow for how to treat out-of-vocabulary (OOV) terms.

To run ```avgEmoValues.py``` it requires the following arguments:
* dataPath: path to csv file containing utterances. This file should contain the columns 'text' with the utterances ordered temporarily 
* lexPath: path to the lexicon file. This file should contain two columns: ```word,emotion_score``` with the header ```word,valence``` as an example for the emotion dimension _valence_.
* lexNames: name of the emotion category or dimension an emotion arc is being created for e.g., valence
* savePath: path to the output folder
* NA: how to treat OOV words. Choices are to either ignore OOV terms by replacing them with 'NA' (NAs are present) or to include OOV terms and assign a neutral score (none for no NA terms). Note, that depending on the emotion you are analzying and the lexicon's scale range, a neutral score may mean different things. For example, when using a lexicon ranging from -1 to 1 for valence, 0 is a neutral score. However, if the lexicon for valence ranges from 0 to 1, then 0.5 would be considered neutral since valence is a bipolar emotion.

The python package [Twokenize](https://github.com/myleott/ark-twokenize-py) is used to help preprocess the text. This repository should be cloned in the folder where you are running the script.

```
python avgEmoValues.py --dataPath <path to utterances> --lexPath <path to lexicon file> --lexNames <emotion> --savePath <path to output folder> --NA <ignore OOV terms or assign neutral score [none,present]> --neutralScore <float, default is 0>
```

To run eval_emo_arc.py, two arguments are required:
* manual_dataPath: path to the file with the utterances manually annotated for emotion
* automatic_dataPath: path to the file with emotion scores derived from automatic approaches such as the lexicon-based approach
  
```
python eval_emo_arc.py --manual_dataPath <path to manually annotated utterances> --automatic_dataPath <path to automatically annotated output>
```
