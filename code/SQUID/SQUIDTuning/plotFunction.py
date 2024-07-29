import matplotlib.pyplot as plt
import numpy as np
import pickle as pkl
import os
import glob
#import packages

def getDict(file):
    """This function reads a pickle file 
    and returns the dictionary stored in it"""

    with open(file,'rb') as f:
        SQUID_dict = pkl.load(f)
        #print(type(SQUID_dict.keys()))
    return SQUID_dict

# calculate the derivative
def getDerivative(x, y):
    dy_forward = np.diff(y) / np.diff(x)
    half_diff = np.diff(x) / 2
    x_mid = x[:-1] + half_diff
    return dy_forward, x_mid

def get_sublist_around_point(inputlist, start_point, num_elements_each_side=4):
    """
    plot 4 points before and 3 pts after the chosen point
    """
    start_index = max(0, start_point - num_elements_each_side)
    end_index = min(len(inputlist), start_point + num_elements_each_side)
    return inputlist[start_index:end_index]

def PlotandSave(folder):
    
    folder_path = folder+'/data'
    pkl_files = glob.glob(os.path.join(folder_path, '*.SQUID_OUTPUT.pkl'))
    #a empty dictionary to store diff pkl files
    data = {}
    #print(len(pkl_files))
    #save the date to a Dictioanry
    for i in range(len(pkl_files)):
        file_name = pkl_files[i].split('\\')[-1]
        #print(file_name)
        data[f'{file_name}'] = getDict(pkl_files[i])
        
        # if i > 1:
        #     break

    #print(data)

    for file in data:
        SQUID_pstring = data[file]["squid_pstring"]
        SQUID_pstring = SQUID_pstring.replace("/", "_")

        save_path = f'plots/{folder}/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        

        intermediate_vphis = data[file]['intermediate_vphis']
        vphis = intermediate_vphis["vphis"]
        for key in vphis:
            if "CB" in key:
                label = vphis[key]['label']
                label = label[:33]+" V"
                y = vphis[key]['y']
                x = vphis[key]['x']
                plt.plot(x,y,label = label, marker = 'o')
        
        plt.title(f"VPhi Plot for a range of current baises\nSQUID id: {SQUID_pstring}")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.savefig(f"{save_path}{SQUID_pstring}_intermediate.png", bbox_inches='tight')
        plt.cla()

        cb_optimization = data[file]['cb_optimization']
        for key in cb_optimization:
            if "v" in key or "chosen_point" in key:
                label = cb_optimization[key]['label']
                y = cb_optimization[key]['y']
                x = cb_optimization[key]['x']
                plt.plot(x,y,label = label)
        plt.title(f"current baises optimization(VOP2P vs CBV)\nSQUID id: {SQUID_pstring}")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.savefig(f"{save_path}{SQUID_pstring}_cb_optimization.png", bbox_inches='tight')
        plt.cla()

        fb_optimization = data[file]['fb_optimization']
        

        for key in fb_optimization:
            
            if "vphi_curve" in key:
                label = fb_optimization[key]['label']
                y = (fb_optimization[key]['y'])
                x = (fb_optimization[key]['x']) 
                plt.plot(x,y,label = label)

                dy, dx = getDerivative(x, y)
                
                ddy, ddx = getDerivative(dx, dy)
            
            if "chosen_point" in key:
                label_cp = fb_optimization[key]['label']
                y_cp = fb_optimization[key]['y']
                x_cp = fb_optimization[key]['x']

        plt.axvline(x=x_cp[0], color='b', linestyle='--', label=label_cp)       
        plt.title(f"Flux Bias optimization(For single V-Phi)\nSQUID id: {SQUID_pstring}")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.savefig(f"{save_path}{SQUID_pstring}_fb_optimization.png", bbox_inches='tight')
        plt.cla()

        plt.title(f"First Derivative of FB_optimization\nSQUID id: {SQUID_pstring}")
        plt.axvline(x=x_cp[0], color='r', linestyle='--', label=label_cp)
        plt.plot(dx,dy,label = "First Derivative of "+label)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.savefig(f"{save_path}{SQUID_pstring}_fb_optimization_d.png", bbox_inches='tight')
        plt.cla()

        plt.title(f"Second Derivative of FB_optimization\nSQUID id: {SQUID_pstring}")        
        plt.plot(ddx, ddy,label = "Second Derivative of "+label)
        plt.axvline(x=x_cp[0], color='g', linestyle='--', label=label_cp)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.savefig(f"{save_path}{SQUID_pstring}_fb_optimization_dd.png", bbox_inches='tight')
        plt.cla()

        #get zoom in part of the plot
        # use get_sublist_around_point function
        for i in range(len(x)):
            if i == 0:
                continue

            if (x[i] > x_cp[0] and x[i-1] < x_cp[0]):
                record_index = i
                
        zoom_x = get_sublist_around_point(x, record_index)
        zoom_y = get_sublist_around_point(y, record_index)

        plt.plot(zoom_x,zoom_y,"bo-", label = "zoom in the chosen point")
        plt.plot(x_cp,y_cp,"r-", label = label_cp)
        plt.title(f"Zoom in the chosen point")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.savefig(f"{save_path}{SQUID_pstring}_zoom.png", bbox_inches='tight')
        plt.cla()

        #get the zoom in part of the first derivative plot
        zoom_dy, zoom_dx = getDerivative(zoom_x, zoom_y)
        zoom_ddy, zoom_ddx = getDerivative(zoom_dx, zoom_dy)

        plt.plot(zoom_dx,zoom_dy,"ro-", label = "First Derivative of zoom in")
        plt.plot(x_cp,y_cp,"r-", label = label_cp)
        plt.title(f"First Derivative of Zoom in the chosen point")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.savefig(f"{save_path}{SQUID_pstring}_zoom_d.png", bbox_inches='tight')
        plt.cla()

        plt.plot(zoom_ddx,zoom_ddy,"go-", label = "Second Derivative of zoom in")
        plt.plot(x_cp,y_cp,"r-", label = label_cp)
        plt.title(f"Second Derivative of Zoom in the chosen point")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
        plt.savefig(f"{save_path}{SQUID_pstring}_zoom_dd.png", bbox_inches='tight')
        plt.cla()