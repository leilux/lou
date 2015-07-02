#!/usr/bin/env python
#coding: utf-8

#寻找独立特征 -- Finding Independent Features

# 本章将研究如何在数据集并未明确标识结果的前提下，从中提取出重要的潜在特征来。
# 和聚类一样，这些方法的目的不是为了预测，而是要尝试对数据进行特征识别，并且告诉我们值得关注的重要信息。
# 聚类算法将数据集中的每一行数据分别分配给了层级结构中的某个组（group）或某个点（point）——每一项数据都精确对应于一个组，这个组代表了组内成员的平均水平。
# 特征提取：是以上思想的一般表现形式；
# 它会尝试从数据集中寻找新的数据行，将这些新找到的数据行加以组合，就可以重新构造出数据集。
# 和原始数据集不一样，位于新数据集中的每一行数据并不属于某个聚类，而是由若干特征的组合构造而成的。

# 寻找独立特征的必要性例子：
# 鸡尾酒宴会问题：在多人谈话时鉴别声音的问题
# 对重复出现于一组文档中的单词使用模式（word-usage patterns）进行识别，可以识别出，以不同组合形式独立出现于各个文档中的主题。
# 本章例子：
# 一个从不同订阅源下载新闻报道的系统，并从一组报道文章中识别出关键主题来。一篇文章可以包含不止一个主题，主题也可以用于不止一篇文章。
# 关于股票市场数据：将同样的算法用于股票数据，寻找数据背后的原因，以及它们各自对结果所构成的影响。

##搜集一组新闻 -- A Corpus of News

###选择新闻来源 -- Selecting Sources

###下载新闻来源 -- Downloading Sources

###转换成矩阵 -- Converting to a Matrix


##先前的方法 -- Previous Approaches

###贝叶斯分类 -- Bayesian Classification

###聚类 -- Clustering


##非负矩阵因式分解 -- Non-Negative Maxtrix Factorization

###矩阵数学简介 -- A Quick Introduction to Matrix Math

###这与文章矩阵有何关系？ -- What Does This Have to Do with the Articles Matrix?

###使用Numpy -- Using Numpy

###算法实现 -- The Algorithm


##结果呈现 -- Displaying the Results

###以文章的形式呈现 -- Displaying by Article


##利用股票市场的数据 -- Using Stock Market Data

###什么是成交量 -- What Is Trading Volume?

###从Yahoo! Finance下载数据 -- Downloading Data from Yahoo! Finance

###准备矩阵 -- Preparing a Matrix

###运行NMF -- Running NMF

###结果呈现 -- Displaying the Results


##Exercises
