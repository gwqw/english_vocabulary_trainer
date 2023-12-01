"""
    search repeated words in all dictionaries
"""
import os
import sys
import typing as tp


SEP = '\t'


def get_words(vocabulary_path: str) -> tp.List[str]:
    res = []
    with open(vocabulary_path) as f:
        for line in f:
            line = line.strip()
            if not line or SEP not in line:
                continue
            words = line.split(SEP, maxsplit=1)
            assert len(words) == 2
            res.append(words[0])
    return res


def search_repeated_records(dict_path: str) -> tp.Dict[str, tp.List[str]]:
    vocabularies = [entry.name for entry in os.scandir(path=dict_path) if entry.is_file]
    vocabularies.sort()

    # add words from all dicts
    word2dicts = {}
    for dict_name in vocabularies:
        try:
            new_words = get_words(os.path.join(dict_path, dict_name))
            for word in new_words:
                word2dicts.setdefault(word, [])
                word2dicts[word].append(dict_name)
        except Exception:
            continue

    # filter unique recs
    return {k: v for k, v in word2dicts.items() if len(v) > 1}


def main():
    if len(sys.argv) <= 1:
        print("Enter path to dictionaries")
        sys.exit()

    dict_path = sys.argv[1]
    recs = search_repeated_records(dict_path)
    for word, dict_names in recs.items():
        print(f'"{word}" is found in dicts:\t{", ".join(dict_names)}')


if __name__ == "__main__":
    main()
