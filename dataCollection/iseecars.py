import requests
from bs4 import BeautifulSoup
from dataCollection.headers import headers


def get_iseecars_listings(criteria: dict) -> list[dict]:
    cars_found = []

    iseecars_url = f"https://www.iseecars.com/cars-for-sale?Location={criteria.get('zip_code', '')}&Radius={criteria.get('search_distance', '')}&Make={criteria.get('make', '')}&Model={criteria.get('model', '')}&Year_min={criteria.get('min_year', '')}&Year_max={criteria.get('max_year')}&Trim=&Price_min={criteria.get('min_price', '')}&Price_max={criteria.get('max_price', '')}&DealerRating=0&Mileage_min=&Mileage_max={criteria.get('max_mileage')}&range_pricebelowmarket_min=&PriceBelowMarket_min=&PriceBelowMarket_max=&range_pricedrop_min=&PriceDrop_min=&PriceDrop_max=&range_daysonmarket_min=0&range_daysonmarket_max=0&DaysOnMarket_min=&DaysOnMarket_max=&range_mpg_min=0&range_mpg_max=0&MPG_min=&MPG_max=&range_legroom_min=&range_headroom_min=&range_height_min=&range_torsoleglength_min=2&LegRoom_min=&HeadRoom_min=&LegRoom_max=&HeadRoom_max=&range_cargovolume_min=0&range_cargovolume_max=0&CargoRoom_min=&CargoRoom_max=&Engine=&range_horsepower_min=0&range_horsepower_max=0&Horsepower_min=&Horsepower_max=&DriveType=&Color=&InteriorColor=&range_bedlength_min=1.5&range_bedlength_max=1.5&Bed+Length_min=&Bed+Length_max=&range_towingcapacity_min=0&range_towingcapacity_max=0&TowingCapacity_min=&TowingCapacity_max=&Keywords=&visibleKeywords=&Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&DealerId=&_t=a&_c=&offset=0&maxResults=100&sort=BestDeal&sortOrder=desc&Bodystyle={criteria.get('isc_body_style', '')}"

    response = requests.get(iseecars_url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("article")

    for listing in articles:
        listing_info = {}

        listing_info["url"] = listing.attrs["listing-url"]

        additional_info_divs = listing.find_all(
            "div", attrs={"class": "additional-info-content-column"})

        for info_div in additional_info_divs:
            if "Price:" in info_div.find("b"):
                listing_info["price"] = "".join(
                    info_div.find("span").string[1:].split(","))

            if "VIN:" in info_div.find("b"):
                listing_info["vin"] = info_div.find("span").string

        listing_info["zip_code"] = listing.find(
            "div", attrs={"class": "storage"})["data-zip"]

        print(listing_info)

    return cars_found
