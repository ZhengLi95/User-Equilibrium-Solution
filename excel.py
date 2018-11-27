import xlwt
import xlrd

class ExcelProcessor(object):

    def __init__(self):
        ''' Create an instance of ExcelProcessor class
        '''
        self.__input_filename = "input.xls"
        self.__output_filename = "output.xls"

    def create_template(self):
        ''' Create a template file of input data
            under current work directory
        '''
        workbook = xlwt.Workbook()

        sheet0 = workbook.add_sheet(sheetname= 'BASIC_PARAMS', cell_overwrite_ok= True)
        sheet1 = workbook.add_sheet(sheetname= 'DEMAND', cell_overwrite_ok= True)

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

        workbook.save(self.__input_filename)

    def read_links(self):
        ''' Read the topology of the graph
            from the file `input.xls`
        '''
        workbook = xlrd.open_workbook(self.__input_filename)
        data = workbook.sheet_by_index(0)
        rows = data.nrows
        links = [ [self.__trans(data.cell(i, 0).value), self.__trans(data.cell(i, 1).value)] for i in range(1, rows) ]
        return links

    def read_basic_params(self):
        ''' Read the values of variables link_free_time
            and link_capacity from the file `input.xls`
        '''
        workbook = xlrd.open_workbook(self.__input_filename)
        data = workbook.sheet_by_index(0)
        rows = data.nrows

        distance = [float(data.cell(row, 2).value) for row in range(1, rows)]
        link_capacity = [float(data.cell(row, 3).value * float(data.cell(row, 5).value)) for row in range(1, rows)]
        free_speed = [float(data.cell(row, 4).value) for row in range(1, rows)]
        link_free_time = [distance[i] / free_speed[i] * 60 for i in range(len(link_capacity))]

        return link_free_time, link_capacity

    def read_demands(self):
        ''' Read the values of variable origins, 
            destinations and demands from the
            file `input.xls`
        '''
        workbook = xlrd.open_workbook(self.__input_filename)
        demand = workbook.sheet_by_index(1)
        rows = demand.nrows
        cols = demand.ncols

        origins = [self.__trans(demand.cell(i, 0).value) for i in range(1, rows)]
        destinations = [self.__trans(demand.cell(0, j).value) for j in range(1, cols)]
        demands = [demand.cell(i, j).value for i in range(1, rows) for j in range(1, cols)]

        return origins, destinations, demands

    def report_to_excel(self, links, link_flow, link_time, path_time, link_vc, LP_matrix):
        ''' Interface between Python and Excel, 
            used for generating the solution report
        '''

        workbook = xlwt.Workbook()
        flow_sheet = workbook.add_sheet(sheetname= 'FLOW', cell_overwrite_ok= True)
        graph_sheet = workbook.add_sheet(sheetname= 'GRAPH', cell_overwrite_ok= True)

        title1 = ['No.', 'Origin', 'Destination', 'Link Flow', 'Link Time', 'V/C']
        width1 = len(title1) + 1

        for i in range(len(title1)):
            flow_sheet.write(0, i, title1[i])

        for row in range(1, len(links)+1):
            flow_sheet.write(row, 0, row)
            flow_sheet.write(row, 1, links[row-1][0])
            flow_sheet.write(row, 2, links[row-1][1])
            flow_sheet.write(row, 3, round(link_flow[row-1], 3))
            flow_sheet.write(row, 4, round(link_time[row-1], 3))
            flow_sheet.write(row, 5, round(link_vc[row-1], 3))

        title2 = ['No.', 'Path Time']
        width2 = width1 + len(title2) + 1

        for i in range(len(title2)):
            flow_sheet.write(0, i + width1, title2[i])

        for row in range(1, path_time.shape[0] + 1):
            flow_sheet.write(row, 0 + width1, row)
            flow_sheet.write(row, 1 + width1, round(path_time[row-1], 3))

        graph_sheet.write(0, 0, 'LP Matrix')

        for i in range(LP_matrix.shape[0]):
            graph_sheet.write(i+1, 0, i+1)

        for j in range(LP_matrix.shape[1]):
            graph_sheet.write(0, j+1, j+1)

        for i in range(LP_matrix.shape[0]):
            for j in range(LP_matrix.shape[1]):
                graph_sheet.write(i+1, j+1, int(LP_matrix[i,j]))

        workbook.save(self.__output_filename)
    
    def __trans(self, num):
        """ Try to transform a float into int, and then
            into string type. If input is not float, it
            will be returned back without any change
        """
        if isinstance(num, float):
            return str(int(num))
        else:
            return num
        