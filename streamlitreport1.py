from datetime import datetime
import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import requests
import io


"""
# TRADING REPORT
"""
url= "https://raw.githubusercontent.com/tejaswi1995prakash/trading-report/main/Trading%20journal.csv"
download = requests.get(url).content
df = pd.read_csv(io.StringIO(download.decode('utf-8')))


df_IB = df[(df['System'] == 'IBFD_Invertir')].reset_index().drop(columns = ['index'])
df_fd = df[(df['System'] == 'FD System') | (df['System'] == 'Fd System')].reset_index().drop(columns = ['index'])
df_INTRA = df[(df['System'] == 'BNF_Intra')].reset_index().drop(columns = ['index'])

sum_IB = 250000
IB_eq = []
for i in range(len(df_IB)):
  p = df_IB.loc[i,'Net PnL']
  sum_IB = sum_IB+p
  IB_eq.append(sum_IB)

df_IB['eq'] = IB_eq

sum_fd = 250000
fd_eq = []
for i in range(len(df_fd)):
  p = df_fd.loc[i,'Net PnL']
  sum_fd = sum_fd+p
  fd_eq.append(sum_fd)

df_fd['eq'] = fd_eq

sum_INTRA = 250000
INTRA_eq = []
for i in range(len(df_INTRA)):
  p = df_INTRA.loc[i,'Net PnL']
  sum_INTRA = sum_INTRA + p
  INTRA_eq.append(sum_INTRA)

df_INTRA['eq'] = INTRA_eq

df_all = df.groupby('ENTRY DATE').sum().reset_index()

sum = 500000  
all_eq = []
for i in range(len(df_all)):
  p = df_all.loc[i,'Net PnL']
  sum = sum+p
  all_eq.append(sum)

df_all['eq'] = all_eq


#PLOTTING THE GRAPH
import plotly.graph_objects as go

All_systems = go.Figure()
All_systems.add_trace(go.Scatter(x= df_all['ENTRY DATE'], y= df_all['eq'], name= 'ALL SYSTEMS'))
All_systems.update_layout(title = "Performance of all systems")

IB_system = go.Figure()
IB_system.add_trace(go.Scatter(x= df_IB['ENTRY DATE'], y= df_IB['eq'], name= 'IB FD(INVERTIR)'))
IB_system.update_layout(title = "Performance of IB_FD(INVERTIR)")

FD_system = go.Figure()
FD_system.add_trace(go.Scatter(x= df_fd['ENTRY DATE'], y= df_fd['eq'], name= 'FD SYSTEM'))
FD_system.update_layout(title = "Performance of FD")

BNF_INTRA_system = go.Figure()
BNF_INTRA_system.add_trace(go.Scatter(x= df_INTRA['ENTRY DATE'], y= df_INTRA['eq'], name= 'BNF INTRA SYSTEM'))
BNF_INTRA_system.update_layout(title = "Performance of BNF INTRA")


charts = {'All_systems':All_systems,'Invertir':IB_system,'FD':FD_system,'BNF INTRA':BNF_INTRA_system}



chosen = st.radio(
        'Choose a system',
        ('All_systems','Invertir','FD','BNF INTRA'))

st.plotly_chart(charts[chosen])


all_colour = np.where(df_all['Net PnL']<0,'crimson','SeaGreen')
IB_colour = np.where(df_IB['Net PnL']<0,'crimson','SeaGreen')
FD_colour = np.where(df_fd['Net PnL']<0,'crimson','SeaGreen')
BNF_INTRA_colour = np.where(df_INTRA['Net PnL']<0,'crimson','SeaGreen')

"""
### Trade Distribution Graph
"""
ALL_TRADES = go.Figure()
ALL_TRADES.add_trace(go.Bar(x= df_all['ENTRY DATE'], y= df_all['Net PnL'], name= 'All Trades', marker_color = all_colour))
ALL_TRADES.update_layout(title = "PERFORMANCE")

IB_TRADES = go.Figure()
IB_TRADES.add_trace(go.Bar(x= df_IB['ENTRY DATE'], y= df_IB['Net PnL'], name= 'IB Trades', marker_color = IB_colour))
IB_TRADES.update_layout(title = "PERFORMANCE")

FD_TRADES = go.Figure()
FD_TRADES.add_trace(go.Bar(x= df_fd['ENTRY DATE'], y= df_fd['Net PnL'], name= 'FD Trades', marker_color = FD_colour))
FD_TRADES.update_layout(title = "PERFORMANCE")

