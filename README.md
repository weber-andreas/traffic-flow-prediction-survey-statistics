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

## Tools for Conducting Related Work Research

### [Connected Papers](https://www.connectedpapers.com/)

Connected Papers is a research tool that helps you visually explore academic literature by generating graphs of related papers, allowing you to understand the structure, key works, and trends in a specific field.
It also assists in discovering important prior and derivative works, filling gaps in bibliographies, and ensuring you don’t miss significant recent publications.

[Image](assets/connected-papers-example.jpeg)

### [Sort Google Scholar](https://github.com/WittmannF/sort-google-scholar)

Google scholar lacks the ability to sort published papers of specific topic by the number of citations.
The python tool `sortgs` gives you this ability to query a list of papers from Google Scholar including Title, Citations, Links, Rank, and the number of citations per year.
