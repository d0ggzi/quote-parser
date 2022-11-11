from requests import Session
from bs4 import BeautifulSoup
import xlsxwriter


class QuotesParser:

    def __init__(self):
        pass

    def write(self):
        self.book = xlsxwriter.Workbook(f"/home/dggz/code/parsing/shit.xlsx")
        self.worksheet = self.book.add_worksheet("Quotes")
        self.worksheet.set_column("A:A", 100)
        self.worksheet.set_column("B:B", 30)
        self.worksheet.write(0, 0, "hello")
        self.worksheet.write(0, 1, "pidoras")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.book.close()


if __name__ == "__main__":
    parser = QuotesParser()
    parser.write()
    parser.book.close()