import numpy as np
import pandas as pd
import utils

class con1:
    def __init__(self, ID, fc1, length, epsilon_t2 = 0.001, fc2_factor = 0.1, ft_factor = 1, characteristic = True):
        self.resid_str = fc2_factor
        self.ID = ID
        self.fc1 = round(fc1, 1)
        self.fc2 = round(self.resid_str * fc1, 1)
        self.length = length
        if characteristic:
            self.fcm = round(fc1+8,2)
        else:
            self.fcm = fc1
        if fc1 <= 50:
            self.ft = round(ft_factor * 0.3 * self.fcm ** (2/3), 1)
        else:
            self.ft = round(ft_factor * 2.12*np.log(1+0.1*self.fcm), 1)
        self.Gf = round(73 * self.fcm**0.18/1000, 3)
        self.Ec0 = round(int(21500*(self.fcm/10)**(1/3)),-2)
        self.poisson = 0.2
        self.Gc = round(250 * self.Gf, 1)
        self.epsilon_1c = round(5 * fc1 / self.Ec0 /3, 4)
        self.Ec1 = int(round(fc1 / self.epsilon_1c, -2))
        self.alpha = min(max(0,round((self.Ec0 - self.Ec1)/self.Ec1,2)),1)
        self.epsilon_2c = round(self.epsilon_1c + 3 * self.Gc / (2 * length * fc1), 4)
        self.Ec2 = - int(round((1 - self.resid_str) * fc1 /(self.epsilon_2c - self.epsilon_1c), -2))
        self.Et1 = self.Ec0
        self.epsilon_1t = round(self.ft / self.Et1, 5)
        self.epsilon_2t = epsilon_t2
        self.Et2 = - int(round(self.ft /(self.epsilon_2t - self.epsilon_1t), -2))
        
    def adaptic_print(self):
        line = utils.str_joint([self.ID,'con1', self.Ec1, self.fc1, self.Ec2, self.fc2, self.Et1, 
                                      self.ft, self.Et2, self.alpha])
        return line
        
    def data_frame(self):
        data = np.array([[self.ID, self.length, self.fc1, self.fc2, self.ft, self.Ec0, self.Ec1, 
                          self.Ec2, self.Et1, self.Et2, self.Gf, self.Gc, self.epsilon_1c, 
                          self.epsilon_2c, self.epsilon_1t, self.epsilon_2t,  self.alpha]])
        df = pd.DataFrame(data,index=data[:,0])
        df.columns = ['ID', '$$h[mm]$$', '$$f_{c1}[MPa]$$','$$f_{c2}[MPa]$$', '$$f_{t}[MPa]$$',
                      '$$E_{c0}[MPa]$$','$$E_{c1}[MPa]$$','$$E_{c2}[MPa]$$','$$E_{t1}[MPa]$$',
                      '$$E_{t2}[MPa]$$','$$G_{f}[N/mm]$$','$$G_{c}[N/mm]$$','$$e_{c1}$$', 
                      '$$e_{c2}$$','$$e_{t1}$$', '$$e_{t2}$$', '$$alpha$$']
        return df


class stl1:
    def __init__(self, ID, E1, fy, fu, epsilon_u):
        self.ID = ID
        self.E1 = E1
        self.fy = fy
        self.fu = fu
        self.epsilon_u = round(epsilon_u,3)
        self.epsilon_y = round(fy / E1,4)
        self.E2 = round((fu - fy) / (epsilon_u - self.epsilon_y),1)
        self.mu = round(self.E2 / E1,7)
        
    def adaptic_print(self):
        line = utils.str_joint([self.ID,'stl1', self.E1, self.fy, self.mu])
        return line
        
    def data_frame(self):
        data = np.array([[self.ID, self.E1, self.E2, self.fy, self.fu, self.epsilon_y, self.epsilon_u, 
                          self.mu]])
        df = pd.DataFrame(data,index=data[:,0])
        df.columns = ['ID', '$$E_{1}[MPa]$$', '$$E_{2}[MPa]$$', '$$f_{y}[MPa]$$', '$$f_{u}[MPa]$$',
                      '$$e_{y}$$','$$e_{u}$$','$$mu$$']
        return df
    
    def stress_df(self):
        df = pd.DataFrame([[0,0],[self.epsilon_y,self.fy],[self.epsilon_u,self.fu]],columns=['strain','stress'])
        return df