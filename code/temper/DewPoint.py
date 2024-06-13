import numpy as np

def Dew(T,RH): 
    """
    A well-known empirical approximation used to calculate the dew point
    by Wikipedia https://en.wikipedia.org/wiki/Dew_point#Calculating_the_dew_point
    """

    # b and c constant for temperature range -40°C to +50°C
    b = 17.625 
    c = 243.04 #°C 
    lam = np.log(RH/100) + (b*T)/(c+T)
    dewPoint = float(f"{(c*lam)/(b-lam):.2f}") 

    return dewPoint


if __name__ == '__main__':
    print(type(Dew(30,20)),Dew(30,20))
