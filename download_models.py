import spacy

def download_models():
    spacy.cli.download("en_core_web_sm")
    spacy.cli.download("de_core_news_sm")

if __name__ == "__main__":
    download_models()
