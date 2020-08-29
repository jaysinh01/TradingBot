from sklearn import preprocessing

from stock import *
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint

#testing out pairs trading

cola = Stock("INTC")
pep = Stock("NVDA")

colaData = cola.fetchHistoricData("ytd", "1d")
pepData = pep.fetchHistoricData("ytd", "1d")

#print(colaData["Close"])
#print(type(pepData["Close"]))

#normalize data
colaData["Close"] = preprocessing.normalize([colaData["Close"]])[0]
pepData["Close"] = preprocessing.normalize([pepData["Close"]])[0]

#calculate percent change in the series
colaPercentChange = colaData["Close"].pct_change().tail(len(colaData)-1)
pepPercentChange = pepData["Close"].pct_change().tail(len(pepData)-1)

#claclulate corration and cointegration
print(colaPercentChange.corr(pepPercentChange))
score, pvalue, _ = coint(colaData["Close"], pepData["Close"])
print('Cointegration %f is %f' % (score, pvalue))

#plot normalized data
plt.figure(figsize=(12,5))
ax1 = colaData["Close"].plot(color='green', grid=True, label='KO')
ax2 = pepData["Close"].plot(color='purple', grid=True, secondary_y=False, label='PEP')
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
plt.legend(h1+h2, l1+l2, loc=2)
plt.show()

#plot differnce in percent change
plt.figure(figsize=(12,5))
ax1 = (colaPercentChange - pepPercentChange).plot(color='green', grid=True, label='KO - PEP')
plt.grid(True)
plt.axhline(y=0, color='black', linestyle='-')
plt.axhline(y=0.02, color='red', linestyle='-')
plt.axhline(y=-0.02, color='red', linestyle='-')
plt.show()