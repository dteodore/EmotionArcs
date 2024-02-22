This code is based on the [Emotion Dynamics](https://github.com/Priya22/EmotionDynamics/tree/master) codebase by Krishnapriya Vishnubhotla.
Slight modifications were made to allow for how to treat out-of-vocabulary (OOV) terms.


To run:
```
python avgEmoValues.py --dataPath <dataPath to utterances> --lexPath <path to lexicon file> --lexNames <emotion> --savePath <path to output folder > --NA <ignore OOV terms or assign neutral score [none,present]>

```
