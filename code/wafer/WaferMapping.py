import module as md

#goal1
myGoal = md.getGoal('.\code\wafer\\nist_so_mf_detector_array_padinfo.csv')
column_names = ['Grouptype','GroupIndex','Group Section',
                        'Pad X center', 'Pad Y center','Pixel X center', 'Pixel Y center']
myGoal.getColumns(column_names)
path = './newdata/goal1'
bins = 100
scale_form = 'log'
myGoal.getGoal1(path, bins, scale_form)

#goal2 way1

#goal2 way2


