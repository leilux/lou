#!/usr/bin/env python
#coding: utf-8

#构建价格模型 -- Building Price Models

# 大部分分类器非常适合于对未知数据的*所属分类*进行预测。但是，在利用多种不同属性（比如价格）对*数值型数据*进行预测时，贝叶斯分类器、决策树、及支持向量机都不是最佳算法。
# 本章将对一系列算法进行考查：这些算法接受训练，根据之前见过的样本数据作出数值类的预测，而且可以显示概率分布，以帮助用户对预测过程加以解释
# 介绍如何利用这些算法来构造价格预测模型。
# 进行数值型预测的一项关键工作是确定哪些变量是重要的。将利用第5章中介绍过的优化技术，自动确定各个变量的最佳权重。

##构造一个样本数据集 -- Building a Sample Dataset


##k-最近邻算法 -- k-Nearset Neighbors

###近邻数 -- Number of Neighbors

###定义相似度 -- Defining Similarity

###k-最近邻算法的代码 -- Code for k-Nearset Neighbors


##为近邻分配权重 -- Weighted Neighbors

###反函数 -- Inverse Function

###减法函数 -- Subtraction Function

###高斯函数 -- Gaussian Function

###加权kNN -- Weighted kNN


##交叉验证 -- Cross-Validation


##不同类型的变量 -- Heterogeneous Variables

###加入数据集 -- Adding to the Dataset

###按比例缩放 -- Scaling Dimensions


##对缩放结果进行优化 -- Optimizing the Scale

# 在有许多输入变量须要考查的情况下，利用第5章的优化算法自动寻找最优解。


##不对称分布 -- Uneven Distributions

###估计概率密度 -- Estimating the Probability Density

###绘制概率分布 -- Graphing the Probabilities


##使用真实数据eBay API -- Using Real Data--the eBay API

###获取开发者密钥 -- Getting a Developer Key

###建立连接 -- Setting Up a Connection

###执行搜索 -- Performing a Search

###获取商品明细 -- Getting Details for an Item

###构造价格预测程序 -- Building a Price Predictor


##何时使用k-最近邻算法 -- When to Use k-Nearset Neighbors

# 不足：
# 计算量大：需要计算针对每个点的距离
# 在一个包含有许多变量的数据集中，我们可能很难确定合理的权重值，也很难决定是否应该去除某些变量。

# 优势：
# 无需任何计算开销的前提下将新的观测数据加入到数据集中。因为算法是在使用其他观测数据的加权值来进行预测的。
# 一旦确定了最佳的权重值，就可以凭借这些信息更好地掌握数据集所具备的特征
# 当怀疑数据集中还有其他无法度量的变更时，还可以建立概率函数。

##Exercises
