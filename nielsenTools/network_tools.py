#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================
#       Set-up
# ====================

# Import required modules
from nielsenTools.isbn_tools import *

__author__ = 'Victoria Morris'
__license__ = 'MIT License'
__version__ = '1.0.0'
__status__ = '4 - Beta Development'


# ====================
#       Classes
# ====================


class Graph:

    def __init__(self, skip_check=False):
        self.nodes = set()
        self.adjacencies = {}
        self.formats = {}
        self.checked = {}
        self.skip_check = skip_check

    def __contains__(self, node):
        return node in self.nodes

    def __iter__(self):
        return iter(self.nodes)

    def add_node(self, node, format='U'):

        if node not in self.nodes:
            self.nodes.add(node)
            self.adjacencies[node] = set()
            self.formats[node] = format
            self.checked[node] = True if self.formats[node] == 'C' else False
            return
        if format == 'C':
            self.formats[node] = 'C'
            self.checked[node] = True
            return
        if self.checked[node]: return
        if format == 'U': return
        if self.formats[node] == format: return
        if self.formats[node] == 'U' and format in ISBN_FORMATS:
            self.formats[node] = format
            return
        if self.formats[node] == 'C':
            self.checked[node] = True
            return
        if node.startswith(('978311', '9783484')):
            self.formats[node] = 'P'
            self.checked[node] = True
            return
        if 'E' in [self.formats[node], format] and 'P' in [self.formats[node], format]:
            print('\nTrying Google ...')
            try: e = query(node)
            except: pass
            else:
                print('Resoved format of {} using Google Books'.format(node))
                if e:
                    self.formats[node] = 'P'
                    self.checked[node] = False
                    return
                else:
                    self.formats[node] = 'E'
                    self.checked[node] = False
                    return
        if self.skip_check:
            self.formats[node] = 'U'
            self.checked[node] = False
            return
        f = None
        while f not in ISBN_FORMATS:
            pyperclip.copy(node)
            f = input('Please enter the format of ISBN {} '
                      '(current formats are {}, {}): '.format(node, self.formats[node], format)).upper()
            self.formats[node] = f
            self.checked[node] = True
        return
    
    def add_nodes(self, nodes):        
        for n in nodes:
            node, format = n
            self.add_node(node, format)

    def remove_node(self, node):
        self.nodes.discard(node)
        self.adjacencies.pop(node, None)
        self.formats.pop(node, None)
        self.checked.pop(node, None)
        for n in self.adjacencies:
            self.adjacencies[n].discard(node)

    def remove_nodes(self, nodes):
        for n in nodes:
            self.remove_node(n)

    def collective_isbn(self, node):
        self.formats[node] = 'C'
        self.adjacencies[node] = set()
        for n in self.adjacencies:
            self.adjacencies[n].discard(node)

    def collective_isbns(self, nodes):
        for n in nodes:
            self.collective_isbn(n)
            
    def add_edge(self, u, v):
        if u in self and v in self and u != v:
            if self.formats[u] != 'C' and self.formats[v] != 'C':
                self.adjacencies[u].add(v)
                self.adjacencies[v].add(u)
            
    def add_edges(self, edges):        
        for e in edges:
            u, v = e
            self.add_edge(u, v)

    def check_graph(self):
        print('\nChecking graph ...')
        collective = [n for n in self.nodes if self.formats[n] == 'C' and len(self.adjacencies[n]) > 0]
        for n in collective:
            self.adjacencies[n] = set()
            neighours = [a for a in self.nodes if n in self.adjacencies[a]]
            for a in neighours:
                self.adjacencies[a].discard(n)

    def write_graph(self, path):
        self.check_graph()
        for f in ISBN_FORMATS:
            file = open(path.replace('.graph', '_{}.txt'.format(f)), 'w', encoding='utf-8', errors='replace')
            for node in sorted(self.formats):
                if self.formats[node] == f:
                    file.write(node + '\n')
            file.close()

        file = open(path.replace('.graph', '_groups.txt'), 'w', encoding='utf-8', errors='replace')
        for connected_component in sorted(self.connected_components(), key=len, reverse=True):
            file.write(' '.join(s + '|' + self.formats[s] for s in sorted(connected_component)) + '\n')
        for n in sorted(self.isolates()):
            file.write(n + '|' + self.formats[n] + '\n')
        file.close()

        file = open(path, 'w', encoding='utf-8', errors='replace')
        for node in sorted(self.nodes):
            file.write('{}\t{}\t{}\t{}\n'.format(node, self.formats[node], str(self.checked[node]), ';'.join(sorted(self.adjacencies[node]))))
        file.close()

    def connected_components(self):
        seen = set()
        for v in self:
            if v not in seen:
                c = set(self._plain_bfs(v))
                yield c
                seen.update(c)

    def node_connected_component(self, n):
        return set(self._plain_bfs(n))

    def _plain_bfs(self, source):
        seen = set()
        nextlevel = {source}
        while nextlevel:
            thislevel = nextlevel
            nextlevel = set()
            for v in thislevel:
                if v not in seen:
                    yield v
                    seen.add(v)
                    nextlevel.update(self.adjacencies[v])

    def isolates(self):
        return [n for n in self if len(self.adjacencies[n]) == 0]
