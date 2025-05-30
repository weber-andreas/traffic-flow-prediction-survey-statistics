import argparse
import collections
import datetime
import logging
import os
import xml.etree.ElementTree as ET

import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def query_arxiv(search_query, max_results=50000):
    max_results_per_call = min(max_results, 1000)
    base_url = "http://export.arxiv.org/api/query?"
    # arXiv API uses start and max_results for pagination
    search_query = search_query.replace(" ", "+")

    xml_reponses = []
    for current_offset in range(0, max_results, max_results_per_call):
        current_batch_size = min(max_results_per_call, max_results - current_offset)
        query = (
            f"{base_url}search_query=all:{search_query}"
            f"&start={current_offset}&max_results={current_batch_size}"
        )
        logger.info(f"Querying arXiv API with URL: {query}")
        response = requests.get(query, timeout=60 * 5)  # 5 minutes timeout
        response.raise_for_status()
        xml_reponses.append(response.text)
    return xml_reponses


def parse_arxiv_response(xml_reponses: list):
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    years = []
    for i, xml_data in enumerate(xml_reponses):
        logger.info(f"Parsing response {i + 1}/{len(xml_reponses)}")
        current_years = parse_single_arxiv_response(xml_data, ns)
        years.extend(current_years)
    return years


def parse_single_arxiv_response(xml_data: str, ns):
    root = ET.fromstring(xml_data)
    years = []
    for entry in root.findall("atom:entry", ns):
        # published date like '2024-05-01T12:34:56Z'
        published = entry.find("atom:published", ns)
        if published is None:
            logger.info("No published date found in entry, skipping...")
            continue
        published_str = published.text
        if not published_str:
            continue
        year = int(published_str[:4])
        years.append(year)
    return years


def plot_histogram_sns(years: list, topic: str, save_path=None, interpolate=True):
    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 3))

    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    # Count publications per year
    years = [int(year) for year in years]
    year_counts = collections.Counter(years)
    all_years = list(range(min(years), current_year + 1))
    counts = [year_counts.get(y, 0) for y in all_years]

    # Interpolate current year
    if interpolate:
        fraction_year_elapsed = current_month / 12
        actual = year_counts[current_year]
        projected = int(round(actual / fraction_year_elapsed))

        sns.barplot(x=all_years, y=counts, color="skyblue", zorder=2)
        sns.barplot(
            x=[all_years[-1]],
            y=[projected],
            color="lightgray",
            zorder=1,
        )
        logger.info(
            f"Current year {current_year} has {actual} papers, projected: {projected}"
        )
    else:
        sns.barplot(x=all_years, y=counts, color="skyblue")

    total_papers = len(years)
    title_string = (
        f"arXiv Publications on '{topic.capitalize()}'"
        f"by Year\nTotal: {total_papers} papers"
    )
    plt.xlabel("Year")
    plt.ylabel("Number of Publications")
    plt.title(title_string, fontsize=13, pad=10)

    # x-ticks
    str_years = [str(y) for y in all_years]
    lables = [str(y) for y in all_years if y % 5 == 0]
    xticks = [str_years.index(y) for y in lables]
    plt.xticks(xticks, lables, rotation=45)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path.replace(".csv", ".svg"))
    plt.show()


def parse_arguments():

    parser = argparse.ArgumentParser(
        description="Query arXiv, save publication years, and plot histogram"
    )
    parser.add_argument(
        "--topic",
        type=str,
        required=True,
        help="Search topic for arXiv query (e.g., 'traffic prediction')",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=50000,
        help="Maximum number of results to query from arXiv (default: 50000)",
    )
    parser.add_argument(
        "--csv-file",
        type=str,
        default="arxiv_traffic_prediction_statistics.csv",
        help="Skip querying and parsing, just read existing CSV and plot",
    )
    parser.add_argument(
        "--no-interpolate",
        action="store_true",
        help="Disable interpolation for current year in plot",
    )

    return parser.parse_args()


if __name__ == "__main__":
    topic = "traffic prediction"
    file_name = f"arxiv_{topic.replace(' ', '_')}_statistics.csv"
    file_path = os.path.join(os.getcwd(), "topic_relevance", "res", file_name)

    # logger.info(f"Querying arXiv for topic: {topic}")
    # xml_data = query_arxiv(topic, max_results=50000)
    # years = parse_arxiv_response(xml_data)

    # logger.info(f"Found {len(years)} papers on archive")

    # statistic = pd.DataFrame(years, columns=["Year"])
    # statistic.to_csv(file_path, index=False)

    # Read the CSV file and plot using seaborn
    statistc = pd.read_csv(file_path)
    years = statistc["Year"].tolist()
    plot_histogram_sns(years, topic, save_path=file_path)
