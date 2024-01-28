import csv
import re

from gpt import MyGPT


def get_abstracts() -> dict:
    with open("data/prompt_abstract.csv", "r") as f:
        reader = csv.DictReader(f)
        abstract_dict = {row["key"]: row["abstract"] for row in reader}

    with open("output/abstract_score.csv", "r") as f:
        reader = csv.DictReader(f)
        key_to_remove = [row["Key"] for row in reader]
        for key in key_to_remove:
            del abstract_dict[key]

    return abstract_dict


def save_score(key: str, score: int) -> None:
    with open("output/abstract_score.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([key, score])


def get_score(message: str) -> int:
    re.findall(r"score: (\d*)", message)[0]


def main():
    with open("instruction.txt", "r") as f:
        instruction = f.read()

    with open("prompt.txt", "r") as f:
        prompt = f.read()

    gpt = MyGPT(instruction, prompt)

    abstracts_list = get_abstracts()

    for key, abstract in abstracts_list.items():
        result = gpt.get_result(abstract, "gpt-4-1106-preview")
        message = result.choices[0].message.content
        try:
            score = get_score(message)
        except Exception as e:
            with open("error.txt", "a") as f:
                f.write(f"{key}: {e}\n{message}\n")
        else:
            save_score(key, score)


if __name__ == "__main__":
    main()
