#!/usr/bin/env python
#coding: utf-8

#智能进化 -- Evolving Intelligence

# 构造的是一个能构造算法的算法：
# 本章将考查一种截然不同的问题解决方法。与先前遇到一个问题就选择一种算法的思路不同，我们将编写一个程序，尝试自动构造出解决某一问题的最佳程序来。
# 采用**遗传编程**（genetic programming）实现

# 本章涉及两个问题：
# 根据给定的数据集重新构造一个教学函数。
# 在一个简单的棋类游戏中自动生成一个AI玩家。

# 计算能力（computational power）才是真正制约遗传编程问题解决能力的唯一因素。


##什么是遗传编程 -- What is Genetic Programming?

###遗传编程与遗传算法 -- Genetic Programming Versus Genetic Algorithms


##将程序以树行的方式表示 -- Programs As Trees

###在Python中表现树 -- Representing Trees in Python

###树的构造和评估 -- Building and Evaluating Trees

def exampletree():
    '''
    lisp code: (if (gtw p0 3) (addw p1 5) (subw p1 2))
    '''
    return node(ifw, [
        node(gtw, [paramnode(0), constnode(3)]),
        node(addw, [paramnode(1), constnode(5)]),
        node(subw, [paramnode(1), constnode(2)]),
    ])

###程序的展现 -- Displaying the Program


##构造初始种群 -- Creating the Initial Population


##测试题解 -- Testing a Solution

###一个简单的数学测试 -- A Simple Mathematical Test

###衡量程序的好坏 -- Measuring Success


##对程序进行变异 -- Mutating Programs


##Crossover


##构筑环境 -- Building the Environment

# 可以用来拟合曲线

###多样性的重要价值 -- The Importance of Diversity


##一个简单的游戏 -- A Simple Game

###循环赛 -- A Round-Robin Tournament

###真人对抗 -- Playing Against Real People


##更多可能性 -- Further Possibilities

###更多数值型函数 -- More Numerical Functions

###记忆力 -- Memory

###不同数据类型 -- Different Datatypes


##Exercises
