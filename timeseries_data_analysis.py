'''
author: revanth
time: 4th Oct 2022, 6:30 PM UTC+4:00
'''


import pandas as pd

pd.set_option('display.max_columns', None)
#pd.set_option('display.max_colwidth', None)


df = pd.read_csv('interview_df.csv')

print('number of columns : {}, rows : {}'.format(df.shape[1], df.shape[0]))

print(df.dtypes)

print(df.sample(n=5))

df = df[df['customer_id'].isin(['1e9e771c897ae8f0a41a38d66a2e3997','662bd756ac4e10b997a37708682fc7f0','8dc33e67a371270daee5e52d4f4701f7','b2eb3486d85edd6a5455f5f20dbb7fee','d8c14d75899aeafabf11a3ca8f2ea62f'])]
df = df.sort_values('customer_id')

print(df)
df = df.sort_index()
print(df)
df['orders_on_customer_id_7D'] = df.groupby('customer_id',group_keys=False).order_id.apply(lambda x: x.rolling('7D', closed='left').count()).fillna('0').astype('int')
print(df['orders_on_customer_id_7D'])
df['customer_id_has_paid'] = df.groupby('customer_id', group_keys=False).order_status.apply(lambda x: x.shift()) == 'paid'
print(df['customer_id_has_paid'])
df.reset_index().to_csv('abc.csv', index = False)
#df = df.sort_index()
#df['shop_id_count_paid_orders_90D'] = df.groupby("shop_id").rolling('90D', closed= "left")["order_status"].apply(lambda x: x.eq('paid').count())

df["shop_id_count_paid_orders_90D"] = df.groupby("shop_id", group_keys=False).order_status.apply(lambda x: x.eq('paid').cumsum()) #yet to add 90d rolling window
print(df)

