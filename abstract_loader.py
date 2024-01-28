import csv


def main():
    abstract_dict = {}
    no_abstract = []

    with open("data/abstract.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Abstract Note"] != "":
                abstract_dict[row["Key"]] = row["Abstract Note"]
            else:
                no_abstract.append(row["Key"])

    with open("data/prompt_abstract.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["key", "abstract"])
        for key, value in abstract_dict.items():
            writer.writerow([key, value])

    with open("data/no_abstract.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["prompt"])
        for key in no_abstract:
            writer.writerow([key])


if "__name__" == "__main__":
    main()