BNF_INTRA_TRADES = go.Figure()
BNF_INTRA_TRADES.add_trace(go.Bar(x= df_INTRA['ENTRY DATE'], y= df_INTRA['Net PnL'], name= 'BNF INTRA Trades', marker_color = BNF_INTRA_colour))
BNF_INTRA_TRADES.update_layout(title = "PERFORMANCE")



trades = {'ALL_TRADES':ALL_TRADES,'INVERTIR_TRADES':IB_TRADES,'FD_TRADES':FD_TRADES,'BNF_INTRA_TRADES':BNF_INTRA_TRADES}



chosen1 = st.radio(
        'Choose a system',
        ('ALL_TRADES','INVERTIR_TRADES','FD_TRADES','BNF_INTRA_TRADES'))

st.plotly_chart(trades[chosen1])


"""
### Drawdown Graph
"""
previous_peak_all = df_all['eq'].cummax()
All_Systems_Drawdown1 = ((df_all['eq'] - previous_peak_all)/previous_peak_all)*100

previous_peak_IB = df_IB['eq'].cummax()
IB_System_Drawdown1 = ((df_IB['eq'] - previous_peak_IB)/previous_peak_IB)*100

previous_peak_FD = df_fd['eq'].cummax()
FD_System_Drawdown1 = ((df_fd['eq'] - previous_peak_FD)/previous_peak_FD)*100

previous_peak_INTRA = df_INTRA['eq'].cummax()
BNFINTRA_System_Drawdown1 = ((df_INTRA['eq'] - previous_peak_INTRA)/previous_peak_INTRA)*100

df_all['Drawdown'] = All_Systems_Drawdown1
df_IB['Drawdown'] = IB_System_Drawdown1
df_fd['Drawdown'] = FD_System_Drawdown1
df_INTRA['Drawdown'] = BNFINTRA_System_Drawdown1




All_Systems_Drawdown = go.Figure()
All_Systems_Drawdown.add_trace(go.Scatter(x= df_all['ENTRY DATE'], y= df_all['Drawdown'], name= 'All Systems Drawdown', marker_color = 'crimson'))
All_Systems_Drawdown.update_layout(title = "DRAWDOWN")

IB_System_Drawdown = go.Figure()
IB_System_Drawdown.add_trace(go.Scatter(x= df_IB['ENTRY DATE'], y= df_IB['Drawdown'], name= 'IB System Drawdown', marker_color = 'crimson'))
IB_System_Drawdown.update_layout(title = "DRAWDOWN")

FD_System_Drawdown = go.Figure()
FD_System_Drawdown.add_trace(go.Scatter(x= df_fd['ENTRY DATE'], y= df_fd['Drawdown'], name= 'FD System Drawdown', marker_color = 'crimson'))
FD_System_Drawdown.update_layout(title = "DRAWDOWN")

BNFINTRA_System_Drawdown = go.Figure()
BNFINTRA_System_Drawdown.add_trace(go.Scatter(x= df_INTRA['ENTRY DATE'], y= df_INTRA['Drawdown'], name= 'BNF INTRA System Drawdown', marker_color = 'crimson'))
BNFINTRA_System_Drawdown.update_layout(title = "DRAWDOWN")


dd = {'All_Systems_Drawdown':All_Systems_Drawdown,'INVERTIR_System_Drawdown':IB_System_Drawdown,'FD_System_Drawdown':FD_System_Drawdown,'BNFINTRA_System_Drawdown':BNFINTRA_System_Drawdown}

chosen2 = st.radio(
        'Choose a system',
        ('All_Systems_Drawdown','INVERTIR_System_Drawdown','FD_System_Drawdown','BNFINTRA_System_Drawdown'))

st.plotly_chart(dd[chosen2])

current_equity = round(df_all.iloc[-1]['eq'])



#PEAKS
peak_all = round(previous_peak_all[len(previous_peak_all)-1])
peak_IB = round(previous_peak_IB[len(previous_peak_IB)-1])
peak_FD = round(previous_peak_FD[len(previous_peak_FD)-1])
peak_BNF_INTRA = round(previous_peak_INTRA[len(previous_peak_INTRA)-1])

