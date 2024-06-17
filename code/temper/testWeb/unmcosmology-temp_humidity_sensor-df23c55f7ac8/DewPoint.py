import numpy as np

def Dew(T,RH): 
    """
    A well-known empirical approximation used to calculate the dew point
    by Wikipedia https://en.wikipedia.org/wiki/Dew_point#Calculating_the_dew_point
    """

    # b and c constant for temperature range -40 C to +50 C
    b = 17.625 
    c = 243.04 #C 
    lam = np.log(RH/100) + ((b*T)/(c+T))
    dewPoint = ((c*lam)/(b-lam))
    
    
    return ( "{dew:.2f}".format(dew = dewPoint) )

if __name__ == '__main__':
    print(type(Dew(2.0,20.0)),Dew(2.0,20.0)) 

