# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 13:27:14 2019

@author: Henrik Brautmeier

CNN for decoding!
"""

# Neuronal Network 1 for learning the implied vola 
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import keras
from keras.models import Sequential,Model
from keras.layers import InputLayer,Dense,Flatten, Conv2D, Dropout, Input
from keras import backend as K
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
#import py_vollib.black_scholes.implied_volatility as vol
import time
import scipy

###matlab
def root_mean_squared_error(y_true, y_pred):
        return K.sqrt(K.mean(K.square(y_pred - y_true)))
    
def root_relative_mean_squared_error(y_true, y_pred):
        return K.sqrt(K.mean(K.square((y_pred - y_true)/y_true)))    

import scipy.io
mat = scipy.io.loadmat('data_price_week_all_4700_0005_09_11_30_210.mat')
data = mat['data_price']
Nparameters = 5
maturities = np.array([30, 60, 90, 120, 150, 180, 210])
strikes = np.array([0.9, 0.925, 0.95, 0.975, 1.0, 1.025, 1.05, 1.075, 1.1])
Nstrikes = len(strikes)   
Nmaturities = len(maturities)   
yy=data[:,:Nparameters]
xx=data[:,Nparameters+2:].reshape(4700,9,7,1)
X_train, X_test, y_train, y_test = train_test_split(
    xx, yy, test_size=0.15, random_state=42)

X_train, X_val, y_train, y_val = train_test_split(
   X_train, y_train, test_size=0.15, random_state=42)
"""picture scaling needs to be adjusted
scale=StandardScaler()
x_train_transform = scale.fit_transform(X_train)
x_val_transform   = scale.transform(X_val)
x_test_transform  = scale.transform(X_test)
def xtransform(x_train,x_val,x_test):
    return [scale.transform(x_train),scale.transform(x_val), 
            scale.transform(x_test)]
   
def xinversetransform(x):
    return scale.inverse_transform(x)

[X_train_trafo,X_val_trafo, X_test_trafo]=xtransform(X_train, X_val, X_test)

ub=np.amax(yy, axis=0)
lb=np.amin(yy, axis=0)
def myscale(y):
    res=np.zeros(Nparameters)
    for i in range(Nparameters):
        res[i]=(y[i] - (ub[i] + lb[i])*0.5) * 2 / (ub[i] - lb[i])
        
    return res
def myinverse(y):
    res=np.zeros(Nparameters)
    for i in range(Nparameters):
        res[i]=y[i]*(ub[i] - lb[i]) *0.5 + (ub[i] + lb[i])*0.5
        
    return res

