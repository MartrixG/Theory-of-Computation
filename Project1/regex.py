import queue


class regex:
    def __init__(self):
        self.repeat_flag = False
        self.atom_flag = False
        self.nfa = None

    def set_repeat(self):
        self.repeat_flag = True

    def init_nfa(self):
        if self.repeat_flag:
            node1 = self.nfa.start_node
            node1.update_name('1')
            node2 = self.nfa.end_node
            node2.update_name('2')
            self.nfa.start_node = Node('start')
            self.nfa.end_node = Node('end')
            self.nfa.nodes.add(self.nfa.start_node)
            self.nfa.nodes.add(self.nfa.end_node)
            self.nfa.add_edge(self.nfa.start_node, node1, 'epsilon')
            self.nfa.add_edge(self.nfa.start_node, self.nfa.end_node, 'epsilon')
            self.nfa.add_edge(node2, node1, 'epsilon')
            self.nfa.add_edge(node2, self.nfa.end_node, 'epsilon')

    def update_node_id(self):
        i = 0
        nodes = self.nfa.nodes
        edges = self.nfa.edges

        vis = {}
        for node in nodes:
            vis[node] = 0

        q = queue.Queue()
        q.put(self.nfa.start_node)
        vis[self.nfa.start_node] = 1
        while not q.empty():
            head = q.get()
            head.update_id(i)
            i += 1
            for edge in edges:
                if id(head) == id(edge.start_node) and vis[edge.end_node] == 0:
                    q.put(edge.end_node)
                    vis[edge.end_node] = 1

    def print_nfa(self):
        self.update_node_id()
        self.nfa.nodes = sorted(self.nfa.nodes)
        for node in self.nfa.nodes:
            for edge in self.nfa.edges:
                if id(node) == id(edge.start_node):
                    print('begin={:}, end={:}, symbol={:}'.format(edge.start_node.node_id, edge.end_node.node_id,
                                                                  edge.symbol))


class atom_reg(regex):
    def __init__(self, t):
        super(atom_reg, self).__init__()
        self.text = t

    def init_nfa(self):
        self.nfa = Nfa()
        self.nfa.start_node = Node('start')
        self.nfa.end_node = Node('end')
        self.nfa.nodes.add(self.nfa.start_node)
        self.nfa.nodes.add(self.nfa.end_node)
        self.nfa.add_edge(self.nfa.start_node, self.nfa.end_node, self.text)
        super(atom_reg, self).init_nfa()


class concat_reg(regex):
    def __init__(self):
        super(concat_reg, self).__init__()
        self.regs = []

    def add(self, reg):
        self.regs.append(reg)

    def init_nfa(self):
        for reg in self.regs:
            if reg.nfa is None:
                reg.init_nfa()

        self.nfa = Nfa()
        self.nfa = self.regs[0].nfa

        for i in range(len(self.regs)):
            if i != 0:
                now_nfa = self.regs[i].nfa
                for edge in now_nfa.edges:
                    if id(edge.start_node) == id(now_nfa.start_node):
                        self.nfa.nodes.add(edge.end_node)
                        self.nfa.add_edge(self.nfa.end_node, edge.end_node, edge.symbol)
                    else:
                        self.nfa.nodes.add(edge.start_node)
                        self.nfa.nodes.add(edge.end_node)
                        self.nfa.edges.add(edge)
                self.nfa.end_node = now_nfa.end_node
        
        super(concat_reg, self).init_nfa()


class union_reg(regex):
    def __init__(self, re1, re2):
        super(union_reg, self).__init__()
        self.reg1 = re1
        self.reg2 = re2

    def init_nfa(self):
        if self.reg1.nfa is None:
            self.reg1.init_nfa()
        if self.reg2.nfa is None:
            self.reg2.init_nfa()

        self.nfa = Nfa()
        self.nfa.start_node = Node('start')
        self.nfa.end_node = Node('end')
        self.nfa.nodes.add(self.nfa.start_node)
        self.nfa.nodes.add(self.nfa.end_node)
        self.nfa.add_edge(self.nfa.start_node, self.reg1.nfa.start_node, 'epsilon')
        self.nfa.add_edge(self.nfa.start_node, self.reg2.nfa.start_node, 'epsilon')
        self.reg1.nfa.add_edge(self.reg1.nfa.end_node, self.nfa.end_node, 'epsilon')
        self.reg2.nfa.add_edge(self.reg2.nfa.end_node, self.nfa.end_node, 'epsilon')

        for nfa in [self.reg1.nfa, self.reg2.nfa]:
            self.nfa.nodes |= nfa.nodes
            for edge in nfa.edges:
                self.nfa.edges.add(edge)
        
        super(union_reg, self).init_nfa()


class Node:
    def __init__(self, name):
        self.name = name
        self.node_id = 0

    def update_id(self, node_id):
        self.node_id = node_id

    def update_name(self, name):
        self.name = name

    def __str__(self):
        return str(self.node_id)

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.node_id < other.node_id
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Node):
            return self.node_id > other.node_id
        else:
            return NotImplemented


class Edge:
    def __init__(self, node1, node2, symbol):
        self.start_node = node1
        self.end_node = node2
        self.symbol = symbol


class Nfa:
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.nodes = set()
        self.edges = set()

    def add_edge(self, node1, node2, symbol):
        new_edge = Edge(node1, node2, symbol)
        self.edges.add(new_edge)
