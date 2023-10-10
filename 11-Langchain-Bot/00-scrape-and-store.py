from langchain.document_loaders import AsyncHtmlLoader
from bs4 import BeautifulSoup, Comment
import csv
import pickle
import pdb


def tag_visible(element):
    parent_names = ["style", "script", "head", "title", "meta", "[document]"]
    class_names = ["navbar", "footer"]
    print("-------------")
    print(element.parent.name)
    # breakpoint()
    if element.parent.name in parent_names:
        return False
    print(element.parent.attrs)
    print(element.parent.has_attr("navbar__item"))
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, "html.parser")
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)


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
