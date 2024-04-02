import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from datacollection.headers import headers
from datacollection.dc_logger import logger

PAGE_INCREMENT = 20
LISTING_COUNT_REGEX = r"(\d+\-\d+of)?(\d+)carsfound"

driver = webdriver.Firefox()

def get_iseecars_listings(criteria: dict) -> list[dict]:
    """
    Accepts a dictionary representing a specific search, scrapes the iseecars.com website, and returns a list of all cars matching the search criteria.
    """
    cars_found = []

    iseecars_url = f"https://www.iseecars.com/cars-for-sale?Location={criteria.get('zip_code', '')}&Radius={criteria.get('search_distance', '')}&Make={criteria.get('make', '')}&Model={criteria.get('model', '')}&Year_min={criteria.get('min_year', '')}&Year_max={criteria.get('max_year')}&Trim=&Price_min={criteria.get('min_price', '')}&Price_max={criteria.get('max_price', '')}&DealerRating=0&Mileage_min=&Mileage_max={criteria.get('max_mileage')}&range_pricebelowmarket_min=&PriceBelowMarket_min=&PriceBelowMarket_max=&range_pricedrop_min=&PriceDrop_min=&PriceDrop_max=&range_daysonmarket_min=0&range_daysonmarket_max=0&DaysOnMarket_min=&DaysOnMarket_max=&range_mpg_min=0&range_mpg_max=0&MPG_min=&MPG_max=&range_legroom_min=&range_headroom_min=&range_height_min=&range_torsoleglength_min=2&LegRoom_min=&HeadRoom_min=&LegRoom_max=&HeadRoom_max=&range_cargovolume_min=0&range_cargovolume_max=0&CargoRoom_min=&CargoRoom_max=&Engine=&range_horsepower_min=0&range_horsepower_max=0&Horsepower_min=&Horsepower_max=&DriveType=&Color=&InteriorColor=&range_bedlength_min=1.5&range_bedlength_max=1.5&Bed+Length_min=&Bed+Length_max=&range_towingcapacity_min=0&range_towingcapacity_max=0&TowingCapacity_min=&TowingCapacity_max=&Keywords=&visibleKeywords=&Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&DealerId=&_t=a&_c=&offset=0&maxResults=100&sort=BestDeal&sortOrder=desc"
    iseecars_url = f"https://www.iseecars.com/cars-for-sale#autoZip=False&Location={criteria.get('zip_code', '')}&Radius={criteria.get('search_distance', '')}&Make={criteria.get('make', '')}&Model={criteria.get('model', '')}&Year_min={criteria.get('min_year', '')}&Year_max={criteria.get('max_year')}&Price_max={criteria.get('max_price', '')}&_t=a&offset=80&maxResults=20&sort=BestDeal&sortOrder=desc"

    response = requests.get(iseecars_url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    page_limit = soup.find(id="cars_v2-results-header")

    whitespace_chars = " \t foo \n bar "

    page_limit_text = list(page_limit.stripped_strings)[0]

    page_limit_text = "".join(page_limit_text.split(whitespace_chars))
    
    page_limit_text = page_limit_text.replace(" ", "").lower()

    logger.info(page_limit_text)

    match = re.search(LISTING_COUNT_REGEX, page_limit_text)

    logger.info(match)

    match_group = match.group(2)

    logger.info(match_group)

    if match:
        num_listings = int(match_group)

    else:
        num_listings = 0

    logger.info(num_listings)

    curr_offset = 0

    while curr_offset < num_listings:


        # iseecars_url = f"https://www.iseecars.com/cars-for-sale?Location={criteria.get('zip_code', '')}&Radius={criteria.get('search_distance', '')}&Make={criteria.get('make', '')}&Model={criteria.get('model', '')}&Year_min={criteria.get('min_year', '')}&Year_max={criteria.get('max_year')}&Trim=&Price_min={criteria.get('min_price', '')}&Price_max={criteria.get('max_price', '')}&DealerRating=0&Mileage_min=&Mileage_max={criteria.get('max_mileage')}&offset={curr_offset}&maxResults=20&sort=BestDeal&sortOrder=desc"
        iseecars_url = f"https://www.iseecars.com/cars-for-sale#autoZip=False&Location={criteria.get('zip_code', '')}&Radius={criteria.get('search_distance', '')}&Make={criteria.get('make', '')}&Model={criteria.get('model', '')}&Year_min={criteria.get('min_year', '')}&Year_max={criteria.get('max_year')}&Price_max={criteria.get('max_price', '')}&_t=a&offset=80&maxResults=20&sort=BestDeal&sortOrder=desc"
        
        logger.info(f"accessing listings with offset {curr_offset} with url {iseecars_url}")
        driver.get(iseecars_url)
        response = driver.page_source

        soup = BeautifulSoup(response, "html.parser")

        with open(f"datacollection/page_dump/dump_offset{curr_offset}.html", "w") as f:
            f.write(response.text)

        articles = soup.find_all("article")

        for listing in articles:
            listing_info = {}

            listing_info["url"] = listing.attrs["listing-url"]

            logger.info(f"listing found with url {listing_info['url']}")

            additional_info_divs = listing.find_all(
                "div", attrs={"class": "additional-info-content-column"})

            for info_div in additional_info_divs:
                if "Price:" in info_div.find("b"):
                    listing_info["price"] = int("".join(
                        info_div.find("span").string[1:].split(",")))

                if "VIN:" in info_div.find("b"):
                    listing_info["vin"] = info_div.find("span").string

                if "Mileage:" in info_div.find("b"):
                    mileage_text = info_div.find("span").string
                    mileage_text = mileage_text.split(" ")[0]
                    mileage_list = mileage_text.split(",")
                    mileage = 0
                    for term in mileage_list:
                        mileage = mileage * 1000 + int(term)

                    listing_info["mileage"] = mileage

            additional_data = listing.find(
                "div", attrs={"class": "storage"})

            listing_info["zip_code"] = int(additional_data["data-zip"]
                                        if "data-zip" in additional_data else criteria.get('zip_code', 1))

            try:
                listing_info["model_year"] = int(
                    additional_data["data-label"].split()[0])
            except ValueError:
                listing_info["model_year"] = None

            if "vin" not in listing_info or "price" not in listing_info:
                continue

            cars_found.append(listing_info)
        
        curr_offset += PAGE_INCREMENT

    logger.info(cars_found)

    logger.info(len(cars_found))

    return cars_found
