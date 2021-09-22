from regex import atom_reg, concat_reg, union_reg
from utils import read_re, pre_process
from graphviz import Digraph


special_ch = ['(', ')', '*', '|', '&', '#']
special_order = {
    '*': 0,
    '&': 1,
    '|': 2,
    '(': 3,
    ')': 4,
    '#': 5
}
priority = [
   #  *   &   |   (   )   #
    [ 1,  1,  1, -1,  1,  1],
    [-1,  1,  1, -1,  1,  1],
    [-1, -1,  1, -1,  1,  1],
    [-1, -1, -1, -1,  0,  2],
    [ 2,  2,  2,  2,  2,  2],
    [-1, -1, -1, -1, -1, -2]
]


def process_regs(src_reg_text):
    reg_text = pre_process(src_reg_text)
    # process
    label_stack = []
    regex_stack = []
    label_stack.append('#')
    i = 0
    while i < len(reg_text):
        ch = reg_text[i]
        if ch not in special_ch:
            regex_stack.append(atom_reg(ch))
            i += 1
        else:
            case = priority[special_order[label_stack[-1]]][special_order[ch]]
            if case == -1:
                label_stack.append(ch)
                i += 1
            elif case == 1:
                label = label_stack[-1]
                if label == '&':
                    reg2 = regex_stack.pop()
                    reg1 = regex_stack.pop()
                    if isinstance(reg1, concat_reg) and not reg1.repeat_flag:
                        reg1.add(reg2)
                        regex_stack.append(reg1)
                    else:
                        tmp_concat_reg = concat_reg()
                        tmp_concat_reg.add(reg1)
                        tmp_concat_reg.add(reg2)
                        regex_stack.append(tmp_concat_reg)
                    label_stack.pop()
                elif label == '|':
                    reg2 = regex_stack.pop()
                    reg1 = regex_stack.pop()
                    regex_stack.append(union_reg(reg1, reg2))
                    label_stack.pop()
                elif label == '*':
                    regex_stack[-1].set_repeat()
                    label_stack.pop()
            elif case == 0:
                label_stack.pop()
                i += 1
            elif case == -2:
                break
            else:
                pass
    return regex_stack[0]


def visual(nfa):
    dot = Digraph(comment='NFA', format="png")
    for node in nfa.nodes:
        dot.node(node.__str__(), node.__str__())

    for edge in nfa.edges:
        if edge.symbol != 'epsilon':
            dot.edge(edge.start_node.__str__(), edge.end_node.__str__(), edge.symbol)
        else:
            dot.edge(edge.start_node.__str__(), edge.end_node.__str__(), 'ε')

    dot.view()


if __name__ == '__main__':
    reg = process_regs(read_re('res.txt'))
    reg.init_nfa()
    reg.print_nfa()
    visual(reg.nfa)
