from requests import Session
from bs4 import BeautifulSoup
import xlsxwriter


class QuotesParser:
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 "
                      "Safari/537.36"}

    def __init__(self, output_file):
        self.work = Session()
        self.work.get("https://quotes.toscrape.com/", headers=self.headers)
        self.writer = Writer(output_file)

    def login(self, login, password):
        response = self.work.get("https://quotes.toscrape.com/login", headers=self.headers)
        soup_login = BeautifulSoup(response.text, "lxml")
        token = soup_login.find("form").find("input").get("value")
        data = {"csrf_token": token,
                "username": login,
                "password": password}
        self.work.post("https://quotes.toscrape.com/login", headers=self.headers, data=data, allow_redirects=True)

    def parse_quotes(self):
        page = 1
        while True:
            result = self.work.get(f"https://quotes.toscrape.com/page/{page}/", headers=self.headers)
            soup_page = BeautifulSoup(result.text, "lxml")
            quotes = soup_page.find_all("div", class_="quote")
            if len(quotes) == 0:
                break
            for quote in quotes:
                text = quote.find("span", class_="text").text[1:-1]
                author = quote.find("small", class_="author").text
                self.writer.write(text, author)
            page += 1


class Writer:
    row = 0
    column = 0

    def __init__(self, output_file):
        self.book = xlsxwriter.Workbook(f"/home/dggz/code/parsing/{output_file}.xlsx")
        self.worksheet = self.book.add_worksheet("Quotes")
        self.worksheet.set_column("A:A", 100)
        self.worksheet.set_column("B:B", 30)

    def write(self, text, author):
        self.worksheet.write(self.row, self.column, text)
        self.worksheet.write(self.row, self.column + 1, author)
        self.row += 1


if __name__ == "__main__":
    parser = QuotesParser("quotes")
    parser.login("admin", "admin")
    parser.parse_quotes()
    parser.writer.book.close()
