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

try:
    import readline  # noqa: only for linux
except ImportError:
    pass

CONFIG_NAME = "english_vocabulary_trainer.cfg"
SLEEP_TIME = 2
VOC_PATH = "vocabularies"
VARIANTS_TO_SELECT = 4
SEP = '\t'
SEP_LEARN = ' '

SEPARATORS = {
    "space": ' ',
    "tab": '\t',
    "eol": '\n',
}


@dataclass
class Config:
    sleep_time: int = SLEEP_TIME
    voc_path: str = VOC_PATH
    variants_to_select: int = VARIANTS_TO_SELECT
    separator_for_learn: str = SEP_LEARN


CONFIG = Config()
INF = 1000000


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
    CONFIG.separator_for_learn = SEPARATORS.get(
        parameters.get("separator_for_learn", "space").lower(),
        SEP_LEARN
    )


def _read_vocabulary(*vocabulary_paths: tp.List[str], max_size: int = -1) -> tp.Dict[str, str]:
    if max_size < 0:
        max_size = INF
    vocabulary_paths = [os.path.join(CONFIG.voc_path, vocabulary_path) for vocabulary_path in vocabulary_paths]
    vocabulary = {}
    for vocabulary_path in vocabulary_paths:
        with open(vocabulary_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if SEP not in line:
                    raise RuntimeError(f"line {line} is without separator '{SEP}', dict file: {vocabulary_path}")
                words = line.split(SEP, maxsplit=1)
                assert len(words) == 2
                vocabulary[words[0].strip()] = words[1].strip()
                if len(vocabulary) >= max_size:
                    break
        if len(vocabulary) >= max_size:
            break

    return vocabulary


def _check_vocabulary(vocabulary: tp.Dict[str, str]) -> bool:
    return bool(vocabulary)


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


def look_words(vocabulary: tp.Dict[str, str]) -> None:
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


def _safe_parse_int(value: str) -> int:
    try:
        return int(value)
    except Exception:
        return 0


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
                print(f'{j+1}: {variant}', end=CONFIG.separator_for_learn)
            print()
            guess = _safe_parse_int(input())-1
            if guess < 0 or guess >= len(variants) or variants[guess] != item[1]:
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


def learn_words(vocabulary: tp.Dict[str, str]) -> None:
    """select translation from english from variants"""
    items = _get_shuffled_list(vocabulary)
    tranlations = _get_all_translations(vocabulary)
    print("select correct variant (type number and press enter)")
    _learn_with_variants(items, tranlations)


def test_words(vocabulary: tp.Dict[str, str]) -> None:
    """learn english writing"""
    items = _get_shuffled_list(vocabulary)
    print("write english translation to words")
    _learn_writing(items)


def _read_and_check_vocabulary(args: tp.List[str]) -> tp.Dict[str, str]:
    vocabulary = _read_vocabulary(*args)
    if not _check_vocabulary(vocabulary):
        print("error: no vocabulary filename or empty vocabulary")
        sys.exit()
    return vocabulary


def main():
    if len(sys.argv) <= 1:
        print(
        """
Program for learing new words:
    list -- list all availiable dictionaries
    look <dictname>[ <dictname>...] -- look at words and their translations
    learn <dictname>[ <dictname>...] -- learn words (choose correct translation from variants)
    test <dictname>[ <dictname>...] -- test words (type word by its translation)
        """)
        sys.exit()

    _read_and_update_config()

    command = sys.argv[1]
    if command == 'list':
        list_dicts()
    elif command == 'look':
        vocabulary = _read_and_check_vocabulary(sys.argv[2:])
        look_words(vocabulary)
    elif command == 'learn':
        vocabulary = _read_and_check_vocabulary(sys.argv[2:])
        learn_words(vocabulary)
    elif command == 'test':
        vocabulary = _read_and_check_vocabulary(sys.argv[2:])
        test_words(vocabulary)
    else:
        print('unknown command:', command)


if __name__ == '__main__':
    main()
