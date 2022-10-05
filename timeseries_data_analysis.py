'''
author: revanth
email:  revanthm93@gmail.com
date:   5th Oct 2022, 10:30 AM UTC+4:00
'''

import os  # standard library
import sys
import pandas as pd  # 3rd party packages

pd.set_option('display.max_columns', None)  # To view all columns in dataframe in terminal without shrinking

'''Since we are playing around the time series data, loaded the csv (interview_df.csv) as dataframe
and defined  'created_date' column as index column also explicitly mentioned
'created_date' column to be parsed as datetime field'''
df = pd.read_csv('interview_df.csv', index_col='created_date', parse_dates=['created_date'])
df = df.sort_index()  # sort df based on index

# Data Exploration
print('number of columns : {}, rows : {}' \
      .format(df.shape[1], df.shape[0]))  # returns the no.of columns (excluding index_column) & rows
print(df.dtypes)  # returns datatype of each column in df
print(df.sample(n=5))  # returns randomly sampled 5 records

# Starting with generating new columns

'''orders_on_customer_id_7D: Number of orders on customer_id in the last 7 days
This can be achieved by grouping df by column customer_id and then perform a the rolling operation on every individual group.
group by: to group records based on the customer_id
rolling: to count the number of orders in the last 7 days for each transaction for every customer.
'7D': to roll window for 7 days
'closed=left' : to exclude the current row value in the rolling window.
'group_keys=False'  : to eliminate the additional index column
'fillna('0')' : to fill the null values with '0' in the result.
'astype('int'): to convert float to integer.
'''
df['orders_on_customer_id_7D'] = df.groupby('customer_id', group_keys=False).order_id.apply(
    lambda x: x.rolling('7D', closed='left').count()).fillna('0').astype('int')
print(df['orders_on_customer_id_7D'])

'''customer_id_has_paid: True if the customer has paid prior to the order, False otherwise.
This can be achieved by grouping df by column customer_id and 
then using shift() method to get the difference between consecutive rows.
finally verifying if the value is paid, which returns a boolean True if paid, False otherwise.
shift() : to find the difference between consecutive rows.
'''

df['customer_id_has_paid'] = df.groupby('customer_id', group_keys=False).order_status.apply(
    lambda x: x.shift()) == 'paid'
print(df['customer_id_has_paid'])

'''shop_id_count_paid_orders_90D: Number of paid orders on shop_id in the last 90 days.
'90D': to roll window for 90 days
'eq': to check if the order_status is 'paid'
'''

df["shop_id_count_paid_orders_90D"] = df.assign(new=df["order_status"].eq('paid')).groupby(
    "shop_id").order_status.apply(lambda x: x.rolling('90D', closed='left').count()).fillna('0').astype('int')
print(df['shop_id_count_paid_orders_90D'])

df.to_csv('result_df.csv') #writing df with 3 new addional columns as result_df.csv
