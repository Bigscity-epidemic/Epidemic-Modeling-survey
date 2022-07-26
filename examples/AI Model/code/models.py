import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv


import networkx as nx
import numpy as np
import scipy.sparse as sp


from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler

from fbprophet import Prophet
from statsmodels.tsa.arima_model import ARIMA

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
hiddenimports = collect_submodules('fbprophet')
datas = collect_data_files('fbprophet')



            
def arima(ahead,start_exp,n_samples,labels):
    var = []
    for idx in range(ahead):
        var.append([])

    error= np.zeros(ahead)
    count = 0
    for test_sample in range(start_exp,n_samples-ahead):#
        print(test_sample)
        count+=1
        err = 0
        for j in range(labels.shape[0]):
            ds = labels.iloc[j,:test_sample-1].reset_index()

            if(sum(ds.iloc[:,1])==0):
                yhat = [0]*(ahead)
            else:
                try:
                    fit2 = ARIMA(ds.iloc[:,1].values, (2, 0, 2)).fit()
                except:
                    fit2 = ARIMA(ds.iloc[:,1].values, (1, 0, 0)).fit()
                #yhat = abs(fit2.predict(start = test_sample , end = (test_sample+ahead-1) ))
                yhat = abs(fit2.predict(start = test_sample , end = (test_sample+ahead-2) ))
            y_me = labels.iloc[j,test_sample:test_sample+ahead]
            e =  abs(yhat - y_me.values)
            err += e
            error += e

        for idx in range(ahead):
            var[idx].append(err[idx])
    return error, var



def prophet(ahead, start_exp, n_samples, labels):
    var = []
    for idx in range(ahead):
        var.append([])

    error= np.zeros(ahead)
    count = 0
    for test_sample in range(start_exp,n_samples-ahead):#
        print(test_sample)
        count+=1
        err = 0
        for j in range(labels.shape[0]):
            ds = labels.iloc[j,:test_sample].reset_index()
            ds.columns = ["ds","y"]
            #with suppress_stdout_stderr():
            m = Prophet(interval_width=0.95)
            m.fit(ds)
            future = m.predict(m.make_future_dataframe(periods=ahead))
            yhat = future["yhat"].tail(ahead)
            y_me = labels.iloc[j,test_sample:test_sample+ahead]
            e =  abs(yhat-y_me.values).values
            err += e
            error += e
        for idx in range(ahead):
            var[idx].append(err[idx])
            
    return error, var
            
            

class LSTM(nn.Module):
    def __init__(self, nfeat, nhid, n_nodes, window, dropout,batch_size, recur):
        super().__init__()
        self.nhid = nhid
        self.n_nodes = n_nodes
        self.nout = n_nodes
        self.window = window
        self.nb_layers= 2
        
        self.nfeat = nfeat 
        self.recur = recur
        self.batch_size = batch_size
        self.lstm = nn.LSTM(nfeat, self.nhid, num_layers=self.nb_layers)
    
        self.linear = nn.Linear(nhid, self.nout)
        self.cell = ( nn.Parameter(nn.init.xavier_uniform(torch.Tensor(self.nb_layers, self.batch_size, self.nhid).type(torch.FloatTensor).cuda()),requires_grad=True))
      
        #self.hidden_cell = (torch.zeros(2,self.batch_size,self.nhid).to(device),torch.zeros(2,self.batch_size,self.nhid).to(device))
        #nn.Parameter(nn.init.xavier_uniform(torch.Tensor(self.nb_layers, self.batch_size, self.nhid).type(torch.FloatTensor).cuda()),requires_grad=True))
        
        
    def forward(self, adj, features):
        #adj is 0 here
        #print(features.shape)
        features = features.view(self.window,-1, self.n_nodes)#.view(-1, self.window, self.n_nodes, self.nfeat)
        #print(features.shape)
        #print("----")
        
        
        #------------------
        if(self.recur):
            #print(features.shape)
            #self.hidden_cell = 
            try:
                lstm_out, (hc,self.cell) = self.lstm(features,(torch.zeros(self.nb_layers,self.batch_size,self.nhid).cuda(),self.cell)) 
                # = (hc,cn)
            except:
                #hc = self.hidden_cell[0][:,0:features.shape[1],:].contiguous().view(2,features.shape[1],self.nhid)
                hc = torch.zeros(self.nb_layers,features.shape[1],self.nhid).cuda()                 
                cn = self.cell[:,0:features.shape[1],:].contiguous().view(2,features.shape[1],self.nhid)
                lstm_out, (hc,cn) = self.lstm(features,(hc,cn)) 
        else:
        #------------------
            lstm_out, (hc,cn) = self.lstm(features)#, self.hidden_cell)#self.hidden_cell 
            
        predictions = self.linear(lstm_out)#.view(self.window,-1,self.n_nodes)#.view(self.batch_size,self.nhid))#)
        #print(predictions.shape)
        return predictions[-1].view(-1)
