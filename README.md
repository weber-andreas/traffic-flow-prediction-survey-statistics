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

## Summary of Traffic Flow Prediction Datasets

| Location           | Dataset  | Size    | Interval | Time Span | Year(s)   | Road Type | Source | URL                                                                | Reference                                                                                     |
| ------------------ | -------- | ------- | -------- | --------- | --------- | --------- | ------ | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| California, USA    | LargeST  | 200 GB  | 5 min    | 60 months | 2017–2022 | Highway   | Kaggle | [Link](https://www.kaggle.com/datasets/liuxu77/largest/data)       | Liu, X., et al. (2022). LargeST: A Large-scale Spatiotemporal Dataset for Traffic Prediction. |
| California, USA    | PEMS03   | 2 GB    | 5 min    | 11 months | 2018      | Freeway   | PeMS   | [Link](https://pems.dot.ca.gov/)                                   | Chen, C., et al. (2001). Freeway Performance Measurement System (PeMS).                       |
| California, USA    | PEMS04   | 2 GB    | 5 min    | 2 months  | 2018      | Freeway   | PeMS   | [Link](https://pems.dot.ca.gov/)                                   | Guo, S., et al. (2019). Attention Based Spatial-Temporal Graph Convolutional Networks.        |
| California, USA    | PEMS07   | 4 GB    | 5 min    | 2 months  | 2017      | Freeway   | PeMS   | [Link](https://pems.dot.ca.gov/)                                   | Yu, B., et al. (2017). Spatio-Temporal Graph Convolutional Networks.                          |
| California, USA    | PEMS08   | 1 GB    | 5 min    | 2 months  | 2016      | Freeway   | PeMS   | [Link](https://pems.dot.ca.gov/)                                   | Li, Y., et al. (2017). Diffusion Convolutional Recurrent Neural Network.                      |
| California, USA    | PEMSD7   | 0.01 GB | 5 min    | 2 months  | 2012      | Freeway   | PeMS   | [Link](https://pems.dot.ca.gov/)                                   | Yu, B., et al. (2018). Spatio-Temporal Graph Convolutional Networks.                          |
| California, USA    | PEMSD8   | 0.01 GB | 5 min    | 2 months  | 2016      | Freeway   | PeMS   | [Link](https://pems.dot.ca.gov/)                                   | Guo, S., et al. (2019). Attention Based Spatial-Temporal Graph Convolutional Networks.        |
| San Francisco, USA | PEMS-BAY | 0.01 GB | 5 min    | 6 months  | 2017      | Freeway   | PeMS   | [Link](https://pems.dot.ca.gov/)                                   | Li, Y., et al. (2017). Diffusion Convolutional Recurrent Neural Network.                      |
| Los Angeles, USA   | METR-LA  | 0.01 GB | 5 min    | 4 months  | 2012      | Freeway   | Kaggle | [Link](https://www.kaggle.com/datasets/xiaohualu/metr-la-complete) | Li, Y., et al. (2017). Diffusion Convolutional Recurrent Neural Network.                      |
| Beijing, China     | TaxiBJ   | 0.4 GB  | 30 min   | 17 months | 2013–2016 | Urban     | PWC    | [Link](https://paperswithcode.com/dataset/taxibj)                  | Zhang, J., et al. (2017). Deep Spatio-Temporal Residual Networks.                             |
| Beijing, China     | T-Drive  | 0.8 GB  | 60 min   | 5 months  | 2015      | Urban     | Kaggle | [Link](https://www.kaggle.com/datasets/arashnic/tdriver)           | Yuan, J., et al. (2010). T-Drive: Driving Directions Based on Taxi Trajectories.              |
| Shenzhen, China    | SZ-Taxi  | 0.1 GB  | 15 min   | 1 month   | 2015      | Urban     | GitHub | [Link](https://github.com/lehaifeng/T-GCN/tree/master/data)        | Zhao, L., et al. (2018). T-GCN: A Temporal Graph Convolutional Network.                       |
