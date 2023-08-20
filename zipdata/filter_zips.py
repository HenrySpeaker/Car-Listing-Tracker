from csv import DictReader, DictWriter


def filter_zips():
    with open("ZipData/uszips.csv") as file:
        reader = DictReader(file)

        data = []

        for row in reader:
            data.append(
                {"zip": row["zip"], "city": row["city"], "state": row["state_name"]})

    with open("ZipData/zips.csv", "w", newline="") as file:
        writer = DictWriter(file, fieldnames=["zip", "city", "state"])
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    filter_zips()
