# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 11:22:35 2015

@author: jmmauricio
"""


import numpy as np
import xlrd
import pandas as pd

def losses(i_rms, m, fp, T_a, params):

    a_i = params['a_i']
    b_i = params['b_i']
    c_i = params['c_i']
    d_i = params['d_i']
    e_i = params['e_i']
    a_d = params['a_d']
    b_d = params['b_d']
    c_d = params['c_d']
    d_d = params['d_d']
    e_d = params['e_d']

    R_th_igbt =params['R_th_igbt']
    R_th_diode=params['R_th_diode']
    R_th_igbt_case=params['R_th_igbt_case']
    R_th_diode_case=params['R_th_diode_case']
    R_th_sink =params['R_th_sink']
    
    
    p_igbt  = a_i + (b_i - c_i*m*fp)*i_rms + (d_i - e_i*m*fp)*i_rms*i_rms
    p_diode = a_d + (b_d - c_d*m*fp)*i_rms + (d_d - e_d*m*fp)*i_rms*i_rms
    
    p_switch = p_igbt + p_diode
    
    T_sink       = T_a          + p_switch*R_th_sink;
    T_case_igbt  = T_sink       + p_igbt *R_th_igbt_case; 
    T_case_diode = T_sink       + p_diode*R_th_diode_case;
    T_igbt       = T_case_igbt  + p_igbt *R_th_igbt;
    T_diode      = T_case_diode + p_diode*R_th_diode;
    
    #print(R_th_igbt,R_th_igbt_case,T_case_igbt,T_sink)
    
    powers = dict(p_igbt=p_igbt,
                  p_diode=p_diode)
                  
    temperatures = dict(T_igbt=T_igbt,
                        T_diode=T_diode,
                        T_case_igbt=T_case_igbt,
                        T_case_diode=T_case_diode,
                        T_sink=T_sink,
                        T_igbt_deg=T_igbt-273.15,
                        T_diode_deg=T_diode-273.15,
                        T_sink_deg=T_sink-273.15)    
                        
    return powers, temperatures 
  
def vscthmodel(i_rms, m, fp, T_a, params):

    a_i = params['a_i']
    b_i = params['b_i']
    c_i = params['c_i']
    d_i = params['d_i']
    e_i = params['e_i']
    a_d = params['a_d']
    b_d = params['b_d']
    c_d = params['c_d']
    d_d = params['d_d']
    e_d = params['e_d']


    R_th_igbt_sink=params['R_th_igbt_sink']
    R_th_diode_sink=params['R_th_diode_sink']
    R_th_sink_a =params['R_th_sink_a']
    
    
    p_igbt  = a_i + (b_i - c_i*m*fp)*i_rms + (d_i - e_i*m*fp)*i_rms*i_rms
    p_diode = a_d + (b_d - c_d*m*fp)*i_rms + (d_d - e_d*m*fp)*i_rms*i_rms
    
    p_switch = p_igbt + p_diode
    
    T_sink       = T_a          + p_switch*R_th_sink_a;
    T_igbt  = T_sink       + p_igbt *R_th_igbt_sink; 
    T_diode = T_sink       + p_diode*R_th_diode_sink;

    
    #print(R_th_igbt,R_th_igbt_case,T_case_igbt,T_sink)
    
    powers = dict(p_igbt=p_igbt,
                  p_diode=p_diode)
                  
    temperatures = dict(T_igbt=T_igbt,
                        T_diode=T_diode,
                        T_sink=T_sink,
                        T_igbt_deg=T_igbt-273.15,
                        T_diode_deg=T_diode-273.15,
                        T_sink_deg=T_sink-273.15)    
                        
    return powers, temperatures   

def man2param(man_electric, man_thermal={}):
    '''
    
    Input
    -----
    
    List of 5 tuples
    
   [
   [i_1,m_1,cosphi_1,p_igbt_1,p_diode_1],
   [i_2,m_1,cosphi_1,p_igbt_2,p_diode_2],
   [i_3,m_1,cosphi_1,p_igbt_3,p_diode_3],
   [i_4,m_2,cosphi_2,p_igbt_4,p_diode_4],
   [i_5,m_2,cosphi_2,p_igbt_5,p_diode_5]
   ]

    '''
    
    if type(man_electric)==list:
        man_electric = [[0]*5]*5

    if type(man_electric)==dict:
        d = man_electric       
        
    k2deg = 273.15
    
    i_1 = man_electric['i_1']
    i_2 = man_electric['i_2']
    i_3 = man_electric['i_3']
    i_4 = man_electric['i_4']
    i_5 = man_electric['i_5']
    
    
    p_igbt_1 = man_electric['p_igbt_1']
    p_igbt_2 = man_electric['p_igbt_2']
    p_igbt_3 = man_electric['p_igbt_3']
    p_igbt_4 = man_electric['p_igbt_4']
    p_igbt_5 = man_electric['p_igbt_5']
    
    p_diode_1 = man_electric['p_diode_1']
    p_diode_2 = man_electric['p_diode_2']
    p_diode_3 = man_electric['p_diode_3']
    p_diode_4 = man_electric['p_diode_4']
    p_diode_5 = man_electric['p_diode_5']
    
    m_1 = man_electric['m_1']
    m_2 = man_electric['m_2']
    m_3 = man_electric['m_3']
    m_4 = man_electric['m_4']
    m_5 = man_electric['m_5']
    
    cosphi_1 = man_electric['cosphi_1']
    cosphi_2 = man_electric['cosphi_2']
    cosphi_3 = man_electric['cosphi_3'] 
    cosphi_4 = man_electric['cosphi_4'] 
    cosphi_5 = man_electric['cosphi_5'] 
     
    alpha_1 = m_1*cosphi_1 
    alpha_2 = m_2*cosphi_2 
    alpha_3 = m_3*cosphi_3 
    alpha_4 = m_4*cosphi_4
    alpha_5 = m_5*cosphi_5
        
    A = np.array(
    [
    [1,  i_1,  -i_1*alpha_1,  i_1**2, -i_1**2*alpha_1],
    [1,  i_2,  -i_2*alpha_2,  i_2**2, -i_2**2*alpha_2],
    [1,  i_3,  -i_3*alpha_3,  i_3**2, -i_3**2*alpha_3],
    [1,  i_4,  -i_4*alpha_4,  i_4**2, -i_4**2*alpha_4],
    [1,  i_5,  -i_5*alpha_5,  i_5**2, -i_5**2*alpha_5]
    ]
    )
    
    b_igbt = np.array(
    [
    [p_igbt_1],
    [p_igbt_2],
    [p_igbt_3],
    [p_igbt_4],
    [p_igbt_5]
    ]
    ) 
    
       
    x = np.linalg.solve(A, b_igbt)
    
    a_i  = x[0]
    b_i = x[1]
    c_i = x[2]
    d_i = x[3]
    e_i = x[4]
        
    b_diode = np.array(
    [
    [p_diode_1],
    [p_diode_2],
    [p_diode_3],
    [p_diode_4],
    [p_diode_5]
    ]
    )     
    
    x = np.linalg.solve(A, b_diode)
    
    a_d  = x[0]
    b_d = x[1]
    c_d = x[2]
    d_d = x[3]
    e_d = x[4]
    
    
    points=[
            [1, i_1,m_1,cosphi_1,alpha_1,p_igbt_1,p_diode_1],
            [2, i_2,m_2,cosphi_2,alpha_2,p_igbt_2,p_diode_2],
            [3, i_3,m_3,cosphi_3,alpha_3,p_igbt_3,p_diode_3],
            [4, i_4,m_4,cosphi_4,alpha_4,p_igbt_4,p_diode_4],
            [5, i_5,m_5,cosphi_5,alpha_5,p_igbt_5,p_diode_5]
            ]

    params = dict(
    a_i = a_i,
    b_i = b_i,
    c_i = c_i,
    d_i = d_i,
    e_i = e_i,
    a_d = a_d,
    b_d = b_d,
    c_d = c_d,
    d_d = d_d,
    e_d = e_d 
    )
    
    
    if not man_thermal == {}:

        # man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a+k2deg]]
        
        if type(man_thermal) == list:
            idx = 0
            p_igbt   = man_thermal[idx][0]
            p_diode  = man_thermal[idx][1]
            
            T_igbt   = man_thermal[idx][2]
            T_diode  = man_thermal[idx][3]
            T_sink   = man_thermal[idx][4]
            T_a      = man_thermal[idx][5]
            
        if type(man_thermal) == dict:
            idx = 0
            p_igbt   = man_thermal['p_igbt']
            p_diode  = man_thermal['p_diode']
            
            T_igbt   = man_thermal['T_igbt']
            T_diode  = man_thermal['T_diode']
            T_sink   = man_thermal['T_sink']
            T_a      = man_thermal['T_a']     
            

        p_switch = p_igbt + p_diode   
        
        R_th_igbt_sink = (T_igbt-T_sink)/p_igbt
        
        R_th_sink_a = (T_sink-(T_a))/p_switch
        
        R_th_diode_sink = (T_diode-T_sink)/p_diode
        
    #    print(tabulate(points,tablefmt='latex'))
        
        params.update = dict(
        R_th_igbt_sink = R_th_igbt_sink,
        R_th_diode_sink = R_th_diode_sink,    
        R_th_sink_a = R_th_sink_a,   
        )

        if 'tau_sink' in man_thermal:
            tau_sink = man_thermal['tau_sink']
            # tau_sink = C_sink * R_th_sink_a => C_sink = tau_sink/R_th_sink_a
            C_sink = tau_sink/R_th_sink_a
            params.update({'C_sink':C_sink})
            
            
    return params 
  


def semisel_xls(file,shs_for_param, shs_for_validate, T_a_deg):
    k2deg = 273.15
    
    wb = xlrd.open_workbook(file)
    man_electric = []
    man_thermal  = []
      
    for sh_num in shs_for_param:        
        sh = wb.sheet_by_index(sh_num)
        
        V_dc  = float(sh.cell_value(0,1).split(' ')[0])
        V_ac  = float(sh.cell_value(1,1).split(' ')[0])
        i_rms = float(sh.cell_value(2,1).split(' ')[0])
        freq  = float(sh.cell_value(4,1).split(' ')[0])
        fp    = float(sh.cell_value(5,1))
        f_sw  = float(sh.cell_value(7,1).split(' ')[0])
        
        p_igbt  = float(sh.cell_value(15,1).split(' ')[0])
        p_diode = float(sh.cell_value(18,1).split(' ')[0])
        T_igbt  = float(sh.cell_value(23,1).split(' ')[0])        
        T_diode = float(sh.cell_value(24,1).split(' ')[0])
        T_sink= float(sh.cell_value(21,1).split(' ')[0])
        
        m = V_ac*np.sqrt(2)/V_dc
        
        man_electric += [[i_rms,m,fp,p_igbt,p_diode]]
        man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a_deg+k2deg]]
        
        print('{} & {} & {} & {} & {} & {} & {}'.format(i_rms, fp, p_igbt, p_diode, T_igbt, T_diode, T_sink))

    params = man2param(man_electric,man_thermal)

    
    print('\midrule')
    for sh_num in shs_for_validate:        
        sh = wb.sheet_by_index(sh_num)
        
        V_dc  = float(sh.cell_value(0,1).split(' ')[0])
        V_ac  = float(sh.cell_value(1,1).split(' ')[0])
        i_rms = float(sh.cell_value(2,1).split(' ')[0])
        freq  = float(sh.cell_value(4,1).split(' ')[0])
        fp    = float(sh.cell_value(5,1))
        f_sw  = float(sh.cell_value(7,1).split(' ')[0])
        
        p_igbt  = float(sh.cell_value(15,1).split(' ')[0])
        p_diode = float(sh.cell_value(18,1).split(' ')[0])
        T_igbt  = float(sh.cell_value(23,1).split(' ')[0])        
        T_diode = float(sh.cell_value(24,1).split(' ')[0])
        T_sink= float(sh.cell_value(21,1).split(' ')[0])
        
        m = V_ac*np.sqrt(2)/V_dc
        
        pows, temps    = vscthmodel(i_rms, m, fp, T_a_deg, params)


        print('{:2.1f} & {:2.2f} & {:2.1f} & {:2.1f}  & {:2.1f} & {:2.1f}   & {:2.1f} & {:2.1f}  & {:2.1f} & {:2.1f}   & {:2.1f} & {:2.1f} \\\\  '.format(i_rms, 
                                                                                                          fp,
                                                                                                          p_igbt, pows['p_igbt'][0], 
                                                                                                          p_diode, pows['p_diode'][0], 
                                                                                                          T_igbt, temps['T_igbt_deg'][0],
                                                                                                          T_diode, temps['T_diode_deg'][0],
                                                                                                          T_sink, temps['T_sink_deg'][0],



))
        
        
    
    return params
    
  

def imposim_xls(file):
    k2deg = 273.15
    
    wb = xlrd.open_workbook(file)
    man_electric = []
    man_thermal  = []
     
           
    sh = wb.sheet_by_index(0)
    
    V_dc  = float(sh.cell_value(20,3))
    m     = float(sh.cell_value(26,3))

    idx = 9  
    
    T_a_deg = float(sh.cell_value(idx+53,9))  
    
    i_rms   = float(sh.cell_value(idx,0))
    m       = float(sh.cell_value(26,3))
    fp      = float(sh.cell_value(27,3))  
    p_igbt  = float(sh.cell_value(idx,6))+ 0.5*float(sh.cell_value(idx,13))  
    p_diode = float(sh.cell_value(idx,11)) + 0.5*float(sh.cell_value(idx,13))  
    T_igbt  = float(sh.cell_value(idx+34,10))
    T_diode = float(sh.cell_value(idx+52,10))   
    T_sink = float(sh.cell_value(idx+52,8)) + float(sh.cell_value(idx+53,9)) 
    man_electric += [[i_rms,m,fp,p_igbt,p_diode]]
    man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a_deg+k2deg]]
    print('{:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} \\\\'.format(i_rms, fp, p_igbt, p_diode, T_igbt, T_diode, T_sink))
    
    idx = 13  
    i_rms   = float(sh.cell_value(idx,0))
    m       = float(sh.cell_value(26,3))
    fp      = float(sh.cell_value(27,3))  
    p_igbt  = float(sh.cell_value(idx,6))+ 0.5*float(sh.cell_value(idx,13))  
    p_diode = float(sh.cell_value(idx,11))+ 0.5*float(sh.cell_value(idx,13))  
    T_igbt  = float(sh.cell_value(idx+34,10))
    T_diode = float(sh.cell_value(idx+52,10))   
    T_sink = float(sh.cell_value(idx+52,8)) + float(sh.cell_value(idx+53,9))   
    man_electric += [[i_rms,m,fp,p_igbt,p_diode]]    
    man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a_deg+k2deg]]
    print('{:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} \\\\'.format(i_rms, fp, p_igbt, p_diode, T_igbt, T_diode, T_sink))

 
    idx = 16  
    i_rms   = float(sh.cell_value(idx,0))
    m       = float(sh.cell_value(26,3))
    fp      = float(sh.cell_value(27,3))  
    p_igbt  = float(sh.cell_value(idx,6)) + 0.5*float(sh.cell_value(idx,13))  
    p_diode = float(sh.cell_value(idx,11))  + 0.5*float(sh.cell_value(idx,13))  
    T_igbt  = float(sh.cell_value(idx+34,10))
    T_diode = float(sh.cell_value(idx+52,10))   
    T_sink = float(sh.cell_value(idx+52,8)) + float(sh.cell_value(idx+53,9))    
    man_electric += [[i_rms,m,fp,p_igbt,p_diode]] 
    man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a_deg+k2deg]]
    print('{:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} \\\\'.format(i_rms, fp, p_igbt, p_diode, T_igbt, T_diode, T_sink))
        
    sh = wb.sheet_by_index(1)
    m     = float(sh.cell_value(26,3))
       
    idx = 13  
    i_rms   = float(sh.cell_value(idx,0))
    m       = float(sh.cell_value(26,3))
    fp      = float(sh.cell_value(27,3))  
    p_igbt  = float(sh.cell_value(idx,6))    + 0.5*float(sh.cell_value(idx,13))  
    p_diode = float(sh.cell_value(idx,11))   + 0.5*float(sh.cell_value(idx,13))  
    T_igbt  = float(sh.cell_value(idx+34,10))
    T_diode = float(sh.cell_value(idx+52,10))   
    T_sink = float(sh.cell_value(idx+52,8)) + float(sh.cell_value(idx+53,9))
    man_electric += [[i_rms,m,fp,p_igbt,p_diode]]    
    man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a_deg+k2deg]]
    print('{:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} \\\\'.format(i_rms, fp, p_igbt, p_diode, T_igbt, T_diode, T_sink))

    idx = 16  
    i_rms   = float(sh.cell_value(idx,0))
    m       = float(sh.cell_value(26,3))
    fp      = float(sh.cell_value(27,3))  
    p_igbt  = float(sh.cell_value(idx,6)) + 0.5*float(sh.cell_value(idx,13))  
    p_diode = float(sh.cell_value(idx,11)) + 0.5*float(sh.cell_value(idx,13))  
    T_igbt  = float(sh.cell_value(idx+34,10))
    T_diode = float(sh.cell_value(idx+52,10))   
    T_sink = float(sh.cell_value(idx+52,8)) + float(sh.cell_value(idx+53,9))
    man_electric += [[i_rms,m,fp,p_igbt,p_diode]] 
    man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a_deg+k2deg]]
    print('{:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} \\\\'.format(i_rms, fp, p_igbt, p_diode, T_igbt, T_diode, T_sink))
    
    
    print(np.array(man_electric))
    params = man2param(man_electric,man_thermal)

def imposim2xls(file):
    k2deg = 273.15
    
    df_1 = pd.read_excel(file, sheetname=0, skiprows=8)
    df_2 = pd.read_excel(file, sheetname=1, skiprows=8)
    print(df_1)

    idx1 = 3
    idx2 = 10
    idx3 = 16
    
    man_electric = [
                   [df_1.i_rms[idx1],df_1.m[idx1],df_1.fp[idx1],df_1.p_igbt[idx1],df_1.p_diode[idx1]],
                   [df_1.i_rms[idx2],df_1.m[idx2],df_1.fp[idx2],df_1.p_igbt[idx2],df_1.p_diode[idx2]],
                   [df_1.i_rms[idx3],df_1.m[idx3],df_1.fp[idx3],df_1.p_igbt[idx3],df_1.p_diode[idx3]],
                   [df_2.i_rms[idx2],df_2.m[idx2],df_2.fp[idx2],df_2.p_igbt[idx2],df_2.p_diode[idx2]],
                   [df_2.i_rms[idx3],df_2.m[idx3],df_2.fp[idx3],df_2.p_igbt[idx3],df_2.p_diode[idx3]],
                   ]    
                    
    man_thermal = [
                  [df_1.p_igbt[idx2],df_1.p_diode[idx2],df_1.T_igbt[idx2]+k2deg,df_1.T_diode[idx2]+k2deg,df_1.T_sink[idx2]+k2deg,df_1.T_a[idx2]+k2deg],
                  ]
    
    params =  man2param(man_electric, man_thermal)
    
    return params
    
    
    
    
if __name__ == '__main__':
    k2deg = 273.15
    
    man_electric = {
            'i_1':1400 ,'m_1':0.8 , 'cosphi_1':0.8,'p_igbt_1':3570 ,'p_diode_1':1046 ,
            'i_2':1000 ,'m_2':0.8 , 'cosphi_2':0.2,'p_igbt_2':1952 ,'p_diode_2': 931 ,
            'i_3':1300 ,'m_3':0.8 , 'cosphi_3':0.2,'p_igbt_3':2772 ,'p_diode_3':1252 ,
            'i_4':1000 ,'m_4':0.1 , 'cosphi_4':0.2,'p_igbt_4':1882 ,'p_diode_4': 987 ,
            'i_5':1500 ,'m_5':0.85, 'cosphi_5':0.5,'p_igbt_5':3749 ,'p_diode_5':1293 ,
            }    
 
    man_thermal = {
            'p_igbt':3570 ,'p_diode':1046 , 'T_igbt':125 , 'T_diode':97 , 'T_sink':57.3, 'T_a':40.0}


    params = man2param(man_electric,man_thermal)
    print(vscthmodel(1000, 0.8, 0.2, 40.0+273.15, params))
    print(vscthmodel(np.arange(100,1500,100), 0.8, 0.2, 40.0+273.15, params))
        
#    file = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/ARTICLES/doing/vsc_model/code/semikron_100kva/semikron_SKiiP38GB12E4V1.xls'
##    shs_for_param = [0,2,4,5,6] 
##    shs_for_validate = [7,8,9,10]    
##    T_a_deg = 40.0+k2deg
##    params = semisel_xls(file,shs_for_param, shs_for_validate, T_a_deg)    
##
##    print(params)
#    file = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/ARTICLES/doing/vsc_model/code/imposim/imposim_F800R17.xls'
#    params = imposim2xls(file)
#    print(params)
#
#
#    
#    T_a = 40+ k2deg
#    R_th_diode_sink = params['R_th_diode_sink']
#    R_th_igbt_sink = params['R_th_igbt_sink']
#    R_th_sink_a = params['R_th_sink_a']
#    a_d = params['a_d']
#    a_i = params['a_i']
#    b_d = params['b_d']
#    b_i = params['b_i']
#    c_d = params['c_d']
#    c_i = params['c_i']
#    d_d = params['d_d']
#    d_i = params['d_i']
#    e_d = params['e_d']
#    e_i = params['e_i']
#
#    
#    i_rms = 520
#
#    m = 400*np.sqrt(2)/800
#    fp =  1.0
#    p_igbt  = 1.000*(a_i + (b_i - c_i*m*fp)*i_rms + (d_i - e_i*m*fp)*i_rms*i_rms)
#    p_diode = 1.000*(a_d + (b_d - c_d*m*fp)*i_rms + (d_d - e_d*m*fp)*i_rms*i_rms)
#     
#    p_switch = p_igbt + p_diode + i_rms**2*0.000
#    
#    print('p_igbt',p_igbt)
#    print('p_diode',p_diode)
#    print('p_switch', p_switch)
#    T_sink_0       = T_a    + p_switch*R_th_sink_a;
#    T_igbt_0       = T_sink_0 + p_igbt *R_th_igbt_sink;
#    T_diode_0      = T_sink_0 + p_diode*R_th_diode_sink;
#
#    print('T_sink_0', T_sink_0-k2deg)
#    print('T_igbt_0', T_igbt_0-k2deg)
#    print('T_diode_0', T_diode_0-k2deg)
##    
###    C_th_diode= 10
###    C_th_diode_case= 2
###    C_th_igbt= 18
###    C_th_igbt_case= 5
###    C_th_sink= 6000.0
###    R_th_diode= 0.01979045401629802
###    R_th_diode_case= 0.018
###    R_th_igbt= 0.009765625
###    R_th_igbt_case= 0.009
###    R_th_sink= 0.007
###    a_d = 143.48507451
###    a_i = 421.02132341
###    b_d = 0.589627
###    b_i = 0.55708434
###    c_d = 0.18337165
###    c_i =-0.12254324
###    d_d = 0.00026235
###    d_i = 0.00089385
###    e_d = 0.00021407
###    e_i =-0.00041411
###    T_a = 35.0+273
###    params ={'C_th_diode': C_th_diode,
###     'C_th_diode_case': C_th_diode_case,
###     'C_th_igbt': C_th_igbt,
###     'C_th_igbt_case': C_th_igbt_case,
###     'C_th_sink': C_th_sink,
###     'R_th_diode': R_th_diode,
###     'R_th_diode_case': R_th_diode_case,
###     'R_th_igbt': R_th_igbt,
###     'R_th_igbt_case':R_th_igbt_case,
###     'R_th_sink': R_th_sink,
###     'a_d':  a_d,
###     'a_i':  a_i,
###     'b_d':  b_d,
###     'b_i':  b_i,
###     'c_d':  c_d,
###     'c_i':  c_i,
###     'd_d':  d_d,
###     'd_i':  d_i,
###     'e_d':  e_d,
###     'e_i':  e_i,
###     'm':0.85,
###     'fp':0.8,
###     'i_rms':1400,
###      'T_a':35+273.3,       
###            }
###            
###    
###    i_rms = 1500
###    fp = 0.85
###    m = 0.8
###    pows, temps = losses(i_rms, m, fp, T_a, params)
###    print(pows)
###    print(temps)