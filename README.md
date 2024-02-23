Coming soon!

# Emotion Arcs

If you use any of the resources provided in this repository, cite the following work:
```
@inproceedings{teodorescu-mohammad-2023-evaluating,
    title = "Evaluating Emotion Arcs Across Languages: Bridging the Global Divide in Sentiment Analysis",
    author = "Teodorescu, Daniela  and
      Mohammad, Saif",
    editor = "Bouamor, Houda  and
      Pino, Juan  and
      Bali, Kalika",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2023",
    month = dec,
    year = "2023",
    address = "Singapore",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.findings-emnlp.271",
    doi = "10.18653/v1/2023.findings-emnlp.271",
    pages = "4124--4137",
    abstract = "Emotion arcs capture how an individual (or a population) feels over time. They are widely used in industry and research; however, there is little work on evaluating the automatically generated arcs. This is because of the difficulty of establishing the true (gold) emotion arc. Our work, for the first time, systematically and quantitatively evaluates automatically generated emotion arcs. We also compare two common ways of generating emotion arcs: Machine-Learning (ML) models and Lexicon-Only (LexO) methods. By running experiments on 18 diverse datasets in 9 languages, we show that despite being markedly poor at instance level emotion classification, LexO methods are highly accurate at generating emotion arcs when aggregating information from hundreds of instances. We also show, through experiments on six indigenous African languages, as well as Arabic, and Spanish, that automatic translations of English emotion lexicons can be used to generate high-quality emotion arcs in less-resource languages. This opens up avenues for work on emotions in languages from around the world; which is crucial for commerce, public policy, and health research in service of speakers often left behind. Code and resources: https://github.com/dteodore/EmotionArcs",
}
```

# What is in this repository?
- Code to generate emotion arcs using lexicons and gold emotion labelled instances
- Code to evaluate generated emotion arcs compared to gold emotion arcs

# Folders
- ```Lexicons/```: Information on where to obtain emotion lexicons used in our experiments
- ```src/```: scripts to compute instance-level emotion scores for a temporally ordered stream of utterances, and to evaluate generated emotion arcs to manual annotations

# Ethical Considerations


# Authors
If you have any questions please contact the authors:

Daniela Teodorescu, dteodore@ualberta.ca
