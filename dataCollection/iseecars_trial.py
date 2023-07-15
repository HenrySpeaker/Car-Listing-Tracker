import requests

headers = {
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Gpc": "1",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "Accept-Language": "en-GB,en;q=0.9"
}
proxies = {
    "http": "http://50.96.204.251:18351"
}
iseecars_url = "https://www.iseecars.com/cars-for-sale?Location=50123&Radius=50&Make=&Model=&Year_min=&Year_max=&Trim=&Price_min=&Price_max=&DealerRating=0&Mileage_min=&Mileage_max=&range_pricebelowmarket_min=&PriceBelowMarket_min=&PriceBelowMarket_max=&range_pricedrop_min=&PriceDrop_min=&PriceDrop_max=&range_daysonmarket_min=0&range_daysonmarket_max=0&DaysOnMarket_min=&DaysOnMarket_max=&range_mpg_min=0&range_mpg_max=0&MPG_min=&MPG_max=&range_legroom_min=&range_headroom_min=&range_height_min=&range_torsoleglength_min=2&LegRoom_min=&HeadRoom_min=&LegRoom_max=&HeadRoom_max=&range_cargovolume_min=0&range_cargovolume_max=0&CargoRoom_min=&CargoRoom_max=&Engine=&range_horsepower_min=0&range_horsepower_max=0&Horsepower_min=&Horsepower_max=&DriveType=&Color=&InteriorColor=&range_bedlength_min=1.5&range_bedlength_max=1.5&Bed+Length_min=&Bed+Length_max=&range_towingcapacity_min=0&range_towingcapacity_max=0&TowingCapacity_min=&TowingCapacity_max=&Keywords=&visibleKeywords=&Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&DealerId=&_t=a&_c=&offset=0&maxResults=100&sort=BestDeal&sortOrder=desc&lfc_t0=MTY4NjUxMzYxOTA2Nw%3D%3D"
iseecarsurl2 = "https://www.iseecars.com/cars-for-sale?Location=90210&Radius=50&Make=&Model=&Year_min=&Year_max=&Trim=&Price_min=&Price_max=&DealerRating=0&Mileage_min=&Mileage_max=&range_pricebelowmarket_min=&PriceBelowMarket_min=&PriceBelowMarket_max=&range_pricedrop_min=&PriceDrop_min=&PriceDrop_max=&range_daysonmarket_min=0&range_daysonmarket_max=0&DaysOnMarket_min=&DaysOnMarket_max=&range_mpg_min=0&range_mpg_max=0&MPG_min=&MPG_max=&range_legroom_min=&range_headroom_min=&range_height_min=&range_torsoleglength_min=2&LegRoom_min=&HeadRoom_min=&LegRoom_max=&HeadRoom_max=&range_cargovolume_min=0&range_cargovolume_max=0&CargoRoom_min=&CargoRoom_max=&Engine=&range_horsepower_min=0&range_horsepower_max=0&Horsepower_min=&Horsepower_max=&DriveType=&Color=&InteriorColor=&range_bedlength_min=1.5&range_bedlength_max=1.5&Bed+Length_min=&Bed+Length_max=&range_towingcapacity_min=0&range_towingcapacity_max=0&TowingCapacity_min=&TowingCapacity_max=&Keywords=&visibleKeywords=&Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&DealerId=&_t=a&_c=&offset=20&maxResults=20&sort=BestDeal&sortOrder=desc&lfc_t0=MTY4NjUxMzYxOTA2Nw%3D%3D"
autote = "https://www.iseecars.com/cars-for-sale?Location=90210&Radius=50&Make=ford&Model=crown+victoria&Year_min=&Year_max=&Trim=&Price_min=&Price_max=&DealerRating=0&Mileage_min=&Mileage_max=&range_pricebelowmarket_min=&PriceBelowMarket_min=&PriceBelowMarket_max=&range_pricedrop_min=&PriceDrop_min=&PriceDrop_max=&range_daysonmarket_min=-5&range_daysonmarket_max=185&DaysOnMarket_min=&DaysOnMarket_max=&range_mpg_min=0&range_mpg_max=50&MPG_min=&MPG_max=&range_legroom_min=&range_headroom_min=&range_height_min=&range_torsoleglength_min=2&LegRoom_min=&HeadRoom_min=&LegRoom_max=&HeadRoom_max=&range_cargovolume_min=0&range_cargovolume_max=505&CargoRoom_min=&CargoRoom_max=&Engine=&range_horsepower_min=0&range_horsepower_max=1050&Horsepower_min=&Horsepower_max=&DriveType=&Color=&InteriorColor=&range_bedlength_min=1.5&range_bedlength_max=8.5&Bed+Length_min=&Bed+Length_max=&range_towingcapacity_min=0&range_towingcapacity_max=25100&TowingCapacity_min=&TowingCapacity_max=&Keywords=&visibleKeywords=&Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&DealerId=&_t=a&_c=&offset=0&maxResults=20&sort=LastPriceDropDate&sortOrder=desc&lfc_t0=MTY4NjUxMzYxOTA2Nw%3D%3D"
url2 = "https://www.iseecars.com/cars-for-sale?Location=50123&Radius=50&Make=&Model=&Year_min=&Year_max=&Trim=&Price_min=&Price_max=&DealerRating=0&Mileage_min=&Mileage_max=&range_pricebelowmarket_min=&PriceBelowMarket_min=&PriceBelowMarket_max=&range_pricedrop_min=&PriceDrop_min=&PriceDrop_max=&range_daysonmarket_min=0&range_daysonmarket_max=0&DaysOnMarket_min=&DaysOnMarket_max=&range_mpg_min=0&range_mpg_max=0&MPG_min=&MPG_max=&range_legroom_min=&range_headroom_min=&range_height_min=&range_torsoleglength_min=2&LegRoom_min=&HeadRoom_min=&LegRoom_max=&HeadRoom_max=&range_cargovolume_min=0&range_cargovolume_max=0&CargoRoom_min=&CargoRoom_max=&Engine=&range_horsepower_min=0&range_horsepower_max=0&Horsepower_min=&Horsepower_max=&DriveType=&Color=&InteriorColor=&range_bedlength_min=1.5&range_bedlength_max=1.5&Bed+Length_min=&Bed+Length_max=&range_towingcapacity_min=0&range_towingcapacity_max=0&TowingCapacity_min=&TowingCapacity_max=&Keywords=&visibleKeywords=&Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&DealerId=&_t=a&_c=&offset=0&maxResults=20&sort=LastPriceDropDate&sortOrder=desc&lfc_t0=MTY4NjUxMzYxOTA2Nw%3D%3D"

