import requests

with open("datacollection/page_dump/test.html", "w", encoding="utf-8") as f:
    f.write(requests.get("https://www.iseecars.com/cars-for-sale#autoZip=False&Location=90210&Radius=all&Make=Aston+Martin&Model=Vantage&Year_min=1992&Year_max=2023&Price_max=1000000&_t=a&offset=80&maxResults=20&sort=BestDeal&sortOrder=desc&lfc_t0=MTcwNjM4OTQ1MDc5MQ%3D%3D").text)