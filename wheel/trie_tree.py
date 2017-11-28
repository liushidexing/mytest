#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/23 17:57
# @Author  : ligang-s
# @File    : trie_tree.py


import sys

class Node:
    def __init__(self):
        # self.value = None
        self.children = {}
        self.times = 0

class Trie_tree:
    def __init__(self):
        self.root = Node()

    def insert(self,content):
        node = self.root
        # tmp_content = ""
        new_flag = 0
        for key in content:
            if key not in node.children:
                node.children[key] = Node()
                # tmp_content += key
                node = node.children[key]
                # node.value = tmp_content
                new_flag = 1
            else:
                node = node.children[key]
                # tmp_content += key
                # node.value = tmp_content
        node.times += 1
        if new_flag == 1:
            self.root.times += 1

    def search(self,content):
        output_result = ''
        node = self.root
        for key in content:
            if key not in node.children:
                return None
            else:
                output_result += key
                node = node.children[key]
        if node.times == 0:
            return None
        else:
            return output_result,node.times

    def delete(self,content):
        node = self.root
        for key in content[:-1]:
            if key not in node.children:
                return 0
            else:
                node = node.children[key]

        ##delete the node by the judgement of last key of content
        if content[-1] not in node.children:
            return 0
        elif len(node.children[content[-1]].children) != 0:
            if node.children[content[-1]].times != 0:
                node.children[content[-1]].times = 0
                self.root.times -= 1
                return 1
            else:
                return 0
        elif len(node.children[content[-1]].children) == 0:
            node.children.pop(content[-1])
            self.root.times -= 1
            return 1

    def display_node(self,node):
        output_result = ''
        if len(node.children) == 0:
            print node.value
        else:
            if node.times != 0:
                print node.value
            for key in node.children.keys():
                self.display_node(node.children[key])

    def display(self,node,value):
        if len(node.children) == 0:
            pass
        else:
            for key in node.children.iterkeys():
                if node.children[key].times != 0:
                    print value + key
                self.display(node.children[key],value+key)

def test():
    trie = Trie_tree()
    trie.insert("qihoo")
    trie.insert("lenovo")
    trie.insert("qiguai")
    trie.display(trie.root,"\t")

    sys.exit(0)
    print
    print '###test###'
    print trie.search("qiq")
    print trie.search('qihoo')
    print trie.root.children.keys()

    print
    print '###output all###'
    # trie.display_node(trie.root)
    trie.display(trie.root, '')
    print trie.root.times
    trie.insert('qihoo')
    print trie.insert('qihooa')
    print trie.search('qi')
    trie.display(trie.root, '')
    print trie.root.times
    print trie.delete('qi')
    print trie.search('qihoo')
    print trie.delete('qihoo')
    print trie.search('qihooa')
    print trie.search('qihoo')


if __name__ == "__main__":
    test()