res = requests.get(autote,
                   headers=headers, proxies=proxies)

print(f"cookies: {res.cookies}")
print(f"headers: {res.headers}")
print(f"history: {res.history}")
print(f"url: {res.url}")
# print(f"text: {res.text}")

with open('result.html', "w", encoding="utf-8") as file:
    file.write(res.text)

url1 = "https://www.iseecars.com/cars-for-sale?Location=20910&Radius=50&Make=&Model=&Year_min=&Year_max=&Trim=&Price_min=&Price_max=&DealerRating=0&Mileage_min=&Mileage_max=&range_pricebelowmarket_min=&PriceBelowMarket_min=&PriceBelowMarket_max=&range_pricedrop_min=&PriceDrop_min=&PriceDrop_max=&range_daysonmarket_min=0&range_daysonmarket_max=0&DaysOnMarket_min=&DaysOnMarket_max=&range_mpg_min=0&range_mpg_max=0&MPG_min=&MPG_max=&range_legroom_min=&range_headroom_min=&range_height_min=&range_torsoleglength_min=2&LegRoom_min=&HeadRoom_min=&LegRoom_max=&HeadRoom_max=&range_cargovolume_min=0&range_cargovolume_max=0&CargoRoom_min=&CargoRoom_max=&Engine=&range_horsepower_min=0&range_horsepower_max=0&Horsepower_min=&Horsepower_max=&DriveType=&Color=&InteriorColor=&range_bedlength_min=1.5&range_bedlength_max=1.5&Bed+Length_min=&Bed+Length_max=&range_towingcapacity_min=0&range_towingcapacity_max=0&TowingCapacity_min=&TowingCapacity_max=&Keywords=&visibleKeywords=&Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&DealerId=&_t=a&_c=&offset=40&maxResults=20&sort=BestDeal&sortOrder=desc&lfc_t0=MTY4NjUxMzYxOTA2Nw%3D%3D"

proxy_res = requests.get("http://jsonip.com",
                         headers=headers, proxies={"http": "http://146.56.150.146:32241"})
print(f"proxy response is {proxy_res.content}")