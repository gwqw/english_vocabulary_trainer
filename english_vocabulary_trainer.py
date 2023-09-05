"""
    list -- list of availiable dictionaries
    look <dictname> -- look at words
    learn <dictname> -- learn words
    test <dictname> -- test words
"""
import os
import random
import sys
import typing as tp
from dataclasses import dataclass
from time import sleep

CONFIG_NAME = "english_vocabulary_trainer.cfg"
SLEEP_TIME = 2
VOC_PATH = "vocabularies"
VARIANTS_TO_SELECT = 4
SEP = '\t'


@dataclass
class Config:
    sleep_time: int = SLEEP_TIME
    voc_path: str = VOC_PATH
    variants_to_select: int = VARIANTS_TO_SELECT


CONFIG = Config()


def _read_and_update_config() -> None:
    parameters = {}
    with open(CONFIG_NAME) as f:
        for l in f:
            if '=' not in l: continue
            n, v = [w.strip() for w in l.split('=', maxsplit=1)]
            parameters[n] = v

    CONFIG.sleep_time = int(parameters.get("look_delay_time_s", SLEEP_TIME))
    CONFIG.voc_path = parameters.get("vocabulary_dir", VOC_PATH)
    CONFIG.variants_to_select = int(parameters.get("learn_variants_number", VARIANTS_TO_SELECT))


def _read_vocabulary(vocabulary_path: str) -> tp.Dict[str, str]:
    vocabulary_path = os.path.join(CONFIG.voc_path, vocabulary_path)
    vocabulary = {}
    with open(vocabulary_path) as f:
        for line in f:
            line = line.strip()
            if not line or SEP not in line:
                continue
            words = line.split(SEP, maxsplit=1)
            assert len(words) == 2
            vocabulary[words[0]] = words[1]
    return vocabulary


def _get_shuffled_list(vocabulary: tp.Dict[str, str]) -> tp.List[tp.Tuple[str, str]]:
    items = list(vocabulary.items())
    random.shuffle(items)
    return items


def _get_all_translations(vocabulary: tp.Dict[str, str]) -> tp.List[str]:
    return list(vocabulary.values())


def list_dicts():
    vocabularies = [entry.name for entry in os.scandir(path=CONFIG.voc_path) if entry.is_file]
    vocabularies.sort()
    for name in vocabularies:
        print(name)


def look_words(vocabulary_path: str):
    vocabulary = _read_vocabulary(vocabulary_path)
    items = _get_shuffled_list(vocabulary)
    n = len(items)
    for i, item in enumerate(items):
        print(f"{i+1}/{n}: {item[0]}")
        sleep(CONFIG.sleep_time)
        print(item[1])
        sleep(CONFIG.sleep_time)


def _get_n_random_translations(translations: tp.List[str], n=4, include=None) -> tp.List[str]:
    assert translations
    n = min(n, len(translations))
    res = random.sample(translations, n)
    if include and include not in res:
        res.pop()
        res.append(include)
    return res


def _learn_with_variants(items: tp.List[tp.Tuple[str, str]], translations: tp.List[str]):
    unlearned = set(items)
    while unlearned:
        n = len(unlearned)
        unlearned_new = set()
        for i, item in enumerate(unlearned):
            print(f'{i+1}/{n}: {item[0]}:')
            variants = _get_n_random_translations(
                translations, n=CONFIG.variants_to_select, include=item[1])
            random.shuffle(variants)
            for j, variant in enumerate(variants):
                print(f'{j+1}: {variant}', end=' ')
            print()
            guess = int(input())-1
            if guess >= len(variants) or variants[guess] != item[1]:
                print('wrong! correct answer:', item[1])
                unlearned_new.add(item)
            else:
                print('correct!')
            print()
        unlearned = unlearned_new


def _learn_writing(items):
    unlearned = set(items)
    while unlearned:
        n = len(unlearned)
        unlearned_new = set()
        for i, item in enumerate(unlearned):
            print(f'{i+1}/{n}: {item[1]}:')
            guess = input().strip()
            if guess.lower() != item[0].lower():
                print('wrong! correct answer:', item[0])
                unlearned_new.add(item)
            else:
                print('correct!')
            print()
        unlearned = unlearned_new


def learn_words(vocabulary_path: str):
    """select translation from english from variants"""
    vocabulary = _read_vocabulary(vocabulary_path)
    items = _get_shuffled_list(vocabulary)
    tranlations = _get_all_translations(vocabulary)
    print("select correct variant (type number and press enter)")
    _learn_with_variants(items, tranlations)


def test_words(vocabulary_path: str):
    """learn english writing"""
    vocabulary = _read_vocabulary(vocabulary_path)
    items = _get_shuffled_list(vocabulary)
    print("write english translation to words")
    _learn_writing(items)


def main():
    if len(sys.argv) <= 1:
        print(
        """
Program for learing new words:
    list -- list all availiable dictionaries
    look <dictname> -- look at words and their translations
    learn <dictname> -- learn words (choose correct translation from variants)
    test <dictname> -- test words (type word by its translation)
        """)
        sys.exit()

    _read_and_update_config()

    command = sys.argv[1]
    if command == 'list':
        list_dicts()
    elif command == 'look':
        look_words(sys.argv[2])
    elif command == 'learn':
        learn_words(sys.argv[2])
    elif command == 'test':
        test_words(sys.argv[2])
    else:
        print('unknown command:', command)


if __name__ == '__main__':
    main()
