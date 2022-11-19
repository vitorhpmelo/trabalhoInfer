
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


#%%


usina="SAOSIMAO"
usina2="São Simão"

df=pd.read_csv(usina+".csv")
df['data']= pd.to_datetime(df['data'],)



#%%
dfHist=df[df['data']<="6/1/2022"].copy()
dfFuturo=df[df['data']>"6/1/2022"].copy()

#%%

x1=dfHist["Volume Útil (%)"].values
y1=dfHist["Cota (m)"].values
[a1,b1,r1,p1,std_err1]=stats.linregress(x1,y1)
x2=dfHist["Defluência (m³/s)"]
y2=dfHist["h2"].values
[a2,b2,r2,p2,std_err2]=stats.linregress(x2,y2)
# %%

plt.title(usina2+"\nVolume (vu%) x Cota (m)")
plt.xlabel("vu%")
plt.ylabel("Cota (m)")

X1=np.linspace(min(x1),max(x1))
plt.scatter(x1,y1,label="valores medidos",marker="d",color="r")
plt.plot(X1,a1*X1+b1,label="regressão",color="b")
ya=np.max(y1)
xa=np.min(x1)+0.05*np.mean(x1)
ofs=(np.max(y1)-np.min(y1))/10
plt.annotate("a = {:.2e}".format(a1),(xa,ya))
plt.annotate("b = {:.2e}".format(b1),(xa,ya-ofs))
plt.annotate("r = {:.2e}".format(r1),(xa,ya-2*ofs))
plt.annotate("std_err = {:.2e}".format(std_err1),(xa,ya-3*ofs))
plt.legend(loc="lower right")
plt.grid()
plt.savefig("regressãoh1"+usina+".jpg",dpi=1200)
plt.close()
#%%


model=np.poly1d(np.polyfit(x2, y2, 3))
#%%
X2=np.linspace(min(x2),max(x2))
fig=plt.title(usina2+"\nDefluência ($m^{3}/s$) x Nivel Canal de Fuga (m)")
plt.xlabel("Nivel Canal de Fuga (m)")
plt.ylabel("Defluência ($m^{3}/s$)")
plt.scatter(x2,y2,label="valores medidos",marker="d",color="r")
plt.plot(X2,a2*X2+b2,label="regressão linear",color="b")
plt.plot(X2,model(X2),label="regressão polinomial",color="g")
ya=np.max(y2)
xa=np.max(x2)-0.6*np.mean(x2)
ofs=(np.max(y2)-np.min(y2))/10
plt.annotate("a = {:.2e}".format(a1),(xa,ya))
plt.annotate("b = {:.2e}".format(b1),(xa,ya-ofs))
plt.annotate("r = {:.2e}".format(r1),(xa,ya-2*ofs))
plt.annotate("std_err = {:.2e}".format(std_err1),(xa,ya-3*ofs))
plt.legend(loc="lower right")
plt.grid()
plt.savefig("regressãoh2"+usina+".jpg",dpi=1200)
plt.close()

#%%
nt=0.92
ng=0.95
g=9.81
p=1000
PC=0.01
k=nt*ng*g*p*(1-PC)/1e6
dfHist["PGreglin"]=k*((a1*x1+b1)-(a2*x2+b2))*dfHist["Vazão Turbinada (m³/s)"]
dfHist["PGregpol3"]=k*((a1*x1+b1)-(model(x2)))*dfHist["Vazão Turbinada (m³/s)"]
dfHist["erroreglin"]=np.abs(dfHist["PGreglin"]-dfHist['PG'])
dfHist["erroregpol"]=np.abs(dfHist["PGregpol3"]-dfHist['PG'])

dfHist.to_csv("HistPrev"+usina+".csv")


#%%

x1=dfFuturo["Volume Útil (%)"].values
y1=dfFuturo["Cota (m)"].values
x2=dfFuturo["Defluência (m³/s)"]
y2=dfFuturo["h2"].values


dfFuturo["PGreglin"]=k*((a1*x1+b1)-(a2*x2+b2))*dfFuturo["Vazão Turbinada (m³/s)"]
dfFuturo["PGregpol3"]=k*((a1*x1+b1)-(model(x2)))*dfFuturo["Vazão Turbinada (m³/s)"]
dfFuturo["erroreglin"]=np.abs(dfFuturo["PGreglin"]-dfFuturo['PG'])
dfFuturo["erroregpol"]=np.abs(dfFuturo["PGregpol3"]-dfFuturo['PG'])
dfFuturo.to_csv("FuturoPrev"+usina+".csv")

# %%





