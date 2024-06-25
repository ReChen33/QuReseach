import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def saveCSV(data, path = '.\data\goal', numbins=100, scale='linear'):

    num, bins, patches = plt.hist(data, bins=numbins)

    path_filename = f'{path} {len(bins)-1}bins'

    plt.xscale(scale)
    plt.savefig(f'{path_filename}.png')         
    plt.show()

    #create an array stored the value number per bin
    number_per_bin = []
    for i in range(len(patches)):
        if num[i] != 0:
            number_per_bin.append([f"({bins[i]},{bins[i+1]})",num[i]])
                
    # Save data to CSV
    number_per_bin = np.array(number_per_bin)
    data_NpB = np.column_stack((number_per_bin[:,0],number_per_bin[:,1])) 
    # the data for number_per_bin
    df = pd.DataFrame(data_NpB,columns=['range of distance','number in the range'])
    df.to_csv(f'{path_filename}.csv', index=False)


def getDistance(data,xIndex,yIndex):

    distance = []
    
    for i in range(len(data)):
        
        if i+1 < len(data):
            x_distance = data[i][xIndex] - data[i+1][xIndex]
            y_distance = data[i][yIndex] - data[i+1][yIndex]
            
        elif i+1 == len(data):
            x_distance = data[i][xIndex] - data[0][xIndex]
            y_distance = data[i][yIndex] - data[0][yIndex]

        distance_xy = np.sqrt((x_distance)**2 + (y_distance)**2)
        distance.append(distance_xy)

    return distance


class getGoal:
    """use getGoal class for goal1, goal2 way1, and goal2 way2"""    

    def __init__(self, data_file = 'nist_so_mf_detector_array_padinfo.csv'):
        self.data = pd.read_csv(data_file)

    def getColumns(self,column_names = ['Grouptype','GroupIndex','Group Section',
                        'Pad X center', 'Pad Y center','Pixel X center', 'Pixel Y center']):
#Index help: 
    # Grouptype is 0; GroupIndex is 1; Group Section is 2; 
    # Pad X center is 3; Pad Y center is 4; 
    # Pixel X center is 5; Pixel Y center is 6
        self.data_goal = self.data[column_names]
        self.data_goal = np.array(self.data_goal).tolist()

    def getGoal1(self,path_name = "./data/goal1", bins=100, scale_form='log'):
        pixel_x_center = self.data['Pixel X center']

        #get unique pixel x 
        unique_pixel_x = np.unique(pixel_x_center)

        distance_goal1 = []
        #first group the data by pixel x save to group_data
        #and then group the data by pixel y
        #and then calculate the distance to the pad

        for j in range(len(unique_pixel_x)):
            group_data = []           
            y_pixel_in_group = []

            #first group the data by pixel x
            for i in range(len(self.data)):
                if pixel_x_center[i] == unique_pixel_x[j]:
                    group_data.append(self.data_goal[i])
                    # get all pixel y position 
                    y_pixel_in_group.append(self.data_goal[i][6])

            #get unique pixel y
            unique_pixel_y = np.unique(y_pixel_in_group)   
            for k in range(len(unique_pixel_y)):

                group_data_y = []
                for i in range(len(group_data)):
                    if y_pixel_in_group[i] == unique_pixel_y[k]:
                        #group the data by same pixel y   
                        group_data_y.append(group_data[i])
                     
                distance_goal1.append(getDistance(group_data_y,3,4))

        saveCSV(distance_goal1, path = path_name, numbins = bins, scale = scale_form)
                

if __name__ == '__main__':
    myGoal = getGoal('.\code\wafer\\nist_so_mf_detector_array_padinfo.csv')
    column_names = ['Grouptype','GroupIndex','Group Section',
                        'Pad X center', 'Pad Y center','Pixel X center', 'Pixel Y center']
    myGoal.getColumns(column_names)
    path = '.\code\wafer\\newdata\goal1'
    bins = 100
    scale_form = 'log'
    myGoal.getGoal1(path, bins, scale_form)