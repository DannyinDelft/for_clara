# -*- coding: utf-8 -*-
#-- GEO1001.2020--hw01
#-- [Danny Marx]
#-- [4624475]
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy
import seaborn as sns
from scipy.stats import  spearmanr,ttest_ind
from pylab import axvline

df=[]

#Create Dataframes from files

df.append(pd.read_excel ('C:/Users/marxd/Desktop/GEO1001_ST/2020/A1_Resit/HEAT - A_final.xls', skiprows=[0,1,2,4]))
df.append(pd.read_excel ('C:/Users/marxd/Desktop/GEO1001_ST/2020/A1_Resit/HEAT - B_final.xls', skiprows=[0,1,2,4]))
df.append(pd.read_excel ('C:/Users/marxd/Desktop/GEO1001_ST/2020/A1_Resit/HEAT - C_final.xls', skiprows=[0,1,2,4]))
df.append(pd.read_excel ('C:/Users/marxd/Desktop/GEO1001_ST/2020/A1_Resit/HEAT - D_final.xls', skiprows=[0,1,2,4]))
df.append(pd.read_excel ('C:/Users/marxd/Desktop/GEO1001_ST/2020/A1_Resit/HEAT - E_final.xls', skiprows=[0,1,2,4]))



#Compute mean, variance and std for all variables

#Mean
for i in range(5):
    print('The mean for sensor',i+1,'is:\n',df[i].mean(axis = 0, skipna = True))


#Variance
for i in range(5):
    print('The variance for sensor',i+1,'is:\n',df[i].var(axis = 0, skipna = True))

#std
for i in range(5):
    print('The stdvariance for sensor',i+1,'is:\n',df[i].std(axis = 0, skipna = True))



#1 plot that contains histograms for the 5 sensors Wind Direction values
for i in range(5):
    plt.hist(df[i]['Direction ‚ True'],bins = 5,alpha=0.5,label='Sensor'+str(i+1))
plt.legend(loc='upper right')
plt.title('Wind Direction Histograms for all Sensors')
plt.show()

for i in range(5):
    plt.hist(df[i]['Direction ‚ True'],bins = 50,alpha=0.5,label='Sensor'+str(i+1))
plt.legend(loc='upper right')
plt.title('Wind Direction Histograms for all Sensors')
plt.show()

#the number of bins are important as they point to the peaks in a distribution. Using 5 bins doesn't portray the data too well. 
#On the other hand, using 50 bins looks better but is also doesn't give sense of distribution
#Frequency Polygon
for i in range(5):
    plt.hist(df[i]['Temperature'],alpha=0.5,label='Sensor'+str(i+1))
plt.legend(loc='upper right')
plt.title('Temperature Histograms for all Sensors')
plt.show()


#3 plots that include the 5 sensors boxplot for: Wind Speed, Wind Direction and Temperature

plt.boxplot([df[0]['Wind Speed'],df[1]['Wind Speed'],df[2]['Wind Speed'],df[3]['Wind Speed'],df[4]['Wind Speed']])
plt.title('Wind Speed')
plt.show()

plt.boxplot([df[0]['Direction ‚ True'],df[1]['Direction ‚ True'],df[2]['Direction ‚ True'],df[3]['Direction ‚ True'],df[4]['Direction ‚ True']])
plt.title('Direction ‚ True')
plt.show()

plt.boxplot([df[0]['Temperature'],df[1]['Temperature'],df[2]['Temperature'],df[3]['Temperature'],df[4]['Temperature']])
plt.title('Temperature')
plt.show()




#PMF, PDF and CDF for the 5 sensors Temperature values in independent plots
#PMF
fig, axes = plt.subplots(1, 5, figsize=(15, 5), sharey=True)
fig.suptitle('PMF')
for i in range(5):
    probabilities = df[i]['Temperature'].value_counts(normalize=True)    
    sns.barplot(ax=axes[i],x=probabilities.index, y=probabilities.values)
    axes[i].set_title('Sensor'+str(i+1))


#PDF
stats_df=[]
for i in range(5):
    stats_df.append(df[i]\
                    .groupby('Temperature')\
                        ['Temperature']\
                            .agg('count')\
                                .pipe(pd.DataFrame)\
                                    .rename(columns={'Temperature':'frequency'}))
                        
        #pdf

    stats_df[i]['pdf']=stats_df[i]['frequency']/sum(stats_df[i]['frequency'])

    #cdf
    stats_df[i]['cdf'] = stats_df[i]['pdf'].cumsum()
    stats_df[i] = stats_df[i].reset_index()
    
