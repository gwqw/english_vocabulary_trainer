"""
    convert dictionary from '\n'-separated format for '\t'-separated format
"""
import sys
import os.path


def _make_output_filename(input_filename: str) -> str:
    fname, _ = os.path.splitext(input_filename)
    return fname + ".out"


def convert(input_filename: str, output_filename: str) -> None:
    with open(input_filename) as f, open(output_filename, 'w') as g:
        is_first = True
        for line in f:
            line = line.strip()
            if not line:
                continue
            g.write(line)
            if is_first:
                g.write('\t')
                is_first = False
            else:
                g.write('\n')
                is_first = True


def main():
    if len(sys.argv) <= 1:
        print("Enter input dictionary filename")
        sys.exit()

    input_filename = sys.argv[1]
    output_filename = _make_output_filename(input_filename)
    convert(input_filename, output_filename)


if __name__ == "__main__":
    main()