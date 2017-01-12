import xlwt


#============================================================================
# Please input the location where you want to create the tamplate
data_loc = 'data.xls'

#============================================================================


workbook = xlwt.Workbook()

sheet0 = workbook.add_sheet(sheetname= 'BASIC_DATA', cell_overwrite_ok= True)
sheet1 = workbook.add_sheet(sheetname= 'DEMAND', cell_overwrite_ok= True)
sheet2 = workbook.add_sheet(sheetname= 'PARAMS', cell_overwrite_ok= True)

title_sheet0 = ['From', 'To', 'Distance (km)', 'No. of Lane', 'Free Flow Speed (km/h)', 'Capacity per lane (PCU)']

for i in range(len(title_sheet0)):
    sheet0.write(0, i, title_sheet0[i])

basic_data = [
    [5, 7, 10.0, 2, 60, 1800],
    [5, 9, 10.0, 2, 60, 1800],
    [6, 7, 10.0, 2, 60, 1800],
    [6, 8, 14.1, 2, 60, 1800],
    [7, 8, 10.0, 2, 60, 1800],
    [7, 10, 10.0, 2, 60, 1800],
    [8, 11, 10.0, 2, 60, 1800],
    [8, 12, 14.1, 2, 60, 1800],
    [9, 10, 10.0, 2, 60, 1800],
    [9, 16, 22.4, 2, 60, 1800],
    [10, 11, 10.0, 2, 60, 1800],
    [10, 13, 10.0, 2, 60, 1800],
    [11, 14, 10.0, 2, 60, 1800],
    [12, 15, 10.0, 2, 60, 1800],
    [13, 14, 10.0, 2, 60, 1800],
    [13, 16, 10.0, 2, 60, 1800],
    [14, 15, 10.0, 2, 60, 1800],
    [14, 17, 10.0, 2, 60, 1800],
    [16, 17, 10.0, 2, 60, 1800],
]

for row in range(1, len(basic_data)+1):
    for col in range(len(basic_data[0])):
        sheet0.write(row, col, basic_data[row-1][col])

sheet1.write(0, 0, 'Demand')
sheet1.write(0, 1, 17)
sheet1.write(0, 2, 15)
sheet1.write(1, 0, 5)
sheet1.write(2, 0, 6)

demands = [
    [6750, 6000],
    [5250, 7500]
]

for i in range(1, len(demands)+1):
    for j in range(1, len(demands)+1):
        sheet1.write(i, j, demands[i-1][j-1])

sheet2.write(0, 0, 'ALPHA')
sheet2.write(0, 1, 0.15)
sheet2.write(1, 0, 'BETA')
sheet2.write(1, 1, 4)

workbook.save(data_loc)

