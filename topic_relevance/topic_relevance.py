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

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def query_arxiv(search_query, max_results=50000):
    max_results_per_call = min(max_results, 1000)
    base_url = "http://export.arxiv.org/api/query?"
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


def parse_single_arxiv_response(xml_data: str, ns):
    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        logger.warning(f"XML parsing failed: {e}")
        return []

    records = []
    for entry in root.findall("atom:entry", ns):
        published = entry.find("atom:published", ns)
        title = entry.find("atom:title", ns)
        authors = entry.findall("atom:author/atom:name", ns)

        if (
            published is None
            or published.text is None
            or title is None
            or title.text is None
            or not authors  # This is a list, safe to check directly
        ):
            logger.debug("Skipping incomplete entry")
            continue

        # Clean and validate fields
        published_str = published.text.strip()
        title_str = title.text.strip().replace("\n", " ").replace("  ", " ")
        authors_lst = [a.text.strip() for a in authors if a.text and a.text.strip()]

        if not (published_str and title_str and authors_lst):
            logger.debug("Skipping entry with empty cleaned fields")
            continue

        # Parse year safely
        if not published_str[:4].isdigit():
            logger.debug(f"Skipping invalid year format: {published_str}")
            continue
        year = int(published_str[:4])

        authors_str = ", ".join(authors_lst)

        records.append({"Title": title_str, "Authors": authors_str, "Year": year})

    return records


def parse_arxiv_response(xml_responses: list):
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    all_records = []
    for i, xml_data in enumerate(xml_responses):
        logger.info(f"Parsing response {i + 1}/{len(xml_responses)}")
        records = parse_single_arxiv_response(xml_data, ns)
        all_records.extend(records)
    return all_records


def plot_histogram(df: pd.DataFrame, topic: str, save_path=None, interpolate=True):
    sns.set(style="whitegrid")
    plt.figure(figsize=(6, 3))

    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month

    years = df["Year"].astype(int).tolist()
    year_counts = collections.Counter(years)
    all_years = list(range(min(years), current_year + 1))
    counts = [year_counts.get(y, 0) for y in all_years]

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
        f" by Year\nTotal: {total_papers} papers"
    )
    plt.xlabel("Year")
    plt.ylabel("Number of Publications")
    plt.title(title_string, fontsize=13, pad=10)

    str_years = [str(y) for y in all_years]
    labels = [str(y) for y in all_years if y % 5 == 0]
    xticks = [str_years.index(y) for y in labels]
    plt.xticks(xticks, labels, rotation=45)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path.replace(".csv", ".svg"))
    plt.show()


def main():
    args = parse_args()
    res_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")

    topic_name = args.topic.replace(" ", "_").lower()
    file_name = f"arxiv_{topic_name}_statistics.csv"
    os.makedirs(res_dir, exist_ok=True)

    file_path = os.path.join(res_dir, args.csv_file or file_name)

    if args.csv_file:
        if not os.path.exists(file_path):
            logger.error(f"CSV file not found under file path '{file_path}'")
            return
        logger.info(f"Reading existing CSV from {file_path}")
        statistic = pd.read_csv(file_path)
    else:
        logger.info(f"Querying arXiv for topic: {args.topic}")
        xml_data = query_arxiv(args.topic, max_results=args.max_results)
        records = parse_arxiv_response(xml_data)

        logger.info(f"Found {len(records)} papers on archive")

        statistic = pd.DataFrame(records)  # Has Title, Authors, Year
        statistic.to_csv(file_path, index=False)
        logger.info(f"Saved statistics CSV to {file_path}")

    plot_histogram(
        statistic, args.topic, save_path=file_path, interpolate=not args.no_interpolate
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Query arXiv, save publication titles/authors/years, and plot histogram"
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
        help="Path to save the CSV file with statistics",
    )
    parser.add_argument(
        "--no-interpolate",
        action="store_true",
        help="Disable interpolation for current year in plot",
    )

    return parser.parse_args()


# Example usage:
# python topic_relevance.py --topic "traffic prediction" --max-results 10
# python topic_relevance.py --topic "traffic prediction" --csv-file "arxiv_traffic_prediction_statistics.csv"
if __name__ == "__main__":
    main()
