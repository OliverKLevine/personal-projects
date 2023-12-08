from urllib.request import Request, urlopen
import os
from datetime import date
import json

def parse_ID_seminars(html):
    htmls = [line.split("</div></div></article></div></div>")[0] for line in html.split('<div  class="tribe-common-g-row tribe-events-calendar-list__event-row" >')[1:]]
    seminars = {}
    for html in htmls:
        seminar = {}
        html = html[html.index("<a\n href="):]
        seminar["url"] = html.split('"')[1]
        seminar["speaker"] = html.split("Seminar:")[1].split('"')[0].strip()
        seminar["blurb"] = html.split("<p>")[1].split("</p>")[0].replace("[&hellip;]","").strip()
        print(seminar)
    return seminars

def parse_Genetics_seminars(html):
    return html.split("views-field views-field-title")[1:]

def jprint(content):
    print(json.dumps(content,indent=4))

def main():
    seminars = {}
    html_cache = os.path.dirname(__file__) + "/html_cache.json"
    today = int(str(date.today()).replace("-",""))
    urls = {
        "ID":"https://vet.uga.edu/events/category/infectious-diseases/list/",
        "Genetics":"https://www.genetics.uga.edu/events/seminars"
    }
    try:
        with open(html_cache,"r") as input:
            raw_html = json.load(input)
    except: raw_html = {}
    any_fetched = False
    for department in urls:
        fetch = True
        if department in raw_html:
            if raw_html[department]["fetched"] == today: fetch = False
        else: raw_html[department] = {}
        if fetch:
            print(f"FETCHING {department.upper()} FROM WEB")
            any_fetched = True
            raw_html[department]["fetched"] = today
            request = Request(
                url=urls[department],
                headers={"User-Agent":"Mozilla/5.0"}
            )
            raw_html[department]["html"] = urlopen(request).read().decode("utf8")
    if any_fetched:
        with open(html_cache,"w") as output:
            json.dump(raw_html, output, indent=4)

    for department in raw_html:
        jprint(globals()[f"parse_{department}_seminars"](raw_html[department]["html"]))


if __name__ == "__main__":
    main()