#PDF Plot
fig, axes = plt.subplots(1, 5, figsize=(15, 5), sharey=True)
fig.suptitle('PDF')
for i in range(5):  
    sns.barplot(ax=axes[i],x=stats_df[i]['Temperature'], y=stats_df[i]['pdf'])
    axes[i].set_title('Sensor'+str(i+1))

#CDF Plot
fig, axes = plt.subplots(1, 5, figsize=(15, 5), sharey=True)
fig.suptitle('CDF')
for i in range(5):  
    sns.lineplot(ax=axes[i],x=stats_df[i]['Temperature'], y=stats_df[i]['cdf'])
    axes[i].set_title('Sensor'+str(i+1))
    
#pdf and the kernel density estimation for the Wind Speed values


stats_df=[]
for i in range(5):
    stats_df.append(df[i]\
                    .groupby('Wind Speed')\
                        ['Wind Speed']\
                            .agg('count')\
                                .pipe(pd.DataFrame)\
                                    .rename(columns={'Wind Speed':'frequency'}))
                        
        #pdf

    stats_df[i]['pdf']=stats_df[i]['frequency']/sum(stats_df[i]['frequency'])
    stats_df[i] = stats_df[i].reset_index()

fig, axes = plt.subplots(1, 5, figsize=(15, 5), sharey=True)
fig.suptitle('PDF')
for i in range(5):  
    sns.barplot(ax=axes[i],x=stats_df[i]['Wind Speed'], y=stats_df[i]['pdf'])
    axes[i].set_title('Sensor'+str(i+1))
    

ax=df[0]['Wind Speed'].plot.kde(label='KDE plot for sensor 1',legend=True)
ax=df[1]['Wind Speed'].plot.kde(label='KDE plot for sensor 2',legend=True)
ax=df[2]['Wind Speed'].plot.kde(label='KDE plot for sensor 3',legend=True)
ax=df[3]['Wind Speed'].plot.kde(label='KDE plot for sensor 4',legend=True)
ax=df[4]['Wind Speed'].plot.kde(label='KDE plot for sensor 5',legend=True)

#The KDE plots for sensor B and E do not correspond to their respective PDFs. In theory, PDF is 
#constructed using the KDE plot. So, they should show similar distribution. The culprit might be too many
#zero values for the temperature.


#Correlations between all the sensors for the variables: Temperature, Wet Bulb Globe Temperature (WBGT), Crosswind Speed
# Let's make the dataframe lengths equal
df[0].drop(df[0].tail(1).index,inplace=True)
df[3].drop(df[3].tail(2).index,inplace=True)
df[4].drop(df[4].tail(2).index,inplace=True)

temp_corr_p=[]
wbg_corr_p=[]
cws_corr_p=[]

temp_corr_s=[]
wbg_corr_s=[]
cws_corr_s=[]

for i in range(5):
    for j in range(5):
        temp_corr_p.append(df[i]['Temperature'].corr(df[j]['Temperature']))
        wbg_corr_p.append(df[i]['Globe Temperature'].corr(df[j]['Globe Temperature']))
        cws_corr_p.append(df[i]['Crosswind Speed'].corr(df[j]['Crosswind Speed']))
        a,b=spearmanr(df[i]['Temperature'],df[j]['Temperature'])
        temp_corr_s.append(a)
        a,b=spearmanr(df[i]['Globe Temperature'],df[j]['Globe Temperature'])
        wbg_corr_s.append(a)
        a,b=spearmanr(df[i]['Crosswind Speed'],df[j]['Crosswind Speed'])
        cws_corr_s.append(a)
fig=plt.subplots()        
plt.scatter(temp_corr_p,temp_corr_s,label='Temperature')
plt.scatter(wbg_corr_p,wbg_corr_s,label='Wet Bulb Globe Temperature')
plt.scatter(cws_corr_p,cws_corr_s,label='Crosswind Speed')
plt.xlabel('Pearsons Coefficient')
plt.ylabel('Spearmans Rank Coefficient')
plt.legend(loc='upper left')
plt.show()

#First of all pearsons and spearmans rank coeffiecients give similar results.There is a very high correlation between temperature values, this is because
#the sensors are in close proximity. The wet bulb globe temperature also shows very high correlations, however the correlation between B,C,D and E. They might be closer.
#For cross wind speed the correlations are more or less similar except B and D have a lower correlation. Also, the highest correlation is observed between B and C. This means they are close to each other.
#E and D also have a slightly higher correlation.





