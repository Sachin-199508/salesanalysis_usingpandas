#!/usr/bin/env python
# coding: utf-8

# *** US Sales Analysis***
# 

# #### Importing required libararies

# In[46]:


import pandas as pd
import os
import warnings
warnings.filterwarnings("always")
import matplotlib.pyplot as plt


# #### Merging 12 months of sales data

# In[47]:


df = pd.read_csv("./Desktop/Sales_Data/Sales_April_2019.csv")
files = [file for file in os.listdir('./Desktop/Sales_Data')]
all_months_data = pd.DataFrame()
for file in files:
    df = pd.read_csv("./Desktop/Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data,df])

all_months_data.to_csv("all_data.csv", index=False)


# In[48]:


all_data = pd.read_csv("all_data.csv")
all_data.head()


# ### Task2:Add Month Column

# Clean the data

# In[49]:


nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()

all_data = all_data.dropna(how='all')
all_data.head()


# In[50]:


all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
all_data.head()


# In[51]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# #### Task 3: Add a SALES Column

# In[52]:


all_data.dtypes


# Task 4: Add a city Column

# In[83]:


def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(" ")[1]


all_data['City'] = all_data['Purchase Address'].apply(lambda x: get_city(x)+"("+ get_state(x)+')')
#all_data = all_data.drop('column', axis =1)
#del all_data['Column']
all_data.head()


# In[84]:


all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

all_data.head()


# In[85]:


all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.head()


# #### Question 1 : What was the best month for sales? how much was earned that month?

# In[86]:


results=all_data.groupby('Month').sum()


# In[87]:


months = range(1,13)
plt.bar(months,results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()


# #### What city had the highest number of sales

# In[91]:


results=all_data.groupby('City').sum()
results


# In[96]:


cities =[ city for city , df in all_data.groupby('City')]

plt.bar(cities,results['Sales'])
plt.xticks(cities,rotation='vertical',size=8)
plt.ylabel('Sales in USD ($)')
plt.xlabel('City namer')
plt.show()


# #### Question 3: What time should we display advertisements to maximize likelihood of customer's buying product

# In[100]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])


# In[107]:


all_data['Hour']  = all_data['Order Date'].dt.hour
all_data['Minute']  = all_data['Order Date'].dt.minute
all_data['Count'] = 1
all_data.head()


# In[110]:


hours = [hour for hour, df in all_data.groupby('Hour')]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.grid()
plt.show()

# For advertisement recommendation is around 11am or 7pm


# #### Question 4: What products are most ofter sold together?

# In[113]:


df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ",".join(x))
df = df[['Order ID','Grouped']].drop_duplicates()
df.head()


# In[119]:


from itertools import combinations
from collections import Counter

count = Counter()
for row in df['Grouped']:
    row_list = row.split(",")
    count.update(Counter(combinations(row_list,2)))
    
for key, value in count.most_common(10):
    print(key,value)


# #### Question 4: What product sold the most? Why do you think it sold the most?

# In[124]:


product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']

products = [product for product, df in product_group]
plt.ylabel('Quantity Ordered')
plt.xlabel('Product')
plt.bar(products,quantity_ordered)
plt.xticks(products,rotation='vertical',size=8)
plt.show()


# In[131]:


prices = all_data.groupby('Product').mean()['Price Each']
fig , ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered)
ax2.plot(products, prices,'b-')


ax1.set_xlabel('product Name')
ax1.set_ylabel('Quantity Ordered',color='g')
ax2.set_ylabel('Price ($)',color='b')
ax1.set_xticklabels(products, rotation='vertical',size=8)

plt.show()


# In[ ]:





# In[134]:





# In[ ]:




