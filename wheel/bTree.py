#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/26 17:52
# @Author  : ligang-s
# @File    : bTree.py

class Node:
    def __init__(self,data):
        self.value = data
        self.left_child = None
        self.right_child = None

    def pre_order(self):
        if self.value != None:
            print self.value
        if self.left_child:
            self.left_child.pre_order()
        if self.right_child:
            self.right_child.pre_order()

    def pre_order_new(self):
        node_list = []
        node = self
        node_list.append(node)
        while len(node_list) != 0:
            node = node_list.pop()
            if node.value != None:
                print node.value
            if node.right_child != None:
                node_list.append(node.right_child)
            if node.left_child != None:
                node_list.append(node.left_child)

    def mid_order(self):
        if self.left_child:
            self.left_child.mid_order()
        if self.value != None:
            print self.value
        if self.right_child:
            self.right_child.mid_order()

    def mid_order_new(self):
        node_list = []
        node = self
        # node_list.append(node)
        while len(node_list) != 0 or node:
            # node = node_list.pop()
            while node:
                node_list.append(node)
                node = node.left_child
            node = node_list.pop()
            print node.value
            node = node.right_child


    def midOrder(self):
        # if not self.root:
        #     return
        stackNode = []
        node = None
        node = self
        while stackNode or node:
            while node:
                stackNode.append(node)
                node = node.left_child
            node = stackNode.pop()
            print node.value
            node = node.right_child
        print len(stackNode)

    def last_order(self):
        if self.left_child:
            self.left_child.last_order()
        if self.right_child:
            self.right_child.last_order()
        if self.value != None:
            print self.value

    def last_order_new(self):
        node_list = []
        node = self
        while node_list or node:
            while node:
                node_list.append(node)
                node = node.left_child
            node = node_list.pop()
            print node.value
            node = node.right_child

class bTree:
    def __init__(self,data,lchild,rchild):
        self.value = data
        self.left_child = lchild
        self.right_child = rchild

    def add_node(self,node,leftchild,rightchild):
        if node:
            if leftchild:
                node.left_child = leftchild
            if rightchild:
                node.right_child = rightchild

def test():
    root = Node(10)
    last_node = Node(10)
    b_tree = bTree(10,None,None)
    node_list = []
    for i in range(10):
        node_list.append(Node(i))
    base_node = root
    base_node.left_child = node_list[0]
    base_node.right_child = node_list[1]
    base_node.left_child.left_child = node_list[2]
    base_node.left_child.right_child = node_list[3]
    base_node.right_child.left_child = node_list[4]
    base_node.right_child.right_child = node_list[5]
    base_node.left_child.left_child.left_child = node_list[6]
    base_node.left_child.left_child.right_child = node_list[7]
    base_node.right_child.left_child.left_child = node_list[8]
    base_node.right_child.left_child.right_child = node_list[9]
    base_node.left_child.right_child.right_child = last_node


    # print root.left_child.value
    print "##pre"
    root.pre_order()
    print "######"
    print "##mid"
    root.mid_order()
    print "######"
    print "##last"
    root.last_order()
    print "######"
    print "##pre_new"
    root.pre_order_new()
    print '#####'
    print '##mid_order'
    root.mid_order_new()

if __name__ == "__main__":
    test()







