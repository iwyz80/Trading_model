import talib as ta
import numpy as np
import pandas as pd
def maCombinations():
    # equilibrumPrice = [] #List to append equilibrum prices between two corresponding MAs
    combinationMA = [] #List to append the moving averages combinations
    # List of Moving averages periods to calculate
    shortMA =[5, 10, 14, 20, 50, 100]
    longMA = [10, 20, 50, 100, 200]
    combinationMA = [[sht, lng] for sht in shortMA for lng in longMA if lng > sht]
    return combinationMA



#Feature function
def feature_create (dataFrame):
    feature = pd.DataFrame()
    equilibrumPrice= pd.DataFrame()
    equ = []
    eqil = []
    dataFrame =RSI(dataFrame)
    dataFrame =williamsR(dataFrame)
    for s_ShortMA, l_LongMA in maCombinations():
   
        #Calculate the short moving average with the close column
        dataFrame['slow_shortMa_'+str(s_ShortMA)] = round(dataFrame['Close'].rolling (window=s_ShortMA, min_periods = 5).mean(),3)

        #Calculate the long moving average with the High column
        dataFrame['fast_longMA_' + str(l_LongMA)] = round(dataFrame['High'].rolling (window = l_LongMA, min_periods= 5).mean(), 3)
        
        #Append prices where the slow and fast MAs are the same.
        for index, value in dataFrame.iterrows():
            if value['slow_shortMa_'+str(s_ShortMA)]==value['fast_longMA_' + str(l_LongMA)] and value['fast_longMA_' + str(l_LongMA)] not in eqil:
                eqil.append(value['fast_longMA_' + str(l_LongMA)])
                equ.append([index, value['fast_longMA_' + str(l_LongMA)]])
                #feature = pd.concat([feature,dataFrame[['Open', 'High', 'Low','Close','fast_longMA_' + str(l_LongMA),'RSI_H_14', 'RSI_C_14','RSI_H_21', 'RSI_C_21', 'WILLR_14','WILLR_21']].loc[dataFrame.index==index]])

        #location where the slowma equals the fastma
        #dataFrame['slow_shortMa_'+str(s_ShortMA)+'equ'+'fast_longMA_' + str(l_LongMA)] = np.where( dataFrame['slow_shortMa_'+str(s_ShortMA)]== dataFrame['fast_longMA_' + str(l_LongMA)],  dataFrame['fast_longMA_' + str(l_LongMA)], float(np.nan))
        
        #equilibrumPrice.append([dataFrame['slow_shortMa_'+str(s_ShortMA)+'equ'+'fast_longMA_' + str(l_LongMA)].notnull().sum(), 'slow_shortMa_'+str(s_ShortMA)+'equ'+'fast_longMA_' + str(l_LongMA)])
        
    #Sort the values of the equilibrum price by date 
    equ = sorted(equ)
    

    #create a new dataframe with the equilibrum price and the dates
    equilibrumPrice = pd.DataFrame(data=[price[1] for price in equ], index=[index[0] for index in equ], columns=['equilPrice'])
    equilibrumPrice.index.rename('Gmt time', inplace=True)

    #create a subset with the dates of the equilibrum price.
    for t_idx in equ:
        feature = pd.concat([feature, dataFrame[['Open', 'High', 'Low','Close','RSI_H_14', 'RSI_C_14','RSI_H_21', 'RSI_C_21', 'WILLR_14','WILLR_21']].iloc[dataFrame.index==t_idx[0]]])
    
    #Join the two dataframes to create the feature dataframe
    df_feature = feature.join(equilibrumPrice)    
    #print (equilibrumPrice.info())
    #print (df_feature.info())
    return df_feature
    

#Calcute the RSI
def RSI (DataFrame):
    for period in [14, 21]:
        
        #Calculate the RSI for the high and close
        DataFrame['RSI_H_' + str(period)] = round (ta.RSI(DataFrame['High'], period), 2)
        DataFrame['RSI_C_' + str(period)] = round (ta.RSI(DataFrame['Close'], period), 2)

    return DataFrame

def stochastic(DataFrame):
    
    pass

#Calculate the WilliamsR
def williamsR (DataFrame):
    for period in [14, 21]:

        #Calculate WilliamsR for 14 and 21 periods
        DataFrame['WILLR_'+ str(period)] = round(ta.WILLR(DataFrame['High'], DataFrame['Low'], DataFrame['Close'], timeperiod=period), 2)
    return DataFrame

def OBV (DataFrame):
    pass