stats_df_temp=[]
for i in range(5):
    stats_df_temp.append(df[i]\
                    .groupby('Temperature')\
                        ['Temperature']\
                            .agg('count')\
                                .pipe(pd.DataFrame)\
                                    .rename(columns={'Temperature':'frequency'}))
                        
        #pdf

    stats_df_temp[i]['pdf']=stats_df_temp[i]['frequency']/sum(stats_df[i]['frequency'])

    #cdf
    stats_df_temp[i]['cdf'] = stats_df_temp[i]['pdf'].cumsum()
    stats_df_temp[i] = stats_df_temp[i].reset_index()

stats_df_hum=[]
for i in range(5):
    stats_df_hum.append(df[i]\
                    .groupby('Relative Humidity')\
                        ['Relative Humidity']\
                            .agg('count')\
                                .pipe(pd.DataFrame)\
                                    .rename(columns={'Relative Humidity':'frequency'}))
                        
        #pdf

    stats_df_hum[i]['pdf']=stats_df_hum[i]['frequency']/sum(stats_df[i]['frequency'])

    #cdf
    stats_df_hum[i]['cdf'] = stats_df_hum[i]['pdf'].cumsum()
    stats_df_hum[i] = stats_df_hum[i].reset_index()




fig, axes = plt.subplots(1, 5, figsize=(15, 5), sharey=True)
fig.suptitle('CDF Temperature')
for i in range(5):  
    sns.barplot(ax=axes[i],x=stats_df_temp[i]['Temperature'], y=stats_df_temp[i]['cdf'])
    axes[i].set_title('Sensor'+str(i+1))

fig, axes = plt.subplots(1, 5, figsize=(15, 5), sharey=True)
fig.suptitle('CDF Humidity')
for i in range(5):  
    sns.barplot(ax=axes[i],x=stats_df_hum[i]['Relative Humidity'], y=stats_df_hum[i]['cdf'])
    axes[i].set_title('Sensor'+str(i+1))

cI_temp=[]
cI_hum=[]

for i in range(5):
    cI_temp.append(scipy.stats.norm.interval(alpha=0.95, loc=np.mean(df[i]['Temperature'])))
    cI_hum.append(scipy.stats.norm.interval(alpha=0.95, loc=np.mean(df[i]['Relative Humidity'])))

fig=plt.subplots()
p1=axvline(x=cI_temp[0][0])
p2=axvline(x=cI_temp[0][1])
sns.lineplot(x=stats_df_temp[0]['Temperature'], y=stats_df_temp[0]['cdf'],ci=95).set_title('Sensor A')
fig=plt.subplots()
p1=axvline(x=cI_temp[1][0])
p2=axvline(x=cI_temp[1][1])
sns.lineplot(x=stats_df_temp[1]['Temperature'], y=stats_df_temp[1]['cdf'],ci=95).set_title('Sensor B')
fig=plt.subplots()
p1=axvline(x=cI_temp[2][0])
p2=axvline(x=cI_temp[2][1])
sns.lineplot(x=stats_df_temp[2]['Temperature'], y=stats_df_temp[2]['cdf'],ci=95).set_title('Sensor C')
fig=plt.subplots()
p1=axvline(x=cI_temp[3][0])
p2=axvline(x=cI_temp[3][1])
sns.lineplot(x=stats_df_temp[3]['Temperature'], y=stats_df_temp[3]['cdf'],ci=95).set_title('Sensor D')
fig=plt.subplots()
p1=axvline(x=cI_temp[4][0])
p2=axvline(x=cI_temp[4][1])
sns.lineplot(x=stats_df_temp[4]['Temperature'], y=stats_df_temp[4]['cdf'],ci=95).set_title('Sensor E')


fig=plt.subplots()
p1=axvline(x=cI_hum[0][0])
p2=axvline(x=cI_hum[0][1])
sns.lineplot(x=stats_df_hum[0]['Relative Humidity'], y=stats_df_hum[0]['cdf'],ci=95).set_title('Sensor A')
fig=plt.subplots()
p1=axvline(x=cI_hum[1][0])
p2=axvline(x=cI_hum[1][1])
sns.lineplot(x=stats_df_hum[1]['Relative Humidity'], y=stats_df_hum[1]['cdf'],ci=95).set_title('Sensor B')
fig=plt.subplots()
p1=axvline(x=cI_hum[2][0])
p2=axvline(x=cI_hum[2][1])
sns.lineplot(x=stats_df_hum[2]['Relative Humidity'], y=stats_df_hum[2]['cdf'],ci=95).set_title('Sensor C')
fig=plt.subplots()
p1=axvline(x=cI_hum[3][0])
p2=axvline(x=cI_hum[3][1])
sns.lineplot(x=stats_df_hum[3]['Relative Humidity'], y=stats_df_hum[3]['cdf'],ci=95).set_title('Sensor D')
fig=plt.subplots()
p1=axvline(x=cI_hum[4][0])
p2=axvline(x=cI_hum[4][1])
sns.lineplot(x=stats_df_hum[4]['Relative Humidity'], y=stats_df_hum[4]['cdf'],ci=95).set_title('Sensor E')

