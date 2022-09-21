#!/usr/bin/env python
# coding: utf-8

# In[24]:


import pandas as pd
import numpy as np
# from google.colab import drive
# drive.mount("/content/gdrive")
dataframe=pd.read_csv('DataSet.csv')
dataframe=dataframe.drop(['Opponents', 'Damage','Fuel','Focus','Track','Focus2','WheelSpinVel'], axis = 1)


# In[49]:


dataframe

X = dataframe.iloc[:,4:].values
y = dataframe.iloc[:,3:4].values
y


# In[50]:


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)


# In[51]:


# Feature Scaling
from sklearn.preprocessing import StandardScaler

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


# In[52]:


from sklearn.ensemble import RandomForestRegressor

regressor = RandomForestRegressor(n_estimators=20, random_state=0)
regressor.fit(X_train, y_train.ravel())
y_pred = regressor.predict(X_test)


# In[53]:


from sklearn import metrics

print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))


# In[54]:


import piskle
piskle.dump(regressor, 'Steer.pskl')


# In[ ]:




