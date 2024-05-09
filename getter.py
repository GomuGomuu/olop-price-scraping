import requests
from selenium import webdriver

# import beautifulsoup
from bs4 import BeautifulSoup


def download_html():
    # create a new instance of the chrome driver
    driver = webdriver.Chrome()
    # get the page
    driver.get("https://www.aba.ae/en/Personal/Loans/Personal-Loan")
    # get the page html
    html = driver.page_source
    # close the driver
    driver.close()
    return html


def write_html(html, file_name="page.html"):
    with open(file_name, "w") as file:
        file.write(html)


def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", id="card-estoque")
    write_html(str(div), "clean.html")
    return str(div)


def get_table(html):
    soup = BeautifulSoup(html, "html.parser")
    div_table = soup.find("div", id="aba-cards")

    write_html(str(div_table), "table.html")


def test():
    image = requests.get(
        "https://repositorio.sbrauble.com/arquivos/in/onepiece/24/65df966616f5b-m0p7y-o56p9-b7fb9549fa5cb8034b503768046d44db.jpg")
    with open(f"cleaned_images/test_card.jpg", "wb") as f:
        f.write(image.content)


if __name__ == "__main__":
    test()
