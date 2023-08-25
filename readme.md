# English vocabulary trainer

English vocabulary trainer -- the utility for learning words like quizelet or Anki.

## Using

1. Download this project.
2. Place vocabularies in "vocabularies" directory as plain text files.
Vocabulary format: each line is word (or expression) and its translation (or description) separated by tab ('\t').
3. Using terminal (command line) in this directory, type:
- `python english_vocabulary.py` -- shows help
- `python english_vocabulary.py list` -- list all availiable dictionaries in vocabularies directory.
- `python english_vocabulary.py look <dictname>` -- look at words from this vocabulary. This mode shows words, wait n seconds, shows translation, wait n seconds, shows next word, etc.
- `python english_vocabulary.py learn <dictname>` -- learn words: choose correct translation from n variants.
- `python english_vocabulary.py test <dictname>` -- learn words: type word, knowing its translation.

## Configuration

This trainer can be configured using `english_vocabulary.cfg`.

Options:
- `look_delay_time_s` -- sleep time for "look" mode,
- `vocabulary_dir` -- name of vocabularies directory,
- `learn_variants_number` -- number of shown variants of translation for "learn" mode.
