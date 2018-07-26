from pyvsc import man2param
import numpy as np
def test_1():
    k2deg = 273.15
    array = np.array
    man_electric = {
        'i_1':1400 ,'m_1':0.8 , 'cosphi_1':0.8,'p_igbt_1':3570 ,'p_diode_1':1046 ,
        'i_2':1000 ,'m_2':0.8 , 'cosphi_2':0.2,'p_igbt_2':1952 ,'p_diode_2': 931 ,
        'i_3':1300 ,'m_3':0.8 , 'cosphi_3':0.2,'p_igbt_3':2772 ,'p_diode_3':1252 ,
        'i_4':1000 ,'m_4':0.1 , 'cosphi_4':0.2,'p_igbt_4':1882 ,'p_diode_4': 987 ,
        'i_5':1500 ,'m_5':0.85, 'cosphi_5':0.5,'p_igbt_5':3749 ,'p_diode_5':1293 ,
        }    
     
    man_thermal = {        'p_igbt':3570 ,'p_diode':1046 , 'T_igbt':125 , 'T_diode':97 , 'T_sink':57.3, 'T_a':40.0}
    
    params = man2param(man_electric,man_thermal)
    
    assert abs(float(params['a_i']) - 918.4939)  < 0.1 