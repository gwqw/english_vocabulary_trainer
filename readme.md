# English vocabulary trainer

English vocabulary trainer -- python script for learning words like quizelet or Anki.

## Usage

1. Download (clone) this project.
2. Place vocabularies in "vocabularies" directory as plain text files.
Vocabulary format: each line is a word (or expression) and its translation (or description), separated by tab ('\t').
3. Using terminal (command line) in this directory, type:
- `python english_vocabulary_trainer.py` -- shows help
- `python english_vocabulary_trainer.py list` -- lists all availiable dictionaries in vocabularies directory.
- `python english_vocabulary_trainer.py look <dictname>` -- look at words from this vocabulary. This mode shows words, waits n seconds, shows translation, waits n seconds, shows next word, etc.
- `python english_vocabulary_trainer.py learn <dictname>` -- learn words: choose correct translation from n variants. Type correct number and press enter.
- `python english_vocabulary_trainer.py test <dictname>` -- learn words: type word, knowing its translation.

## Configuration

This trainer can be configured using `english_vocabulary_trainer.cfg`.

Options:
- `look_delay_time_s` -- sleep time for "look" mode,
- `vocabulary_dir` -- name of vocabulary directory,
- `learn_variants_number` -- number of shown variants of translation for "learn" mode.
