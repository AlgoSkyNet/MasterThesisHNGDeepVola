# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 08:41:27 2019

@author: Henrik Brautmeier

Option Pricing in Maschine Learning
"""
# preambel
#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import hngoption as hng
from help_fun import HNG_MC,HNG_MC_simul

#model parameters 
# Szenario Analyse
#=============================================================================
dt =1
sz_alpha = [0.01,0.02]
sz_gamma = [0.2,0.3]
sz_beta = [0.2,0.5]
sz_lambda = [-0.5,1.3]
sz_omega =[0.1,0.2]
Maturity = np.array([10,20,30,40,50,60])
sz_S0  = [1] #normalization
#sz_rate = [-0.02/252,-0.1/252,0,0.1/252,0.2/252,0.05/252]
szenario_vola_calls ={}
szenario_data =[]
Moneyness = np.array([0.9,0.925,0.95,0.975,1,1.025,1.05,1.075,1.1])

K = Moneyness
S = 1
r = 0
d_lambda = 0
for alpha in sz_alpha:
    for beta in sz_beta:
        for gamma_star in sz_gamma:       
            #for d_lambda in sz_lambda:
            #    gamma_star = gamma+d_lambda+0.5          _             
            for omega in sz_omega:                         
                #for T in sz_maturity: #eventuell unnötig langer pfad modellieren und kürzen?!                            
                    #for S_0 in sz_S0:
                    #    K = Moneyness*S_0
                                        #for r in sz_rate:        
                vola = HNG_MC_simul(alpha, beta, gamma_star, omega, d_lambda, S, K, r, Maturity, dt, output=0)
                #szenario_vola_calls[(alpha,beta,gamma_star,omega)] =  vola.reshape((1,vola.shape[0]*vola.shape[1]))
                szenario_data.append(np.concatenate((np.asarray([alpha,beta,gamma_star,omega]).reshape((1,4)),vola.reshape((1,vola.shape[0]*vola.shape[1]))),axis=1))
                break     
# #===========================================================================
#  
#  dt = 1                                          #Zeitschritt                        
#  alpha = 0.01    
#  beta = 0.2
#  d_lambda = 1.4                                  #real world
#  d_lambda_star = -0.5                            #risk-free 
#  gamma = 0.2                                     #real world
#  gamma_star = gamma+d_lambda+0.5                 #risk-free  
#  omega = 0.1                                     #intercept       
#  PutCall = 1
#  S=1
#  r=0.03/252
#  K=np.array([17,40,50])/30
#  T = 20
#  sigma2 = (omega+alpha)/(1-alpha*gamma_star**2-beta)          #unconditional variance VGARCH
#  V = sigma2
#  
#  #price_rn= hng.HNC(alpha, beta, gamma_star, omega, d_lambda_star, V, S, K, r, T, PutCall) #V= inital sigma2
#  from help_fun import HNG_MC_simul
#  T=np.array([10,20])
#  price_MC_rn = HNG_MC_simul(alpha,beta,gamma_star,omega,d_lambda,S,K,r,T,dt)
#  vola = HNG_MC_simul(alpha, beta, gamma_star, omega, d_lambda, S, K, r, T, dt, output=0)
#    
#  print(price_rn,price_MC_rn)
#  print((price_rn-price_MC_rn)/price_rn*100)
#  #price_p = hng.HNC(alpha, beta, gamma, omega, d_lambda, V, S, K, r, T, PutCall)
#  #price_MC_p = HNG_MC(alpha,beta,gamma,omega,d_lambda,S,K,r,T,PutCall,risk_neutral =False)
#  
# # =============================================================================
