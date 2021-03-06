# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 19:07:26 2019

@author: Parth
"""

'''
Multiple Linear Regression.

--->In Simple Linear Regression, we had just one independent variable. Based on the value 
    of that variable, we would predict the value of the dependent variable. 
    
--->But the real world scenarios are so complex that is it quite impossible to predict a 
    continuous value based on just one single feature. So when we try to predict a continuous value
    based on a set of multiple features given as inputs, that regression is called as Multiple 
    Linear Regression. 
    
--->Multiple Linear Regression's equation is of the form y=B0+B1X1+B2X2+B3X3+BnXn
    Where, 
    X1,X2 are the input features. 
    
--->In Multiple Linear Regression, we should make sure that the features are correlated with 
    the dependent variabele and not with each other i.e Multicollinearity must not exist. 
    
--->Concept of Dummy variables:
    In our dataset, we might be having some features that contain categorical data.
    Eg: Male/Female, Yes/No or even names of cities like California/Mumbai/Goa/Delhi, etc. 
    The problem with these kind of variables is, we can't pass the textual data directly as an input to 
    the classifier, we must quantify it in terms of numerical data first.
    The way dummy variables work is can be explained with an example below: 
    |City|           |Goa|Pune|Delhi|  
    ________ --->    ________________
    |Goa   |         | 1 |  0 | 0  |
    |Pune  |         | 0 |  1 | 0  | 
    |Delhi |         | 0 |  0 | 1  |
    
--->Avoiding the Dummy Variable Trap:
    If there are n categorical variables, we must include n-1 dummy variables in our features. 
    
    
--->Determining which features to be used: 
    In Multiple linear regression, we have multiple features. We need to find out which features are highly 
    correlated with the output variable. 
    For this, we determine the P-value of the features and set a significance level. 
    If the P-value is greater than the Significance level, we discard the feature. 
    If the P-value is smaller than the significance level, it indicates that the feature is strongly 
    correlated with the output variable. Hence, we include(keep/don't discard) the feature.
'''
from sklearn.metrics import accuracy_score
from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer 
import pandas as pd

df1=pd.read_csv('50_startups.csv')
df2=pd.get_dummies(df1['State'])


result = pd.concat([df1,df2],axis=1)
df=result.drop(['State'],axis=1)

y=df.iloc[:,3].values
df0=df.drop(['Profit'],axis=1)


X=df0.iloc[:,:].values



X_train, X_test, y_train, y_test= train_test_split(X,y,test_size=0.2)



# =============================================================================
# I have commented the feature scaling code and haven't executed it because in Linear 
# Regression models the feature scaling is done implicitly by the library. But in some uncommon 
# Regression models like SVR, etc. we need to explicitly scale the features as
# the features aren't implicitly scaled by the library. 
# =============================================================================


'''
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)
sc_y = StandardScaler()
y_train = sc_y.fit_transform(y_train)
'''

cl=LinearRegression()
cl.fit(X_train,y_train)

y_pred=cl.predict(X_test)

#calculating the r2 error manually
ssr=0
sst=0
for i in range(len(y_test)):
    ssr+=(y_test[i]-y_pred[i])**2
    sst+=(y_test[i]-mean(y_test))**2

r2=1-(ssr/sst)


print("R-Squared error is: ",r2_score(y_test,y_pred))

'''
In the code below, I will only use the features that are heavily correlated with the
output variable. 
'''
#Determining the P-value and performing backward elimination. 
import statsmodels.api as sm
'''
In the equation of Linear regression: y= B0+B1X1+B2X2+BnXn, the sklearn library assume B0 as 
B0X0 but the statsmodels library doesn't make this assumption implicitly. 
So we need to assign the value of 1 to X0 i.e we need to append a column of 1's. 
'''
X=X[:,1:]
X=np.append(arr=np.ones((50,1)),values=X,axis=1)
#Backward elimination starts here.
X_opt=X
regressor=sm.OLS(endog=y,exog=X_opt).fit()
regressor.summary()
X_opt=X[:,[0,1,3,4,5]]
regressor=sm.OLS(endog=y,exog=X_opt).fit()
regressor.summary()

X_opt=X[:,[0,3,4]]
regressor=sm.OLS(endog=y,exog=X_opt).fit()
regressor.summary()

X_opt=X[:,[0,3]]
regressor=sm.OLS(endog=y,exog=X_opt).fit()
regressor.summary()

x1=X_opt[:,1:]

X_train, X_test, y_train, y_test= train_test_split(x1,y,test_size=0.2)

cl=LinearRegression()
cl.fit(X_train,y_train)

y_pred=cl.predict(X_test)

#We can observe the increase in r2 value, thus the model performs better when only useful features are supplied
print("R-Squared error is: ",r2_score(y_test,y_pred))

