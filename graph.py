
class Graph(object):
    """ DIRECTED GRAPH CLASS

    A simple Python graph class, demonstrating the essential 
    facts and functionalities of directed graphs, and it is
    designed for our traffic flow assignment problem, thus we
    have the following assumptions:

    1. The graph contains no self-loop, that is, an edge that 
    connects a vertex to itself;

    2. There is at most one edge which connects two vertice;

    Revised from: https://www.python-course.eu/graphs_python.php
    and in our case we must give order to all the edges, thus we
    do not use the unordered data structure.
    """

    def __init__(self, graph_dict= None):
        """ initializes a directed graph object by a dictionary,
            If no dictionary or None is given, an empty dictionary 
            will be used. Notice that this initial graph cannot
            contain a self-loop.
        """
        from collections import OrderedDict
        if graph_dict == None:
            graph_dict = OrderedDict()
        self.__graph_dict = OrderedDict(graph_dict)
        if self.__is_with_loop():
            raise ValueError("The graph are supposed to be without self-loop please recheck the input data!")

    def vertices(self):
        """ returns the vertices of a graph
        """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph
        """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []
        else:
            print("The vertex %s already exists in the graph, thus it has been ignored!" % vertex)

    def add_edge(self, edge):
        """ Assume that edge is ordered, and between two 
            vertices there could exists only one edge. 
        """
        vertex1, vertex2 = self.__decompose_edge(edge)
        if not self.__is_edge_in_graph(edge):
            if vertex1 in self.__graph_dict:
                self.__graph_dict[vertex1].append(vertex2)
                if vertex2 not in self.__graph_dict:
                    self.__graph_dict[vertex2] = []
            else:
                self.__graph_dict[vertex1] = [vertex2]
        else:
            print("The edge %s already exists in the graph, thus it has been ignored!" % ([vertex1, vertex2]))

    def find_all_paths(self, start_vertex, end_vertex, path= []):
        """ find all simple paths (path with no repeated vertices)
            from start vertex to end vertex in graph 
        """
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        paths = []
        for neighbor in self.__graph_dict[start_vertex]:
            if neighbor not in path:
                sub_paths = self.find_all_paths(neighbor, end_vertex, path)
                for sub_path in sub_paths:
                    paths.append(sub_path)
        return paths

    def __is_edge_in_graph(self, edge):
        """ Judge if an edge is already in the graph
        """
        vertex1, vertex2 = self.__decompose_edge(edge)
        if vertex1 in self.__graph_dict:
            if vertex2 in self.__graph_dict[vertex1]:
                return True
            else:
                return False
        else:
            return False
    
    def __decompose_edge(self, edge):
        """ Input is a list or a tuple with only two elements
        """
        if (isinstance(edge, list) or isinstance(edge, tuple)) and len(edge) == 2:
            return edge[0], edge[1]
        else:
            raise ValueError("%s is not of type list or tuple or its length does not equal to 2" % edge)

    def __is_with_loop(self):
        """ If the graph contains a self-loop, that is, an 
            edge connects a vertex to itself, then return
            True, otherwise return False
        """
        for vertex in self.__graph_dict:
            if vertex in self.__graph_dict[vertex]:
                return True
        return False

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as list
            of two vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbor in self.__graph_dict[vertex]:
                edges.append([vertex, neighbor])
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

class TrafficNetwork(Graph):
    ''' TRAFFIC NETWORK CLASS
        Traffic network is a combination of basic graph
        and the demands, the informations about links, paths
        and link-path incidence matrix will be generated
        after the initialization.
    '''

    def __init__(self, graph= None, O= [], D= []):
        Graph.__init__(self, graph)
        self.__origins = O
        self.__destinations = D
        self.__cast()

    # Override of add_edge function, notice that when an edge
    # is added, then the links and paths will changes alongside.
    # However, it doesn't matter when a vertex is added
    def add_edge(self, edge):
        Graph.add_edge(self, edge)
        self.__cast()

    def add_origin(self, origin):
        if origin not in self.__origins:
            self.__origins.append(origin)
            self.__cast()
        else:
            print("The origin %s already exists, thus has been ignored!" % origin)

    def add_destination(self, destination):
        if destination not in self.__destinations:
            self.__destinations.append(destination)
            self.__cast()
        else:
            print("The destination %s already exists, thus has been ignored!" % destination)

    def num_of_links(self):
        return len(self.__links)

    def num_of_paths(self):
        return len(self.__paths)

    def num_of_OD_pairs(self):
        return len(self.__OD_pairs)

    def __cast(self):
        """ Calculate or re-calculate the links, paths and
            Link-Path incidence matrix
        """
        if self.__origins != None and self.__destinations != None:
            # OD pairs = Origin-Destination Pairs
            self.__OD_pairs = self.__generate_OD_pairs()
            self.__links = self.edges()
            self.__paths, self.__paths_category = self.__generate_paths_by_demands()
            # LP Matrix = Link-Path Incidence Matrix
            self.__LP_matrix = self.__generate_LP_matrix()
    
    def __generate_OD_pairs(self):
        ''' Generate the OD pairs (Origin-Destination Pairs)
            by Cartesian production 
        '''
        OD_pairs = []
        for o in self.__origins:
            for d in self.__destinations:
                OD_pairs.append([o, d])
        return OD_pairs

    def __generate_paths_by_demands(self):
        """ According the demands, i.e. the origins and the
            destinations of the traffic flow, to construct a list
            of paths which are necessary for the traffic flow
            assignment model
        """ 
        paths_by_demands = []
        paths_category = []
        od_pair_index = 0
        for OD_pair in self.__OD_pairs:
            paths = self.find_all_paths(*OD_pair)
            paths_by_demands.extend(paths)
            paths_category.extend([od_pair_index] * len(paths))
            od_pair_index += 1
        return paths_by_demands, paths_category

    def __generate_LP_matrix(self):
        """ Generate the Link-Path incidence matrix Delta:
            if the i-th link is on j-th link, then delta_ij = 1,
            otherwise delta_ij = 0
        """
        import numpy as np
        n_links = self.num_of_links()
        n_paths = self.num_of_paths()
        lp_mat = np.zeros(shape= (n_links, n_paths), dtype= int)
        path_index = 0
        for path in self.__paths:
            for i in range(len(path) - 1):
                current_link = self.__get_link_from_path_by_order(path, i)
                link_index = self.__links.index(current_link)
                lp_mat[link_index, path_index] = 1
            path_index += 1
        return lp_mat
    
    def __get_link_from_path_by_order(self, path, order):
        """ Given a path, which is a list with length N, 
            search the link by order, which is a integer
            in the range [0, N-2]
        """
        if len(path) >= 2:
            if order >= 0 and order <= len(path) - 2:
                return [path[order], path[order+1]]
            else:
                raise ValueError("%d is not in the reasonale range!" % order)
        else:
            raise ValueError("%s contains only one vertex and cannot be input!" % path)

    def disp_links(self):
        ''' Print all the links in the network by order
        '''
        counter = 0
        for link in self.__links:
            print("%d : %s" % (counter, link))
            counter += 1

    def disp_paths(self):
        """ Print all the paths in order according to
            given origins and destinations
        """
        counter = 0
        for path in self.__paths:
            print("%d : %s " % (counter, path))
            counter += 1

    def LP_matrix(self):
        ''' Return the Link-Path matrix of
            current traffic network
        '''
        return self.__LP_matrix

    def OD_pairs(self):
        """ Return the origin-destination pairs of
            current traffic network
        """
        return self.__OD_pairs

    def paths_category(self):
        """ Return a list which implies the conjugacy
            between path (self.__paths) and origin-
            destinaiton pair (self.__OD_pairs)
        """
        return self.__paths_category

    def paths(self):
        """ Return the paths with respected to given
            origins and destinations 
        """
        return self.__paths