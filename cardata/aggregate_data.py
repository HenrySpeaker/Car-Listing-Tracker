from csv import DictReader, DictWriter


def get_first_model(model_str):
    start = 0

    while start < len(model_str) and model_str[start] in '"[]':
        start += 1

    end = start

    while end < len(model_str) and model_str[end] not in '"[]':
        end += 1

    return model_str[start:end]


data_collected = {}

for year in range(1992, 2025):
    with open(f"car-data/{year}.csv", "r") as file:
        reader = DictReader(file)

        for row in reader:
            if row["make"] not in data_collected:
                data_collected[row['make']] = {}

            if row["model"] not in data_collected[row['make']]:
                data_collected[row["make"]][row["model"]
                                            ] = get_first_model(row["body_styles"])


with open("car-data/all-models.csv", "w", newline="") as file:
    writer = DictWriter(
        file, fieldnames=["make", "model", "body_style"])
    writer.writeheader()

    for make in data_collected:
        for model in data_collected[make]:
            row = {"make": make, "model": model,
                   "body_style": data_collected[make][model]}
            writer.writerow(row)