#CURRENT EQUITY
current_equity_all = round(df_all.iloc[-1]['eq']) - 500000
current_equity_IB = round(df_IB.iloc[-1]['eq']) - 250000
current_equity_FD = round(df_fd.iloc[-1]['eq']) - 250000
current_equity_BNF_INTRA = round(df_INTRA.iloc[-1]['eq']) - 250000

#DRAWDOWN MAX
drawdown_all = round(min(All_Systems_Drawdown1),1)
drawdown_IB = round(min(IB_System_Drawdown1),1)
drawdown_FD = round(min(FD_System_Drawdown1),1)
drawdown_BNF_INTRA = round(min(BNFINTRA_System_Drawdown1),1)


#Profit Factor 
Invertir_Win_Rate = (len(df_IB[df_IB['Result'] == 'WIN'])/len(df_IB))*100
Invertir_Loss_Rate = (1 - (len(df_IB[df_IB['Result'] == 'WIN'])/len(df_IB)))*100
Invertir_Avg_Win = df_IB[df_IB['Result'] == 'WIN']['Net PnL'].mean()
Invertir_Avg_Loss = abs(df_IB[df_IB['Result'] == 'LOSS']['Net PnL'].mean())
Invertir_Profit_Factor = (Invertir_Win_Rate*Invertir_Avg_Win)/(Invertir_Loss_Rate*Invertir_Avg_Loss)

Fd_Win_Rate = (len(df_fd[df_fd['Result'] == 'WIN'])/len(df_fd))*100
Fd_Loss_Rate = (1 - (len(df_fd[df_fd['Result'] == 'WIN'])/len(df_fd)))*100
Fd_Avg_Win = df_fd[df_fd['Result'] == 'WIN']['Net PnL'].mean()
Fd_Avg_Loss = abs(df_fd[df_fd['Result'] == 'LOSS']['Net PnL'].mean())
Fd_Profit_Factor = (Fd_Win_Rate*Fd_Avg_Win)/(Fd_Loss_Rate*Fd_Avg_Loss)

Intra_Win_Rate = (len(df_INTRA[df_INTRA['Result'] == 'WIN'])/len(df_INTRA))*100
Intra_Loss_Rate = (1 - (len(df_INTRA[df_INTRA['Result'] == 'WIN'])/len(df_INTRA)))*100
Intra_Avg_Win = df_INTRA[df_INTRA['Result'] == 'WIN']['Net PnL'].mean()
Intra_Avg_Loss = abs(df_INTRA[df_INTRA['Result'] == 'LOSS']['Net PnL'].mean())
Intra_Profit_Factor = (Intra_Win_Rate*Intra_Avg_Win)/(Intra_Loss_Rate*Intra_Avg_Loss)

All_Win_Rate = (len(df[df['Result'] == 'WIN'])/len(df))*100
All_Loss_Rate = (1 - (len(df[df['Result'] == 'WIN'])/len(df)))*100
All_Avg_Win = df[df['Result'] == 'WIN']['Net PnL'].mean()
All_Avg_Loss = abs(df[df['Result'] == 'LOSS']['Net PnL'].mean())
All_Profit_Factor = (All_Win_Rate*All_Avg_Win)/(All_Loss_Rate*All_Avg_Loss)


# initialize list of lists
data = [[peak_all,drawdown_all,current_equity_all, All_Win_Rate, All_Profit_Factor ], [peak_IB, drawdown_IB,current_equity_IB,Invertir_Win_Rate,Invertir_Profit_Factor], [peak_FD,drawdown_FD ,current_equity_FD,Fd_Win_Rate,Fd_Profit_Factor], [peak_BNF_INTRA, drawdown_BNF_INTRA,current_equity_BNF_INTRA, Intra_Win_Rate,Intra_Profit_Factor]]
df1 = pd.DataFrame(data, columns = ['PEAK', 'MAX_DRAWDOWN (%)', 'P&L','Win Rate', 'Profit Factor'])
df1['SYSTEMS'] = ['All Systems', "INVERTIR","FD"," BNF INTRA"]
df1 = df1.set_index('SYSTEMS')

"""
## SYSTEMWISE REPORT
"""
st.write(df1)

left_column, right_column = st.beta_columns(2)
# You can use a column just like st.sidebar:
left_column.button('CURRENT ACCOUNT BALANCE = ')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    st.write(current_equity)

#Displaying the dataframe
if st.checkbox('Show dataframe'):
    chart_data = df

    chart_data