# -*- coding: utf-8 -*-
"""Regression & Correlation Analysis - Hospital Marketing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qB4Ybttj09lf-jawIrehR38YdcygMepY
"""

import pandas as pd
import numpy as np
import seaborn as sns
import scipy.stats

from google.colab import files
uploaded = files.upload()

data=pd.read_csv('Campaign-Data.csv')
data.columns

data.head(n=5)

data['Calendardate']=pd.to_datetime(data['Calendardate'])
data['Calendar_month']=data['Calendardate'].dt.month
data['Calendar_year']=data['Calendardate'].dt.year

data['Client Type'].value_counts()

pd.crosstab(data['Client Type'],data['Number of Competition'],margins=True)

data.groupby('Client Type').mean()

data.groupby('Number of Competition').mean()

data.corr()[['Amount Collected']]

cm = sns.light_palette("Yellow", as_cmap=True)
correlation_analysis=pd.DataFrame(data[['Amount Collected',
                                        'Campaign (Email)', 
                                        'Campaign (Flyer)',
                                        'Campaign (Phone)',
                                        'Sales Contact 1',
                                        'Sales Contact 2',
                                        'Sales Contact 3',
                                        'Sales Contact 4',
                                        'Sales Contact 5']].corr()['Amount Collected']).reset_index()
correlation_analysis.columns=['Marketing Channels','Correlation']
correlation_analysis=correlation_analysis[correlation_analysis['Marketing Channels']!='Amount Collected']
correlation_analysis=correlation_analysis.sort_values('Correlation',ascending=False)
correlation_analysis.style.background_gradient(cmap=cm).set_precision(3)

cm = sns.light_palette("Yellow", as_cmap=True)
correlation_analysis=pd.DataFrame(data.groupby('Client Type')[['Amount Collected',
                                                              'Campaign (Email)', 
                                                              'Campaign (Flyer)',
                                                              'Campaign (Phone)',
                                                              'Sales Contact 1',
                                                              'Sales Contact 2',
                                                              'Sales Contact 3',
                                                              'Sales Contact 4',
                                                              'Sales Contact 5']].corr()['Amount Collected']).reset_index()
correlation_analysis=correlation_analysis.sort_values(['Client Type','Amount Collected'],ascending=False)
correlation_analysis.columns=['Client Type','Marketing Channels','Correlation']
correlation_analysis=correlation_analysis[correlation_analysis['Marketing Channels']!='Amount Collected']
correlation_analysis.style.background_gradient(cmap=cm).set_precision(3)

import statsmodels.api as sm
import statsmodels.formula.api as smf
data.columns=[mystring.replace(" ","_") for mystring in data.columns]
data.columns=[mystring.replace("(","") for mystring in data.columns]
data.columns=[mystring.replace(")","") for mystring in data.columns]
results = smf.ols('Amount_Collected ~ Campaign_Email + Campaign_Flyer + Campaign_Phone + Sales_Contact_1 + Sales_Contact_2 + Sales_Contact_3 + Sales_Contact_4 + Sales_Contact_5',data=data).fit()
print(results.summary())

df = pd.read_html(results.summary().tables[1].as_html(),header=0,index_col=0)[0]

df=df.reset_index()
df=df[df['P>|t|']<0.05][['index','coef']]
df

consolidated_summary=pd.DataFrame()
for acctype in list(set(list(data['Client_Type']))):
  temp_data = data[data['Client_Type']==acctype].copy()
  results = smf.ols('Amount_Collected ~ Campaign_Email + Campaign_Flyer + Campaign_Phone + Sales_Contact_1 + Sales_Contact_2 + Sales_Contact_3 + Sales_Contact_4 + Sales_Contact_5',data=temp_data).fit()
  df = pd.read_html(results.summary().tables[1].as_html(),header=0,index_col=0)[0].reset_index()
  df=df[df['P>|t|']<0.05][['index','coef']]
  df.columns=['Variable','Coefficient (Impact)']
  df['Account Type']=acctype
  df=df.sort_values('Coefficient (Impact)',ascending=False)
  df=df[df['Variable']!='Intercept']
  print(acctype)
  consolidated_summary = consolidated_summary.append(df)
  print(df)
  #print(results.summary())

import statsmodels.api as sm
import statsmodels.formula.api as smf
consolidated_summary=pd.DataFrame()
for acctype in list(set(list(data['Client_Type']))):
  print(acctype)
  temp_data = data[data['Client_Type']==acctype].copy()
  results = smf.ols('Amount_Collected ~ Campaign_Email + Campaign_Flyer + Campaign_Phone + Sales_Contact_1 + Sales_Contact_2 + Sales_Contact_3 + Sales_Contact_4 + Sales_Contact_5',data=temp_data).fit()
  df = pd.read_html(results.summary().tables[1].as_html(),header=0,index_col=0)[0].reset_index()
  df=df[df['P>|t|']<0.05][['index','coef']]
  df.columns=['Variable','Coefficient (Impact)']
  df['Account Type']=acctype
  df=df.sort_values('Coefficient (Impact)',ascending=False)
  df=df[df['Variable']!='Intercept']
  consolidated_summary = consolidated_summary.append(df)
  print(results.summary())

consolidated_summary

consolidated_summary.reset_index(inplace=True)
consolidated_summary.drop('index',inplace=True,axis=1)

consolidated_summary.columns=['Variable','ROI','Account Type']
consolidated_summary['ROI'] = consolidated_summary['ROI'].apply(lambda x: round(x,1))
consolidated_summary.style.background_gradient(cmap='RdYlGn')

import seaborn as sns
import matplotlib.pyplot as plt

def format(x):
        return "${:.1f}".format(x)
consolidated_summary['ROI']  = consolidated_summary['ROI'].apply(format)

consolidated_summary.columns = ['Variable','Return on Investment','Account Type']
consolidated_summary.style.background_gradient(cmap='RdYlGn')

consolidated_summary.to_csv('consolidated_summary.csv')
files.download('consolidated_summary.csv')