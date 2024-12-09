import torch
import pandas as pd
from mamba_ssm import Mamba
from RevIN.RevIN import RevIN
import torch.nn.functional as F

class moving_avg(torch.nn.Module):
    """
    Moving average block to highlight the trend of time series
    """
    def __init__(self, kernel_size, stride):
        super(moving_avg, self).__init__()
        self.kernel_size = kernel_size
        self.avg = torch.nn.AvgPool1d(kernel_size=kernel_size, stride=stride, padding=0)

    def forward(self, x):
        # padding on the both ends of time series
        front = x[:, 0:1, :].repeat(1, (self.kernel_size - 1) // 2, 1)
        end = x[:, -1:, :].repeat(1, (self.kernel_size - 1) // 2, 1)
        x = torch.cat([front, x, end], dim=1)
        x = self.avg(x.permute(0, 2, 1))
        x = x.permute(0, 2, 1)
        return x
        

class series_decomp(torch.nn.Module):
    """
    Series decomposition block
    """
    def __init__(self, kernel_size):
        super(series_decomp, self).__init__()
        self.moving_avg = moving_avg(kernel_size, stride=1)

    def forward(self, x):
        moving_mean = self.moving_avg(x)
        res = x - moving_mean
        return res, moving_mean


class Model(torch.nn.Module):
    def __init__(self,configs):
        super(Model, self).__init__()
        self.configs=configs
        if self.configs.include_pred==1:
            self.configs.enc_in = self.configs.enc_in+10
            self.lin1=torch.nn.Linear(2*(self.configs.seq_len+self.configs.pred_len),self.configs.seq_len)
            
        kernel_size = self.configs.kernel_size
        self.decompsition = series_decomp(kernel_size)
        
        self.revin_layer = RevIN(self.configs.enc_in)
        self.revin_layer_enc = RevIN(self.configs.enc_in)

        self.lin2=torch.nn.Linear(2*(self.configs.seq_len),self.configs.n_embed)
        self.lin3=torch.nn.Linear(4*self.configs.n_embed,self.configs.pred_len)
        
        self.dropout1=torch.nn.Dropout(self.configs.dropout)
        self.dropout2=torch.nn.Dropout(self.configs.dropout)

        self.mamba1 = Mamba(d_model=self.configs.n_embed,d_state=self.configs.d_state,d_conv=self.configs.dconv,
                            expand = self.configs.e_fact)
        self.mamba2 = Mamba(d_model=self.configs.enc_in,d_state=self.configs.d_state,d_conv=self.configs.dconv,
                            expand = self.configs.e_fact)

        self.df_dict = self.configs.project_dict

    def forward(self, x):

        if self.configs.include_pred==1:
            zeros = x[:, -self.configs.pred_len:, :]
            x_pred = torch.cat((x, zeros), dim=1)
            k=0
            for key, value in self.df_dict.items():
                k=k+1
                proj_to = value[0]-1 
                proj_from = value[1]-1 
                x_slice_2 = x[:, -1, proj_from:proj_from + self.configs.pred_len]
                x_pred[:, -self.configs.pred_len:, proj_to] = x_slice_2
                x_pred[:, :self.configs.seq_len, 241-k]=x_pred[:, -self.configs.seq_len:, proj_to]
                x_pred[:, -self.configs.pred_len:, 241-k]=x_slice_2

            x = x_pred[: , : , -self.configs.n_nonpred_col-10:]
            x = self.revin_layer_enc(x, 'norm')
            seasonal_init, trend_init = self.decompsition(x)
            x= torch.cat([seasonal_init, trend_init], dim=1)
            x = torch.permute(x, (0,2,1))
            x = self.lin1(x)
            x = torch.permute(x, (0,2,1))
            x = self.revin_layer_enc(x, 'denorm')
        
        x = self.revin_layer(x, 'norm')
        seasonal_init, trend_init = self.decompsition(x)
        xout= torch.cat([seasonal_init, trend_init], dim=1)
        xout = torch.permute(xout, (0,2,1))
        xout = self.lin2(xout)
        
        x1 = self.dropout1(xout)
        x1 = self.mamba1(x1)

        x2 = self.dropout2(xout)
        x2 = torch.permute(x2, (0,2,1))
        x2 = self.mamba2(x2)
        x2 = torch.permute(x2, (0,2,1))

        x = torch.cat([x2, x1, x1+x2, xout], dim=2)
        
        x = self.lin3(x)
        
        x = torch.permute(x, (0,2,1))
        x = self.revin_layer(x, 'denorm')

        return x