X_train_trafo = np.array([myscale(x) for x in X_train])
X_val_trafo = np.array([myscale(x) for x in X_val])
X_test_trafo = np.array([myscale(x) for x in X_test])
"""
#Neural Network
keras.backend.set_floatx('float64')
NN1 = Sequential()#add model layers
NN1.add(InputLayer(input_shape=(9,7,1)))
NN1.add(Conv2D(64, kernel_size=3, activation='relu'))
NN1.add(Conv2D(32, kernel_size=3, activation='relu'))
#NN1.add(Dense(30, activation = 'elu'))
#NN1.add(Dropout(0.05))
NN1.add(Flatten())
NN1.add(Dense(50, activation = 'elu'))
NN1.add(Dense(5, activation='softmax'))
NN1.summary()

input1 = Input(shape = (9,7,1))
x1 = Conv2D(64, kernel_size=3, activation='relu')(input1)
x2 = Conv2D(64, kernel_size=3, activation='relu')(x1)
x3 = Flatten()(x2)
x4 = Dense(50, activation = 'elu')(x3)
seq1 = Dense(1, activation = 'linear')(x4)
seq2 = Dense(1, activation = 'linear')(x4)
seq3 = Dense(1, activation = 'linear')(x4)
seq4 = Dense(1, activation = 'linear')(x4)
seq5 = Dense(1, activation = 'linear')(x4)
out1 = keras.layers.merge.concatenate([seq1, seq2, seq3,seq4,seq5], axis=-1)
NN =Model(inputs=input1, outputs=out1)

        
#NN1.compile(loss = root_mean_squared_error, optimizer = "adam")
NN.compile(loss = 'mean_absolute_percentage_error', optimizer = "adam")
#NN1.compile(loss='categorical_crossentropy', optimizer = "adam")
NN.fit(X_train, y_train, batch_size=32, validation_data = (X_val, y_val),
        epochs = 200, verbose = True, shuffle=1)
#NN1.save_weights('NN_HNGarch_weights.h5')


#test = yinversetransform(NN1.predict(X_test_trafo))
#y_test_trans = yinversetransform(y_test_trafo)
#error = np.abs((test - y_test_trans))/np.abs(y_test_trans)
#error1 = np.zeros((len(error[0,:])))
#for i in range(len(error[0,:])):
#    error1[i] = np.mean(error[:,i])
    
#==============================================================================
#error plots

S0=1.
y_test_re = yinversetransform(y_test_trafo)
prediction_list=[yinversetransform(NN1.predict(X_test_trafo[i].reshape(1,Nparameters))[0]) for i in range(len(X_test_trafo))]
prediction = np.asarray(prediction_list)



plt.figure(figsize=(14,4))
ax=plt.subplot(1,3,1)
err = 100*np.mean(np.abs((y_test_re-prediction)/y_test_re),axis = 0)
plt.title("Average relative error",fontsize=15,y=1.04)
plt.imshow(err.reshape(Nmaturities,Nstrikes))
plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
plt.colorbar(format=mtick.PercentFormatter())
ax.set_xticks(np.linspace(0,Nstrikes-1,Nstrikes))
ax.set_xticklabels(strikes)
ax.set_yticks(np.linspace(0,Nmaturities-1,Nmaturities))
ax.set_yticklabels(maturities)
plt.xlabel("Strike",fontsize=15,labelpad=5)
plt.ylabel("Maturity",fontsize=15,labelpad=5)
plt.show()
ax=plt.subplot(1,3,2)
err = 100*np.std(np.abs((y_test_re-prediction)/y_test_re),axis = 0)
plt.title("Std relative error",fontsize=15,y=1.04)
plt.imshow(err.reshape(Nmaturities,Nstrikes))
plt.colorbar(format=mtick.PercentFormatter())
plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
ax.set_xticks(np.linspace(0,Nstrikes-1,Nstrikes))
ax.set_xticklabels(strikes)
ax.set_yticks(np.linspace(0,Nmaturities-1,Nmaturities))
ax.set_yticklabels(maturities)
plt.xlabel("Strike",fontsize=15,labelpad=5)
plt.ylabel("Maturity",fontsize=15,labelpad=5)

ax=plt.subplot(1,3,3)
err = 100*np.max(np.abs((y_test_re-prediction)/y_test_re),axis = 0)
plt.title("Maximum relative error",fontsize=15,y=1.04)
plt.imshow(err.reshape(Nmaturities,Nstrikes))
plt.colorbar(format=mtick.PercentFormatter())
ax.set_xticks(np.linspace(0,Nstrikes-1,Nstrikes))
ax.set_xticklabels(strikes)
ax.set_yticks(np.linspace(0,Nmaturities-1,Nmaturities))
ax.set_yticklabels(maturities)
plt.xlabel("Strike",fontsize=15,labelpad=5)
plt.ylabel("Maturity",fontsize=15,labelpad=5)
plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
plt.tight_layout()
plt.savefig('HNG_NNErrors.png', dpi=300)
plt.show()



#==============================================================================
#surface
import random
test_sample = random.randint(0,len(y_test))
y_test_sample = y_test_re[test_sample,:]
y_predict_sample = prediction_list[test_sample]
y_test_sample_p = np.reshape(y_test_sample, (Nmaturities, Nstrikes))
y_predict_sample_p = np.reshape(y_predict_sample, (Nmaturities, Nstrikes))
diff = y_test_sample_p-y_predict_sample_p 
rel_diff = np.abs(y_test_sample_p-y_predict_sample_p)/(y_test_sample_p)
    
# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
X = strikes
Y = maturities
X, Y = np.meshgrid(X, Y)


#ax.contour3D(X, Y, Z, 50, cmap='binary')
#ax.plot_surface(X, Y, y_test_sample_p, rstride=1, cstride=1,
#                cmap='viridis', edgecolor='none')
#ax.plot_surface(X, Y, y_predict_sample_p , rstride=1, cstride=1,
#                cmap='viridis', edgecolor='none')
ax.plot_surface(X, Y, rel_diff, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none')
ax.set_xlabel('Strikes')
ax.set_ylabel('Maturities')
ax.set_zlabel('rel. err');
plt.show()


#==============================================================================
#smile
sample_ind = 13
X_sample = X_test_trafo[sample_ind]
y_sample = y_test[sample_ind]
#print(scale.inverse_transform(y_sample))

prediction=yinversetransform(NN1.predict(X_sample.reshape(1,Nparameters))[0])
plt.figure(figsize=(14,12))
for i in range(Nmaturities):
    plt.subplot(4,4,i+1)
    
    plt.plot(np.log(strikes/S0),y_sample[i*Nstrikes:(i+1)*Nstrikes],'b',label="Input data")
    plt.plot(np.log(strikes/S0),prediction[i*Nstrikes:(i+1)*Nstrikes],'--r',label=" NN Approx")
    #plt.ylim(0.22, 0.26)
    
    plt.title("Maturity=%1.2f "%maturities[i])
    plt.xlabel("log-moneyness")
    plt.ylabel("Implied vol")
    
    plt.legend()
plt.tight_layout()
plt.savefig('HNG_smile.png', dpi=300)
plt.show()

#==============================================================================
# gradient methods for optimization with Levenberg-Marquardt
NNParameters=[]
for i in range(0,len(NN1.layers)):
    NNParameters.append(NN1.layers[i].get_weights())

NumLayers=3
def elu(x):
    #Careful function ovewrites x
    ind=(x<0)
    x[ind]=np.exp(x[ind])-1
    return x
def eluPrime(y):
    # we make a deep copy of input x
    x=np.copy(y)
    ind=(x<0)
    x[ind]=np.exp(x[ind])
    x[~ind]=1
    return x
def NeuralNetworkGradient(x):
    input1=x
    #Identity Matrix represents Jacobian with respect to initial parameters
    grad=np.eye(Nparameters)
    #Propagate the gradient via chain rule
    for i in range(NumLayers):
        input1=(np.dot(input1,NNParameters[i][0])+NNParameters[i][1])
        grad=(np.einsum('ij,jk->ik', grad, NNParameters[i][0]))
        #Elu activation
        grad*=eluPrime(input1)
        input1=elu(input1)
    #input1.append(np.dot(input1[i],NNParameters[i+1][0])+NNParameters[i+1][1])
    grad=np.einsum('ij,jk->ik',grad,NNParameters[i+1][0])
    #grad stores all intermediate Jacobians, however only the last one is used here as output
    return grad

#Cost Function for Levenberg Marquardt
def CostFuncLS(x,sample_ind):
    return (NN1.predict(x.reshape(1,Nparameters))[0]-y_test_trafo[sample_ind])
def JacobianLS(x,sample_ind):
    return NeuralNetworkGradient(x).T

def CostFunc(x,sample_ind):
    return np.sum(np.power((NN1.predict(x.reshape(1,Nparameters))[0]-y_test_trafo[sample_ind]),2))
def Jacobian(x,sample_ind):
    return 2*np.sum((NN1.predict(x.reshape(1,Nparameters))[0]-y_test_trafo[sample_ind])*NeuralNetworkGradient(x),axis=1)

Approx=[]
Timing=[]
#sample_ind = 500
#X_sample = X_test_trafo[sample_ind]
#y_sample = y_test[sample_ind]
solutions=np.zeros([1,Nparameters])
#times=np.zeros(1)
init=np.zeros(Nparameters)
n = X_test.shape[0]
#n=1000

for i in range(n):
    disp=str(i+1)+"/"+str(n)
    print (disp,end="\r")
    #L-BFGS-B
    #start= time.clock()
    #I=scipy.optimize.minimize(CostFunc,x0=init,args=i,method='L-BFGS-B',jac=Jacobian,tol=1E-10,options={"maxiter":5000})
    #end= time.clock()
    #solutions=myinverse(I.x)
    #times=end-start
    #Levenberg-Marquardt
    start= time.clock()
    I=scipy.optimize.least_squares(CostFuncLS, init, JacobianLS, args=(i,), gtol=1E-10)
    end= time.clock()
    solutions=myinverse(I.x)
    times=end-start
    Approx.append(np.copy(solutions))
    Timing.append(np.copy(times))
LMParameters=[Approx[i] for i in range(len(Approx))]
#np.savetxt("NNParametersHNG.txt",LMParameters)

#==============================================================================
#Calibration Errors with Levenberg-Marquardt¶
titles=["$\\alpha$","$\\beta$","$\\gamma$","$\\omega$", "$\\sigma$"]
average=np.zeros([Nparameters,n])
fig=plt.figure(figsize=(12,8))
for u in range(Nparameters):
    ax=plt.subplot(2,3,u+1)
    for i in range(n):
        
        X=X_test[i][u]
        plt.plot(X,100*np.abs(LMParameters[i][u]-X)/np.abs(X),'b*')
        average[u,i]=np.abs(LMParameters[i][u]-X)/np.abs(X)
    plt.title(titles[u],fontsize=20)
    plt.ylabel('relative Error',fontsize=15)
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter() )
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.tick_params(axis='both', which='minor', labelsize=15)
    plt.text(0.5, 0.8, 'Average: %1.2f%%\n Median:   %1.2f%% '%(np.mean(100*average[u,:]),
                                                                np.quantile(100*average[u,:],0.5)), horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,fontsize=15)

    print("average= ",np.mean(average[u,:]))
plt.tight_layout()
plt.savefig('HNG_ParameterRelativeErrors.png', dpi=300)
plt.show()



#==============================================================================
#RMSE plot
def bs_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    call = (S * scipy.stats.norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * scipy.stats.norm.cdf(d2, 0.0, 1.0))
    return call

RMSE_opt = np.zeros(n)
RMSE_bs = np.zeros(n)
bs_prices = np.zeros((n,Nmaturities*Nstrikes))
Y = len(y_test[0,:])
for i in range(n):
    Y = y_test[i,:]
    Y_pred = yinversetransform(NN1.predict(myscale(LMParameters[i]).reshape(1,Nparameters))[0])
    RMSE_opt[i] = np.sqrt(np.mean((Y-Y_pred)**2))
    bs = np.zeros((Nmaturities,Nstrikes))
    for t in range(Nmaturities):
        for k in range(Nstrikes):
            bs[t,k] = bs_call(1,strikes[k],maturities[t]/252,0.005,np.sqrt(252*LMParameters[i][-1]))
    bs_prices[i,:] = bs.T.reshape((1,Nmaturities*Nstrikes))
    RMSE_bs[i] = np.sqrt(np.mean((Y-bs_prices[i,:])**2))
    
fig =plt.figure(figsize=(12,8)) 
plt.plot(RMSE_opt)
plt.yscale('log')
plt.plot(RMSE_bs)
plt.yscale('log')
plt.legend(['Neural Net','Black-Scholes'],fontsize=17)
plt.ylabel('RMSE')
plt.xlabel('Scenario')
plt.title("RMSE of optimal parameters",fontsize=20)
plt.savefig('RMSE_BS_Net.png', dpi=300)
    
fig=plt.figure(figsize=(12,8))
plt.plot(RMSE_opt,'b*')
plt.title("RMSE of optimal parameters",fontsize=20)
plt.ylabel('RMSE vola surface',fontsize=15)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter() )
plt.tick_params(axis='both', which='major', labelsize=15)
plt.tick_params(axis='both', which='minor', labelsize=15)
plt.text(0.5, 0.8, 'Average: %1.2f%%\n Median:   %1.2f%% '%(np.mean(100*RMSE_opt),
            np.quantile(100*RMSE_opt,0.5)), horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,fontsize=15)
plt.tight_layout()
plt.show()

#==============================================================================
titles=["$\\alpha$","$\\beta$","$\\gamma$","$\\omega$", "$\\sigma$"]
plt.figure(figsize=(18, 5))
plt.clf()
plt.subplot(121)

ax = plt.gca()
q=np.linspace(0,0.99,200)
for u in range(Nparameters):
    p=plt.plot(100*q,np.quantile(100*average[u,:],q),label=titles[u])
    
    c=p[0].get_color()
ymin, ymax = ax.get_ylim()
ax.set_xlim(0,100)
plt.plot(100*np.ones(2)*0.95,np.array([0,ymax]),'--k',label="95% quantile")
plt.title("Empirical CDF of parameter relative error",fontsize=20)
plt.legend(fontsize=17)
plt.xlabel("quantiles",fontsize=17)
plt.ylabel("relative error",fontsize=17)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter() )
plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter() )
plt.tick_params(axis='both', which='major', labelsize=17)
plt.tick_params(axis='both', which='minor', labelsize=17)
plt.xticks(np.arange(0, 101, step=10))

plt.grid()
plt.subplot(122)


ax = plt.gca()
q=np.linspace(0,1,200)
p=plt.plot(100*q,np.quantile(100*RMSE_opt,q),linewidth=3,label="RMSE")
ymin, ymax = ax.get_ylim()
plt.plot(100*np.ones(2)*0.99,np.array([0,ymax]),'--k',label="99% quantile")
plt.title("Empirical CDF of implied vol surface RMSE",fontsize=20)
plt.legend(fontsize=17)
plt.xlabel("quantiles",fontsize=17)
plt.ylabel("RMSE",fontsize=17)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter() )
plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter() )
plt.tick_params(axis='both', which='major', labelsize=17)
plt.tick_params(axis='both', which='minor', labelsize=17)
plt.xticks(np.arange(0, 101, step=10))
plt.grid()
plt.tight_layout()
plt.savefig('HNG_ErrorCDF.png', dpi=300)
plt.show()

#==============================================================================
#real data
sp500_mat = scipy.io.loadmat('surface_sp500_new.mat')
surface = sp500_mat['vector_surface']
surface_trafo = ytransform(surface,surface,surface)[2]
def CostFuncLS_real(x):
    return (yinversetransform(NN1.predict(x.reshape(1,Nparameters))[0])-surface_trafo).T.flatten()
def JacobianLS_real(x):
    return NeuralNetworkGradient(x).T

solutions=np.zeros([1,Nparameters])
init=np.zeros(Nparameters)

#Levenberg-Marquardt
I=scipy.optimize.least_squares(CostFuncLS_real, init, JacobianLS_real, gtol=1E-10)
LMParameters_real=myinverse(I.x)
Y_pred_real = yinversetransform(NN1.predict(myscale(LMParameters_real).reshape(1,Nparameters))[0])
RMSE_opt_real = np.sqrt(np.mean((surface-Y_pred_real)**2))
err_real_mean = np.mean(100*np.abs((surface-Y_pred_real)/surface),axis = 1)
err_real = (100*np.abs((surface-Y_pred_real)/surface)).reshape((Nmaturities, Nstrikes))
diff = (Y_pred_real - surface).reshape((Nmaturities, Nstrikes))
np.savetxt("SP500_pred_NN.txt",Y_pred_real)