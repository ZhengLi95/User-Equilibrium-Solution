import numpy as np
import copy

def LinkPerformanceFun(link_flow, alpha, beta, t0, capacity):

    value = t0*(1+alpha*((link_flow/capacity)**beta))

    return value

def Integral_LinkPerformanceFun(link_flow, alpha, beta, t0, capacity):

    value = t0*link_flow + alpha*t0*(link_flow**(beta+1))/((capacity**beta)*(beta+1))

    return value

def GetEmptyLinkFlow(NL_matrix):

    link_flow = np.zeros((1, len(NL_matrix)), 'float')

    return link_flow

def GetNodeNumber(NL_matrix):

    max_node_each_link = []

    for link in NL_matrix:
        max_node_each_link.append(max(link))

    max_node = max(max_node_each_link)

    return max_node

def Link2Path(NL_matrix, paths_grouped):

    link_num = len(NL_matrix)
    path_num = 0

    for paths in paths_grouped:
        path_num += len(paths)

    LP_matrix = np.zeros((link_num, path_num),'int')
    col = 0

    for paths in paths_grouped:
        for path in paths:
            length = len(path)
            for i in range(length-1):
                link = [path[i], path[i+1]]
                LP_matrix[NL_matrix.index(link), col] = 1
            col += 1

    return LP_matrix, paths_grouped

def CreateLPMatrix(NL_matrix, demands):

    NODE_NUM = GetNodeNumber(NL_matrix)

    # adj_matrix is the abbreviation of adjacent matrix
    adj_matrix = np.zeros((NODE_NUM + 1, NODE_NUM + 1), 'int')

    for i in range(len(NL_matrix)):
        adj_matrix[NL_matrix[i][0], NL_matrix[i][1]] = 1

    paths_grouped = []
    paths = []

    def search_all_path(graph, o, d, path=[]):
        size = graph.shape[0]
        path.append(o)
        if (o == d):
            paths.append(copy.deepcopy(path))
        else:
            for next_node in range(size):
                if graph[o, next_node] == 1:
                    search_all_path(graph, next_node, d, path)
        path.pop()

    for i in range(len(demands)):
        origin = demands[i][0]
        destination = demands[i][1]
        search_all_path(graph=adj_matrix, o=origin, d=destination)
        paths_grouped.append(copy.deepcopy(paths))
        paths = []
    LP_matrix = Link2Path(NL_matrix, paths_grouped)

    return LP_matrix

def LinkFlow2LinkTime(link_flow, alpha, beta, t0, capacity):

    link_time = np.zeros(link_flow.shape, 'float')

    for i in range(link_time.shape[1]):
        link_time[0, i] = LinkPerformanceFun(link_flow[0, i], alpha, beta, t0[i], capacity[i])

    return link_time


def LinkTime2PathTime(link_time, LP_matrix):

    path_time = link_time.dot(LP_matrix).transpose()

    return path_time


def PathTime2PathFlow_AON_Assign(path_time, LP_matrix, paths_grouped, demands):

    path_flow = np.zeros((LP_matrix.shape[1], 1), 'float')

    col = 0
    group = 0

    for paths in paths_grouped:
        path_num = len(paths)

        buffer_path_time = path_time[col:col + path_num]
        buffer_path_time_min = buffer_path_time.min()

        min_loc = np.where(buffer_path_time == buffer_path_time_min)[0][0]
        abs_min_loc = min_loc + col

        path_flow[abs_min_loc, 0] = demands[group][2]

        col += path_num
        group += 1

    return path_flow

def AllOrNothingAssign(link_flow, LP_matrix, paths_grouped, demands, alpha, beta, t0, capacity):

    link_time = LinkFlow2LinkTime(link_flow, alpha, beta, t0, capacity)
    path_time = LinkTime2PathTime(link_time, LP_matrix)
    path_flow = PathTime2PathFlow_AON_Assign(path_time, LP_matrix, paths_grouped, demands)
    link_flow = LP_matrix.dot(path_flow).transpose()

    return link_flow

def Obj_Value(flow, alpha, beta, t0, capacity, NL_matrix):

    val = 0

    for i in range(len(NL_matrix)):
        val += Integral_LinkPerformanceFun(flow[0, i], alpha, beta, t0[i], capacity[i])

    return val

def Dichotomy(link_flow, auxiliary_link_flow, alpha, beta, t0, capacity, lp_accuracy, NL_matrix):

    LB = 0.
    UB = 1.

    while True:

        theta = (LB + UB) / 2.

        val_LB = Obj_Value((1. - LB) * link_flow + LB * auxiliary_link_flow, alpha, beta, t0, capacity, NL_matrix)
        val_UB = Obj_Value((1. - UB) * link_flow + UB * auxiliary_link_flow, alpha, beta, t0, capacity, NL_matrix)

        if val_LB < val_UB:
            UB = theta
        else:
            LB = theta

        if abs(LB - UB) < lp_accuracy:
            break

    return theta

def CheckConvergence(link_flow, new_link_flow, cp_accuracy):

    dev = abs(np.linalg.norm(new_link_flow) - np.linalg.norm(link_flow)) / np.linalg.norm(link_flow)

    if dev <= cp_accuracy:
        return True
    else:
        return False

def CreateParameters4Evaluation(link_flow, LP_matrix, alpha, beta, t0, capacity):

    link_time = LinkFlow2LinkTime(link_flow, alpha, beta, t0, capacity)

    path_time = LinkTime2PathTime(link_time, LP_matrix)

    vc_ratio = np.zeros(link_flow.shape, 'float')

    for i in range(vc_ratio.shape[1]):
        vc_ratio[0,i] = link_flow[0,i]/capacity[i]

    total_time = np.sum(link_time*link_flow, axis = 1)

    return link_flow, link_time, path_time, vc_ratio, total_time
