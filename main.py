import requests
import xlwt
import re
import argparse

from pathlib import Path
from io import StringIO
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import TextConverter
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from bs4 import BeautifulSoup



def get_cv_email(cv_path):
    pagenums = set()
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)
    infile = open(cv_path, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    match = re.findall(r'[\w\.-]+@[a-z0-9\.-]+', text)
    return match




if __name__ == "__main__":
    parser = argparse.ArgumentParser("export data from libgen.")
    parser.add_argument('-k', '--id', required=True, action='store',
            type=int, help="The journal id.")
    parser.add_argument('-n', '--year', required=True, action='store',
            type=str, help="The range of year (enter like this 2010-2020).")
    args = parser.parse_args()

    jid = args.id
    range_date = args.year.split("-")
    years = range(int(range_date[1]), int(range_date[0]) - 1, -1)

    home_path = Path.home()
    with open(f"{home_path}/exported_data/{jid}.xls", "wb") as file:
    ###################################################################################
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(f"{args.year}")
        row = 1
        ws.write(0, 0 , "Name")
        ws.write(0, 1 , "Author")
        ws.write(0,2, "Email")
        ws.write(0, 3 , "Year")
        for y in years:
            page = requests.get(f"http://libgen.rs/scimag/?journal={jid}&year={y}")
            soup = BeautifulSoup(page.content, 'html.parser')

            authors = []
            names = []
            name_of_journal = None
            a = soup.find_all("tr")
            for counter, i in enumerate(a):
                data = []
                if counter <= 6:
                    continue
                b = i.find_all("td")
                f = b[4].find_all("a")[0]["href"]
                aut = b[0].get_text()
                c = b[1].find("a")
                if c:
                    name = c.get_text()
                else:
                    name = None
                    continue
                try:
                    page1 = requests.get(f"{f}")
                    
                    if not name_of_journal:
                        name_of_journal = b[2].find_all("a")[0].get_text()
                    soup1 = BeautifulSoup(page1.content, "html.parser")
                    l = soup1.find_all("embed")[0]["src"].split("#")[0]
                    if l[1] == "/":
                        req = requests.get(f"https:{l}")
                    else:
                        req = requests.get(f"https://sci-hub.se{l}")
                    Path(f"{home_path}/exported_data/{name_of_journal}/{y}").mkdir(parents=True, exist_ok=True)
                        
                    open(f"{home_path}/exported_data/{name_of_journal}/{y}/{name}.pdf", "w+b").write(req.content)
                    file_path = f"{home_path}/exported_data/{name_of_journal}/{y}/{name}.pdf"
                    emails = get_cv_email(str(file_path))
                    print(name)
                except:
                    continue
            
    ########################################################################################
                ws.write(row, 0, name)
                ws.write(row, 1, aut)
                ws.write(row, 2, ','.join(emails))
                ws.write(row, 3, y)
                row += 1

        wb.save(file)





