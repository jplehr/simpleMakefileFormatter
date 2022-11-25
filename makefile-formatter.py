import argparse
import typing

parser = argparse.ArgumentParser()
parser.add_argument('filename',
                    type=str,
                    help='The name of the file to foramt')
parser.add_argument('outfile', type=str, help='The name of output file')

indent_width = 2
whitespace_after_paren = False
whitespace_before_paren = True
whitespace_around_operator = True

current_indent = 0

indent_increaser = ['ifeq', 'ifneq']
indent_decreaser = ['endif']
indent_dec_inc = ['else', 'elif']

rule_head_seen = False


def indent_line(line: str) -> str:
    global current_indent
    formatted_line = line
    for i in range(0, current_indent):
        for j in range(0, indent_width):
            formatted_line = ' ' + formatted_line

    return formatted_line


def is_make_rule_head(line: str) -> bool:
    '''
    Determines whether the current line is the head of a make rule
    '''
    res = line.find(':')
    return res != -1


def is_make_rule_body(line: str) -> bool:
    global rule_head_seen
    formatted_line = line.strip()

    if len(formatted_line) == 0:
        rule_head_seen = False
        return False

    if rule_head_seen:
        return True


def format_rule(line: str) -> str:
    formatted_line = line.strip()
    return '\t' + formatted_line


def format_rule_head(line: str) -> str:
    return line.strip()


def format_non_rule(line: str) -> str:
    formatted_line = line.strip()
    global current_indent

    for ii in indent_increaser:
        if formatted_line.startswith(ii):
            # print('Increase indent from ' + str(current_indent))
            formatted_line = indent_line(formatted_line)
            current_indent = 1 + current_indent
            return formatted_line

    for id in indent_decreaser:
        if formatted_line.startswith(id):
            # print('Decrease indent from ' + str(current_indent))
            current_indent = current_indent - 1
            formatted_line = indent_line(formatted_line)
            return formatted_line

    for tid in indent_dec_inc:
        if formatted_line.startswith(tid):
            current_indent = current_indent - 1
            formatted_line = indent_line(formatted_line)
            current_indent = current_indent + 1
            return formatted_line

    return indent_line(formatted_line)


def read_file(file_name: str, outfile: str) -> None:
    global rule_head_seen
    formatted_content = ''

    with open(file_name, "r") as f:
        for cur_line in f:
            formatted_line = ''

            if is_make_rule_body(cur_line):
                # print('Indent rule body')
                formatted_line = format_rule(cur_line)

            elif is_make_rule_head(cur_line):
                # print('Found rule head')
                formatted_line = format_rule_head(cur_line)
                rule_head_seen = True

            else:
                formatted_line = format_non_rule(cur_line)

            formatted_content += formatted_line + '\n'
            print(formatted_line)

    with open(outfile, 'w') as of:
        of.write(formatted_content)


if __name__ == '__main__':
    args = parser.parse_args()
    read_file(args.filename, args.outfile)