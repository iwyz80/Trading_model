import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from indicators import *

pd.options.display.max_rows=1220
pd.options.display.max_columns=30
#Read the csv
fileUrl = './input_data/XAUUSD_1Hour.csv'
date_parser = lambda gmtDate: dt.datetime.strptime(gmtDate, '%d.%m.%Y %H:%M:%S.%f')
instr_df = pd.read_csv(fileUrl, parse_dates = ['Gmt time'],index_col = 0, date_parser=date_parser, dayfirst=True, usecols=['Gmt time','Open','High', 'Low', 'Close'])
equilData = feature_create(instr_df)

#Create additional features

#Normalizing the High, close, open, low prices vs the equilprice
equilData['HCe'] =np.where(((equilData['High']>equilData['equilPrice'])& (equilData['Close']>equilData['equilPrice'])), 1, 0)
equilData['OLe'] =np.where(((equilData['Open']>equilData['equilPrice'])& (equilData['Low']>equilData['equilPrice'])), 1, 0)


#compute the 75th and 25th quantile of the RSIs
rsiQuantile = np.quantile(equilData[['RSI_H_14', 'RSI_C_14', 'RSI_H_21','RSI_C_21']],[0.25, 0.75])

#Comparing the mean RSI value and the quantile to create a new feature
equilData['rvq'] =0
equilData.loc[equilData[['RSI_H_14', 'RSI_C_14', 'RSI_H_21','RSI_C_21']].mean(axis=1)>=max(rsiQuantile), 'rvq']=1
equilData.loc[equilData[['RSI_H_14', 'RSI_C_14', 'RSI_H_21','RSI_C_21']].mean(axis=1)<=min(rsiQuantile), 'rvq']=-1

#Compute the 75th and 25th quantile of the WilliamsR
willrQuantile =np.quantile( equilData[['WILLR_14', 'WILLR_21']], [0.25, 0.75])

#Compare the mean WilliamR and the quantile to create a new feature
equilData['wvq'] = 0
equilData.loc[equilData[['WILLR_14', 'WILLR_21']].mean(axis=1)<=min(willrQuantile), 'wvq']=-1
equilData.loc[equilData[['WILLR_14', 'WILLR_21']].mean(axis=1)>=max(willrQuantile), 'wvq']=1

#Compute the change in the equilPrice
equilData['eq_d']=equilData['equilPrice'].diff()

#1. Percentage change

equilData['EH_Pct'] =round( (equilData['equilPrice']-equilData['High'])/equilData['equilPrice'],3)
equilData['EC_Pct'] =round( (equilData['equilPrice']-equilData['Close'])/equilData['equilPrice'], 3)
#2. Difference

# Resample data to daily price for plotting

instr_df_DayHigh = instr_df['High'].resample('D').max()
instr_df_DayLow = instr_df['Low'].resample('D').min()
instr_df_DayClose = (instr_df['Close'].loc[instr_df.index.hour ==23])
instr_df_DayOpen = (instr_df['Open'].loc[instr_df.index.hour ==00])

#Set the time to date only to strip the time so as to merge the different indexed series
instr_df_DayClose.index = instr_df_DayClose.index.date
frame = {'Open': instr_df_DayOpen, 'High':instr_df_DayHigh, 'Low': instr_df_DayLow,'Close':instr_df_DayClose}

# create a new dataframe for plotting
comb_DailyData = pd.DataFrame(frame)
comb_DailyData.index.name ='Date'
print (instr_df)
print (equilData)
print(rsiQuantile)
print (willrQuantile)
print (instr_df.columns)
# print (instr_df.info())
print (comb_DailyData.tail(25))
# plt.plot(comb_DailyData['High'])
plt.plot (equilData['equilPrice'])
plt.show()

