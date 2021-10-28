# -*- coding: utf-8 -*-
"""Big mart sale prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1csVjkE_1ziZ6wupxcd5toSFV7Ur30TA8

##BIG MART SALES PREDICTION

##About Big Mart

Big Mart Retail Corporation is one of the fastest growing express home delivery food and Grocery Retail Store company covering worldwide which is incorporated in the year 2016 In India.                        
     In the years of 2009 big mart started its operation through its first COCO retail store on small size 100 sft. to 300 sft. area. big mart is giving door step delivery to its customer through our retail stores

##Aim of the project

The data scientists at BigMart have collected 2013 sales data for 1559 products across 10 stores in different cities. Also, certain attributes of each product and store have been defined. The aim is to build a predictive model and find out the sales of each product at a particular store.

  Using this model, BigMart will try to understand the properties of products and stores which play a key role in increasing sales.

##About the Dataset

The dataset has 8524 records with 13 columns. The details of each column is given below

    Item_Identifier : Unique product ID
    Item_Weight : Weight of product
    Item_Fat_Content : Whether the product is low fat or not
    Item_Visibility : % of total display area in store allocated to this product
    Item_Type : Category to which product belongs
    Item_MRP : Maximum Retail Price (list price) of product
    Outlet_Identifier : Unique store ID
    Outlet_Establishment_Year : Year in which store was established
    Outlet_Size : Size of the store
    Outlet_Location_Type : Type of city in which store is located
    Outlet_Type : Grocery store or some sort of supermarket
    Item_Outlet_Sales : Sales of product in particular store. This is the outcome variable to be predicted.

##Importing required libraries
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

"""##Importing Dataset"""

df=pd.read_csv('train_set1.csv')

df.shape

df.head()

df.describe()

df.info()

df.columns

"""##Cleaning Data"""

df.isnull().sum()

"""##Removing NULL values from all the columns"""

df['Item_Weight']=df['Item_Weight'].fillna(df['Item_Weight'].mean())

df['Outlet_Size']=df['Outlet_Size'].fillna('Medium')

"""##Exploratory Data Analysis

##Univariate Analysis
"""

sns.distplot(df['Item_Outlet_Sales'])

"""We can see that the Outlet_sales is normally distributed with right skewness."""

sns.boxplot(df['Item_Weight'])

"""Most of the items have weight in range of 8-16. 
The mode of weight is near to 13.
"""

sns.countplot(x='Outlet_Size',data=df)

sns.countplot(df['Outlet_Location_Type'])

"""1.   Most of the Outlet are located in Tier 3.
2.   Tier 2 location is second most after Tier 3.


"""

sns.countplot(df['Outlet_Type'])

"""1.   Most Outlets are Supermarkets of type 1
2.   There is Significant amount of Outlets which are Grocery store.

##Bi-variate Analyis
"""

sns.regplot(x='Item_Weight',y='Item_Outlet_Sales',data=df)

"""The plot show that outlet sales has less co-relation with item weight."""

plt.figure(figsize=(10,10))
sns.boxplot(x='Outlet_Identifier',y='Item_Outlet_Sales',data=df)

"""

1.   OUT027 has maximum outlet sales.
2.   OUT049 and OUT019 have least outlet sales among all.

"""

sns.regplot(x='Item_Visibility',y='Item_Outlet_Sales',data=df)

"""

1.   There is significant co-relation between Item_visibility and outlet sales.
2.   The visbility range 0.00-0.20 has maximum outlet sales.

"""

plt.figure(figsize=(10,10))
sns.boxplot(x='Outlet_Size',y='Item_Outlet_Sales',data=df)

"""The plot shows the relation of Outlet size with outlet sales."""

plt.figure(figsize=(10,6))
ax = sns.countplot('Item_Type', data = df)
plt.xlabel('Item Type')
plt.ylabel('Count')
plt.title('Number of Items')

X = plt.gca().xaxis
for item in X.get_ticklabels():
  item.set_rotation(90)
plt.show()

df.corr()

plt.figure(figsize=(10,5))
sns.heatmap(df.corr(),annot=True)
plt.show()

sns.regplot(x='Item_MRP',y='Item_Outlet_Sales',data=df)

"""

1.   The plot shows that more the price of item, the better is its outlet sale.
2.   The relation is almost linear.

"""

plt.figure(figsize=(10,10))
sns.factorplot(x='Outlet_Type',y='Item_Outlet_Sales',hue='Outlet_Size',data=df)

sns.pairplot(df)

"""The above plot shows all pair of relationship between all attributes

##Feature Engineeering

##Converting categorical data into numerical
"""

df['Item_Fat_Content'].unique()

def fun(x):
  if x=='Low Fat' or x=='LF' or x=='low fat':
    return(0)
  else:
    return(1)

df['Item_Fat_Content']=df['Item_Fat_Content'].apply(fun)

df['Item_Fat_Content'].head()

df['Item_Type'].unique()

df['Outlet_Size'].unique()

def fun1(x):
  if x=='Medium':
    return(0)
  elif x=='High':
    return(1)
  else:
    return(2)

