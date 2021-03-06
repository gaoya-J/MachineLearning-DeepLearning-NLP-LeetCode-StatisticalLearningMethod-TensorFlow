# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 11:17:33 2019

@author: Gift
"""

# Load libraries
import pandas
from pandas.tools.plotting import scatter_matrix #导入散点图矩阵包
import matplotlib.pyplot as plt  
from sklearn import model_selection  #模型比较和选择包
from sklearn.metrics import classification_report  #将主要分类指标以文本输出
from sklearn.metrics import confusion_matrix #计算混淆矩阵，主要来评估分类的准确性
from sklearn.metrics import accuracy_score #计算精度得分
from sklearn.linear_model import LogisticRegression #线性模型中的逻辑回归
from sklearn.tree import DecisionTreeClassifier #树算法中的决策树分类包
from sklearn.neighbors import KNeighborsClassifier #导入最近邻算法中的KNN最近邻分类包
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis #判别分析算法中的线性判别分析包
from sklearn.naive_bayes import GaussianNB #朴素贝叶斯中的高斯朴素贝叶斯包
from sklearn.svm import SVC  #支持向量机算法中的支持向量分类包
from sklearn import datasets
# Load dataset

# Load dataset
data = "iris.data"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(data, names=names) #读取csv数据

# shape
print(dataset.shape)

# head
print(dataset.head(20))

print(dataset.describe())

# class distribution
print(dataset.groupby('class').size())

# histograms
dataset.hist()
plt.show()

# Split-out validation dataset
array = dataset.values #将数据库转换成数组形式
X = array[:,0:4] #取前四列，即属性数值
Y = array[:,4] #取最后一列，种类
validation_size = 0.30 #验证集规模
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed) #分割数据集

# Test options and evaluation metric
seed = 7
scoring = 'accuracy'

# Spot Check Algorithms
models = [] #建立列表
models.append(('LR', LogisticRegression())) #往maodels添加元组（算法名称，算法函数）
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
# evaluate each model in turn
results = []
names = []
for name, model in models: #将算法名称与函数分别读取
	kfold = model_selection.KFold(n_splits=10, random_state=seed) #建立10倍交叉验证
	cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring) #每一个算法模型作为其中的参数，计算每一模型的精度得分
	results.append(cv_results)
	names.append(name)
	msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std()) 
	print(msg) 
    

# Compare Algorithms
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

# Make predictions on validation dataset
knn = KNeighborsClassifier()
knn.fit(X_train, Y_train) #knn拟合序列集
predictions = knn.predict(X_validation) #预测验证集
print(accuracy_score(Y_validation, predictions)) #验证集精度得分
print(confusion_matrix(Y_validation, predictions)) #混淆矩阵
print(classification_report(Y_validation, predictions)) #分类预测报告



















