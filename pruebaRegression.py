#Código para extender ETFs, programado por Sergio Molina www.carterasdebolsa.com

from scipy import stats
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.chdir('C:\\Users\\Abrilnil\\Desktop\\data\\TiingoEOD') #directorio de trabajo donde están ubicados los CSV

NameETF='SSO'      #Ticker del ETF que quieres extender
NameProxy='SPY'   #Ticker del CSV que hace de Proxy

ETF = pd.read_csv(NameETF+'.csv', names=['fecha', 'open', 'high', 'low',
                                     'close', 'volume'], index_col=['fecha'],parse_dates=True)



Proxy = pd.read_csv(NameProxy+'.csv', names=['fecha', 'open', 'high', 'low',
                                         'close', 'volume'],index_col=['fecha'],parse_dates=True)

ETF['returns']= (ETF['close']/ETF['close'].shift(1))-1
Proxy['returns'] = (Proxy['close'] / Proxy['close'].shift(1))-1

fechaInicio = ETF.index[1]

gradient, intercept, r_value, p_value, std_err = stats.linregress(Proxy['returns'].loc[fechaInicio:, ], ETF['returns'].loc[fechaInicio:, ])
print("Gradient and intercept",gradient,intercept,r_value**2)

Proxy.at[0:1, 'returns'] = 0
Proxy['returns+1']=Proxy['returns']+1

Proxy['out'] = (1 + (Proxy['returns'] * gradient + intercept))
Proxy.at[0:1, 'out'] = Proxy['close']

Proxy['out2']=Proxy['out']
Proxy['out2'].loc[fechaInicio:, ] = ETF['returns']+1

Proxy['output'] = np.cumprod(Proxy['out2'])

Proxy['output'].to_csv(NameETF+'+.csv')

print(Proxy)

Proxy['close'].plot(label='Proxy')
Proxy['output'].plot(label=NameETF+'+')


plt.legend(loc=0)
plt.show()
