from langchain.document_loaders import AsyncHtmlLoader
from bs4 import BeautifulSoup, Comment
import csv
import pickle
import pdb


def text_from_html(body):
    soup = BeautifulSoup(body, "html.parser")
    print(soup)
    [s.extract() for s in soup(["style", "script", "[document]", "head", "title"])]
    [s.decompose() for s in soup.find_all("div", {"class": "sidebarViewport_Xe31"})]
    [s.decompose() for s in soup.find_all("nav", {"class": "navbar navbar--fixed-top"})]
    [s.decompose() for s in soup.find_all("div", {"class": "col col--3"})]
    [
        s.decompose()
        for s in soup.find_all("nav", {"class": "pagination-nav docusaurus-mt-lg"})
    ]
    [s.decompose() for s in soup.find_all("footer")]
    visible_text = soup.getText()
    print(visible_text)


def load_csv():
    urls = []
    with open("11-Langchain-Bot/all-langchain-urls.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            urls.append(row[0])
            break

    return urls


def main():
    urls = load_csv()
    loader = AsyncHtmlLoader(urls)
    docs = loader.load()
    # Replace .page_content with cleaned page content.
    for i in range(len(docs)):
        docs[i].page_content = text_from_html(docs[i].page_content)

    # Write it to Pickl
    pickled_str = pickle.dumps(docs)
    with open("langchain_documents.pkl", "wb") as f:
        f.write(pickled_str)


if __name__ == "__main__":
    main()
