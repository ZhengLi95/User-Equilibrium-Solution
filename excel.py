import xlwt
import xlrd

class ExcelProcessor(object):

    def __init__(self, filename= "input"):
        ''' Create an instance of ExcelProcessor class, and
            initialize it by only a name of the file in which
            you will input the basic data. Notice the file
            name cannot be empty!
        '''
        self.__filename = filename

    def create_template(self):
        ''' Create a template file of input data by
            given name under current work directory
        '''
        workbook = xlwt.Workbook()

        sheet0 = workbook.add_sheet(sheetname= 'BASIC_DATA', cell_overwrite_ok= True)
        sheet1 = workbook.add_sheet(sheetname= 'DEMAND', cell_overwrite_ok= True)
        sheet2 = workbook.add_sheet(sheetname= 'PARAMS', cell_overwrite_ok= True)

        title_sheet0 = ['From', 'To', 'Free time (km)', 'No. of Lane', 'Free Flow Speed (km/h)', 'Capacity per lane (PCU)']
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

        workbook.save(self.__filename + ".xls")

    def CreateNLMatrix(self, data_location):

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

    def ReadBasicData(self, data_location):

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

    def read_demands(self, data_location):

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

    def read_params(self, data_location):

        workbook = xlrd.open_workbook(data_location)
        params = workbook.sheet_by_index(2)
        alpha = params.cell(0, 1).value
        beta = params.cell(1, 1).value

        return alpha, beta

    def PrintAnswers2XLS(self, file_location, link_flow, link_time, path_time, vc_ratio, total_time, NL_matrix, LP_matrix):

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