df['Outlet_Size']=df['Outlet_Size'].apply(fun1)

df['Outlet_Size'].head()

df['Outlet_Location_Type'].unique()

def fun2(x):
  if x=='Tier 1':
    return(0)
  elif x=='Tier 2':
    return(1)
  else:
    return(2)

df['Outlet_Location_Type']=df['Outlet_Location_Type'].apply(fun2)

df['Outlet_Location_Type'].head()

df['Outlet_Type'].unique()

def fun3(x):
  if x=='Supermarket Type1':
    return(0)
  elif x=='Supermarket Type2':
    return(1)
  elif x=='Supermarket Type3':
    return(2)
  else:
    return(3)

df['Outlet_Type']=df['Outlet_Type'].apply(fun3)

df['Outlet_Type'].head()

df['Outlet_Identifier'].unique()

df1=pd.get_dummies(df['Outlet_Identifier'])

df=pd.concat([df,df1],axis=1)

df.columns

df.head()

"""##Feature selection

From the co-relation map we plotted before, we can see that there almost no co-relation between 'Item_Identifier', 'Item_type' and 'Outlet_Establishment_year' with our target i.e 'Item_Outlet_sales'

So we will drop these columns and will not use in training out model.

##Assigning data to X and Y variable
"""

x=df.drop(['Item_Identifier','Outlet_Identifier','Outlet_Establishment_Year','Item_Outlet_Sales','Item_Type'],axis=1)
y=df['Item_Outlet_Sales']

x.head()

y.head()

"""##Training Testing and splitting"""

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,mean_absolute_error,accuracy_score,classification_report,confusion_matrix

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)

"""##Linear Regression Model"""

from sklearn.linear_model import LinearRegression

lrm=LinearRegression()

lrm.fit(x_train,y_train)

predicted=lrm.predict(x_test)

"""##Evaluation of Linear Regression model"""

print("MEAN SQUARED ERROR(MSE)",mean_squared_error(y_test,predicted))
print("MEAN ABSOLUTE ERROR(MAE)",mean_absolute_error(y_test,predicted))
print("ROOT MEAN SQUARED ERROR(RMSE)",np.sqrt(mean_squared_error(y_test,predicted)))
print("SCORE",lrm.score(x_test,y_test))

"""##Random Forest Regressor"""

from sklearn.ensemble import RandomForestRegressor

rfg=RandomForestRegressor()

rfg.fit(x_train,y_train)

predicted=rfg.predict(x_test)

"""##Evaluation of Random Forest Regression model"""

print("MEAN SQUARED ERROR(MSE)",mean_squared_error(y_test,predicted))
print("MEAN ABSOLUTE ERROR(MAE)",mean_absolute_error(y_test,predicted))
print("ROOT MEAN SQUARED ERROR(RMSE)",np.sqrt(mean_squared_error(y_test,predicted)))
print("SCORE",rfg.score(x_test,y_test))

"""##Ada Boost Regression"""

from sklearn.ensemble import AdaBoostRegressor

abr=AdaBoostRegressor(n_estimators=70)

abr.fit(x_train,y_train)

predicted=abr.predict(x_test)

"""##Evaluation of AdaBoost Regressor"""

print("MEAN SQUARED ERROR(MSE)",mean_squared_error(y_test,predicted))
print("MEAN ABSOLUTE ERROR(MAE)",mean_absolute_error(y_test,predicted))
print("ROOT MEAN SQUARED ERROR(RMSE)",np.sqrt(mean_squared_error(y_test,predicted)))
print("SCORE",abr.score(x_test,y_test))

"""##Bagging Regressor"""

from sklearn.ensemble import BaggingRegressor

br=BaggingRegressor(n_estimators=30)

br.fit(x_train,y_train)

predicted=br.predict(x_test)

"""##Evaluation of Bagging Regressor"""

print("MEAN SQUARED ERROR(MSE)",mean_squared_error(y_test,predicted))
print("MEAN ABSOLUTE ERROR(MAE)",mean_absolute_error(y_test,predicted))
print("ROOT MEAN SQUARED ERROR(RMSE)",np.sqrt(mean_squared_error(y_test,predicted)))
print("SCORE",br.score(x_test,y_test))

"""##Comparing all Models and finding the best one.

1.   Linear Regression  score: 0.56
2.   Random Forest Regression  Score: 0.52
1.   AdaBoost Regression Score: 0.50
2.   Bagging Regressor  Score 0.55

We can see that Linear Regression model gave us the best score for our testing data. Therefore Linear Regression is best from all the above models.

##Summary

Firstly we studied about the dataset i.e Big Mart Sales Analysis and understood the meaning of each columns. Then we performed Exploratory Data Analysis on our dataset. We plotted various Univariate and Bi-variate plots to study the relationship between various features. Then we cleaned our data and also performed feature enginnering.                                                                                              
We trained our model and predicted values for Outlet_sales. Evaluation was done to find out the best model.

##Conclusion

From all the models that we used, we found out that Linear Regression model gave us the best score i.e 0.56. We therefore end our analysis here and conclude Linear regression as our predictive  model.
"""