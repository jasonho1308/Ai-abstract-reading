import csv
import re
from typing import List

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


def save_score(key: str, score1: int, score2: int, message: str) -> None:
    with open("output/abstract_score.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([key, score1, score2, message.replace("\n", "\\n")])


def get_score(message: str) -> List[int]:
    score1 = re.findall(r"score.*: (\d*)\(.*1\)", message)[0]
    score2 = re.findall(r"score.*: (\d*)\(.*2\)", message)[0]
    if score1 == "" or score2 == "":
        raise Exception("No score")
    return (int(score1), int(score2))


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
        print(f"{key}: {message}")
        try:
            score1, score2 = get_score(message)
            print(score1, score2)
            print()
        except Exception as e:
            with open("output/error.txt", "a") as f:
                f.write(f"{key}: {e}\n{message}\n")
        else:
            save_score(key, score1, score2, message)


if __name__ == "__main__":
    main()
