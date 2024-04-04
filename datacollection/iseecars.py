import re
from time import sleep
from contextlib import closing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datacollection.dc_logger import logger


PAGE_INCREMENT = 20
LISTING_COUNT_REGEX = r"(\d+\-\d+of)?([,\d]+)carsfound"


def get_listings_count(soup: BeautifulSoup) -> int:
    if soup.find("div", class_="no-result-box"):
        return 0

    page_limit = soup.find(id="cars_v2-results-header")

    page_limit_text = list(page_limit.stripped_strings)[0]
    page_limit_text = "".join(page_limit_text.split())
    page_limit_text = page_limit_text.replace(" ", "").lower()

    match = re.search(LISTING_COUNT_REGEX, page_limit_text)
    match_group = match.group(2).replace(",", "")

    if match:
        num_listings = int(match_group)
    else:
        num_listings = 0

    return num_listings


def get_isc_page_soup(driver, url):
    driver.get(url)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "section=pricing")))
    except TimeoutException:
        logger.warn(f"failed with url: {url}")
    finally:
        pass

    response = driver.page_source
    soup = BeautifulSoup(response, "html.parser")

    return soup


def get_iseecars_listings(criteria: dict) -> list[dict]:
    """
    Accepts a dictionary representing a specific search, scrapes the iseecars.com website, and returns a list of all cars matching the search criteria.
    """

    with closing(webdriver.Firefox()) as driver:
        cars_found = []
        iseecars_url = f"https://www.iseecars.com/cars-for-sale#autoZip=False&Location={criteria.get('zip_code', '')}&Radius={criteria.get('search_distance', '')}&Make={criteria.get('make', '')}&Model={criteria.get('model', '')}&Year_min={criteria.get('min_year', '')}&Year_max={criteria.get('max_year')}&Trim=&Price_min={criteria.get('min_price', '')}&Price_max={criteria.get('max_price', '')}&DealerRating=0&Mileage_min=&Mileage_max={criteria.get('max_mileage')}&range_pricebelowmarket_min=&PriceBelowMarket_min=&PriceBelowMarket_max=&range_pricedrop_min=&PriceDrop_min=&PriceDrop_max=&range_daysonmarket_min=0&range_daysonmarket_max=0&DaysOnMarket_min=&DaysOnMarket_max=&range_mpg_min=0&range_mpg_max=0&MPG_min=&MPG_max=&range_legroom_min=&range_headroom_min=&range_height_min=&range_torsoleglength_min=2&LegRoom_min=&HeadRoom_min=&LegRoom_max=&HeadRoom_max=&range_cargovolume_min=0&range_cargovolume_max=0&CargoRoom_min=&CargoRoom_max=&Engine=&range_horsepower_min=0&range_horsepower_max=0&Horsepower_min=&Horsepower_max=&DriveType=&Color=&InteriorColor=&range_bedlength_min=1.5&range_bedlength_max=1.5&Bed+Length_min=&Bed+Length_max=&range_towingcapacity_min=0&range_towingcapacity_max=0&TowingCapacity_min=&TowingCapacity_max=&Keywords=&visibleKeywords=&Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&Key+Features=&DealerId=&_t=a&_c=&offset=0&maxResults=20&sort=BestDeal&sortOrder=desc"
        soup = get_isc_page_soup(driver, iseecars_url)
        num_listings = get_listings_count(soup)
        curr_offset = 0

        while curr_offset < num_listings:
            sleep(0.1)

            iseecars_url = f"https://www.iseecars.com/cars-for-sale#autoZip=False&Location={criteria.get('zip_code', '')}&Radius={criteria.get('search_distance', '')}&Make={criteria.get('make', '')}&Model={criteria.get('model', '')}&Year_min={criteria.get('min_year', '')}&Year_max={criteria.get('max_year')}&Trim=&Price_min={criteria.get('min_price', '')}&Price_max={criteria.get('max_price', '')}&DealerRating=0&Mileage_min=&Mileage_max={criteria.get('max_mileage')}&offset={curr_offset}&maxResults=20&sort=BestDeal&sortOrder=desc"

            logger.info(f"accessing listings with offset {curr_offset} with url {iseecars_url}")
            driver.get(iseecars_url)
            soup = get_isc_page_soup(driver, iseecars_url)
            articles = soup.find_all("article")

            for listing in articles:
                # skip featured listings
                if listing.find("div.listing-meta-featured"):
                    continue

                listing_info = {}
                listing_info["url"] = listing.attrs["listing-url"]
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

    return cars_found
