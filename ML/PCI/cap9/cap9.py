#!/usr/bin/env python
#coding: utf-8

#高阶分类：核方法和SVM -- Advanced Classification：Kernel Methods and SVMs

# 介绍线性分类器和核方法的概念，并介绍一种最为高阶的分类器，同时也是目前仍然处于活跃状态的一个研究领域-支持向量机（SVMs）
# 本章中出现的数据集所涉及的几乎都是关于如何为约会网站的用户寻找配对。
# 选用这样的数据集来为大家示范前述几种分类器的缺陷，以及怎样对数据集进行调整才能更好地适应前述这些算法。
# 将一个复杂数据集扔给一个算法，然后希望它能学会如何进行精确的分类，这几乎是不可能的。
# 选择正确的算法，然后对数据进行适当地预处理，这是要获得满分的分类结果所必须的。
# 通过对本章中出现的数据集所做的调整，能为日后调整其他数据集提供有益的启示。
# 结尾处，学习到如何构造一个包含真实人员信息的数据集，用来预测具备某些性格特征的人们是否可能成为好朋友。


##婚介数据集 -- Matchmaker Dataset


##数据中的难点 -- Difficulties with the Data

###决策树分类器 -- Decision Tree Classifier


##基本的线性分类 -- Basic Linear Classification


##分类特性 -- Categorical Features

###是/否问题 -- Yes/No Questions

###兴趣列表 -- Lists of Interests

###利用Yahoo! Maps来确定距离 -- Determining Distances Using Yahoo! Maps

####获取Yahoo!的应用密钥 -- Getting a Yahoo! Apllication Key

####使用Geocoding API -- Using the Geocoding API

####计算距离 -- Calculating the Distance

###构造新的数据集 -- Creating the New Dataset


##对数据进行缩放处理 -- Scaling the Data


##理解核方法 -- Understanding Kernel Methods

###核技法 -- The Kernel Trick


##支持向量机 -- Support-Vector Machines

# 分界线附近的坐标点称为支持向量。寻找支持向量，并利用支持向量来寻找分界线的算法便是支持向量机


##使用LIBSVM -- Using LIBSVM

###获取LIBSVM -- Getting LIBSVM

# [LIBSVM -- A Library for Support Vector Machines](http://www.csie.ntu.edu.tw/~cjlin/libsvm/)
# [(lib)SVM 簡易入門](http://ntu.csie.org/~piaip/svm/svm_tutorial.html)
# [LibSVM分类的实用指南](http://blog.sina.com.cn/s/blog_72995dcc0100pflx.html)

###一个Python会话的例子 -- A Sample Session

###将SVM用于婚介数据集 -- Applying SVM to the Matchmaker Dataset


##基于Facebook的匹配 -- Matching on Facebook

###获得开发者密钥 -- Getting a Developer Key

###建立会话 -- Creating a Session

###下载好友数据 -- Download Friend Data

###构造匹配数据集 -- Building a Match Dataset

###构造SVM模型 -- Creating an SVM Model


##Exercises

# 2. **优化分界线** 我们是否可以利用第5章中学到的优化方法，而不是仅用求均值的方法来选择分界线呢？你会选用什么样的成本函数呢？
