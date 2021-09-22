import re


def read_re(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        line = f.readline()
        return line


def pre_process(src_reg_text):
    alphabet = r'([0-9]|[a-z]|[A-Z]|[()|*])*$'
    src_reg_text = src_reg_text.replace(' ', '')
    pattern = re.compile(alphabet)
    match = pattern.match(src_reg_text)
    if match:
        pass
    else:
        print('Wrong characters.')
    reg_text = ''
    for i in range(len(src_reg_text)):
        if len(reg_text) == 0:
            reg_text += src_reg_text[i]
        else:
            if src_reg_text[i] == '|' or src_reg_text[i] == '*' or src_reg_text[i] == ')':
                reg_text += (src_reg_text[i])
            else:
                if src_reg_text[i - 1] == '(' or src_reg_text[i - 1] == '|':
                    reg_text += (src_reg_text[i])
                else:
                    reg_text += ('&' + src_reg_text[i])
    reg_text += '#'
    return reg_text
