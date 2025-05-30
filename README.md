# Survey Statistics: Recent Advancements and Limitations in Traffic Flow Forcasting

<br> This repository contains code snippets that are used in the survey paper _"Recent Advancements and Limitations in Traffic Flow Prediciton"_.

## Measure Topic Relevance

- Count the number of ArXiv publication for a research topic
- Generation of statistic that describes topic relevance

**Query Arxiv Papers by Topic**

```sh
python topic_relevance.py --topic "traffic prediction" --max-results 10
```

**Visualize existing CSV File**

```py
python topic_relevance.py --topic "traffic prediction" --csv-file "arxiv_traffic_prediction_statistics.csv"
```
