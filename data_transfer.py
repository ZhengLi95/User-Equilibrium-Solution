import xlwt
import xlrd

def CreateNLMatrix(data_location):

    try:
        workbook = xlrd.open_workbook(data_location)
    except IOError:
        print('Please follow the instruction in README: Build a template by running create_template.py!')
        exit()

    data = workbook.sheet_by_index(0)
    rows = data.nrows

    NL_matrix = []

    for row in range(1, rows):
        NL_matrix.append([int(data.cell(row, 0).value) - 1, int(data.cell(row, 1).value) - 1])

    return NL_matrix

def ReadBasicData(data_location):

    workbook = xlrd.open_workbook(data_location)
    data = workbook.sheet_by_index(0)
    rows = data.nrows

    distance = []
    capacity = []
    free_speed = []
    t0 = []

    for row in range(1, rows):
        distance.append(float(data.cell(row, 2).value))

    for row in range(1, rows):
        capacity.append(float(data.cell(row, 3).value * float(data.cell(row, 5).value)))

    for row in range(1, rows):
        free_speed.append(int(data.cell(row, 4).value))

    for i in range(len(capacity)):
        t0.append(distance[i] / free_speed[i] * 60)

    return capacity, t0

def ReadDemands(data_location):

    workbook = xlrd.open_workbook(data_location)
    demand = workbook.sheet_by_index(1)
    rows = demand.nrows
    cols = demand.ncols

    demands = []
    for i in range(1, rows):
        for j in range(1, cols):
            od = [int(demand.cell(i, 0).value - 1), int(demand.cell(0, j).value - 1)]
            od.append(demand.cell(i, j).value)
            demands.append(od)

    return demands

def ReadParams(data_location):

    workbook = xlrd.open_workbook(data_location)
    params = workbook.sheet_by_index(2)
    alpha = params.cell(0, 1).value
    beta = params.cell(1, 1).value

    return alpha, beta

def PrintAnswers2XLS(file_location, link_flow, link_time, path_time, vc_ratio, total_time, NL_matrix, LP_matrix):

    workbook = xlwt.Workbook()
    flow_sheet = workbook.add_sheet(sheetname= 'FLOW', cell_overwrite_ok= True)
    graph_sheet = workbook.add_sheet(sheetname= 'GRAPH', cell_overwrite_ok= True)

    title1 = ['No.', 'Origin', 'Destination', 'Link Flow', 'Link Time', 'V/C']
    width1 = len(title1) + 1

    for i in range(len(title1)):
        flow_sheet.write(0, i, title1[i])

    for row in range(1, len(NL_matrix)+1):
        flow_sheet.write(row, 0, row)
        flow_sheet.write(row, 1, NL_matrix[row-1][0] + 1)
        flow_sheet.write(row, 2, NL_matrix[row-1][1] + 1)
        flow_sheet.write(row, 3, round(link_flow[0, row-1], 3))
        flow_sheet.write(row, 4, round(link_time[0, row-1], 3))
        flow_sheet.write(row, 5, round(vc_ratio[0, row-1], 3))

    title2 = ['No.', 'Path Flow']
    width2 = width1 + len(title2) + 1

    for i in range(len(title2)):
        flow_sheet.write(0, i + width1, title2[i])

    for row in range(1, path_time.shape[0] + 1):
        flow_sheet.write(row, 0 + width1, row)
        flow_sheet.write(row, 1 + width1, round(path_time[row-1,0], 3))

    title3 = ['Total Travel Time']

    for i in range(len(title3)):
        flow_sheet.write(0, i + width2, title3[i])

    flow_sheet.write(1, width2, round(total_time[0], 3))

    graph_sheet.write(0, 0, 'LP Matrix')

    for i in range(LP_matrix.shape[0]):
        graph_sheet.write(i+1, 0, i+1)

    for j in range(LP_matrix.shape[1]):
        graph_sheet.write(0, j+1, j+1)

    for i in range(LP_matrix.shape[0]):
        for j in range(LP_matrix.shape[1]):
            graph_sheet.write(i+1, j+1, int(LP_matrix[i,j]))


    workbook.save(file_location)