p_val_temp=[]
p_val_ws=[]
#Are the time series for Temperature and Wind Speed same for E,D?
A=df[4]['Temperature'].values.tolist()
B=df[3]['Temperature'].values.tolist()
C=df[4]['Wind Speed'].values.tolist()
D=df[3]['Wind Speed'].values.tolist()

t_check1=ttest_ind(A,B)
p_val_temp.append(t_check1[1])
t_check2=ttest_ind(C,D)
p_val_ws.append(t_check2[1])

alpha=0.05
if(t_check1[1]<alpha or t_check2[1]<alpha):
    print('Variable values of Sensor E different from Sensor D')
else:
    print('Variable values of Sensor E same as Sensor D')
    
#Are the time series for Temperature and Wind Speed same for D,C?
A=df[3]['Temperature'].values.tolist()
B=df[2]['Temperature'].values.tolist()
C=df[3]['Wind Speed'].values.tolist()
D=df[2]['Wind Speed'].values.tolist()

t_check1=ttest_ind(A,B)
p_val_temp.append(t_check1[1])
t_check2=ttest_ind(C,D)
p_val_ws.append(t_check2[1])

alpha=0.05
if(t_check1[1]<alpha or t_check2[1]<alpha):
    print('Variable values of Sensor D different from Sensor C')
else:
    print('Variable values of Sensor D same as Sensor C')
    
#Are the time series for Temperature and Wind Speed same for C,B?
A=df[2]['Temperature'].values.tolist()
B=df[1]['Temperature'].values.tolist()
C=df[2]['Wind Speed'].values.tolist()
D=df[1]['Wind Speed'].values.tolist()

t_check1=ttest_ind(A,B)
p_val_temp.append(t_check1[1])
t_check2=ttest_ind(C,D)
p_val_ws.append(t_check2[1])

alpha=0.05
if(t_check1[1]<alpha or t_check2[1]<alpha):
    print('Variable values of Sensor C different from Sensor B')
else:
    print('Variable values of Sensor C same as Sensor B')

#Are the time series for Temperature and Wind Speed same for B,A?
A=df[1]['Temperature'].values.tolist()
B=df[0]['Temperature'].values.tolist()
C=df[1]['Wind Speed'].values.tolist()
D=df[0]['Wind Speed'].values.tolist()

t_check1=ttest_ind(A,B)
p_val_temp.append(t_check1[1])
t_check2=ttest_ind(C,D)
p_val_ws.append(t_check2[1])

alpha=0.05
if(t_check1[1]<alpha or t_check2[1]<alpha):
    print('Variable values of Sensor B different from Sensor A')
else:
    print('Variable values of Sensor B same as Sensor A')

print('P values for temperature comparison are, respectively:', p_val_temp )
print('P values for Wind Speed comparison are, respectively:', p_val_ws )

#P values of temperature are higher for the first four relationship. the only exception is B and A. That means only A is far away.
#Secondly, we see that cross wind speed P value is  higher than alpha for only for E and D. That means they experience similar cross wind. 
#Although B and C are similar based on temperature they are different based on cross wind speed. 

#We know that sensors B,C,D,E give same temperature values but A doesn't
#We ignore the temperature values from A
#Determine the max and min Temperature from the chosen sensors first and get the corresponding day
for i in range(5):
    df[i]['day']=df[i]['FORMATTED DATE-TIME'].dt.day

time_max=[]
time_min=[]
for i in range(4):
    maxVal=df[i+1]['Temperature'].max()
    time_max.append(df[i+1].loc[df[i+1]['Temperature']==maxVal,'day'])
    minVal=df[i+1]['Temperature'].min()
    time_min.append(df[i+1].loc[df[i+1]['Temperature']==minVal,'day'])

day_max=[]
day_min=[]

for i in time_max:
    day_max.append(np.bincount(i).argmax())

for i in time_min:
    day_min.append(np.bincount(i).argmax())

day_max=np.array(day_max)
day_min=np.array(day_min)

print('The hottest day is: ', np.bincount(day_max).argmax())
print('The coldest day is: ', np.bincount(day_min).argmax())

