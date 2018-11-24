""" Directed Graph Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of directed graphs, and it is
designed for our traffic flow assignment problem, thus we
have the following assumptions:
1. The graph contains no self-loop, that is, an edge that 
connects a vertex to itself
2. There is at most one edge which connects two vertice
Revised from: https://www.python-course.eu/graphs_python.php
and in our case we must give order to all the edges, thus we
do not use the unordered data structure.
"""


class Graph(object):

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
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
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

if __name__ == "__main__":

    g = {
        "a" : ["b", "d"],
        "b" : ["f", "c"],
        "c" : ["b", "d"],
        "d" : ["e"],
        "e" : ["f", "c"],
        "f" : []
    }

    graph = Graph(g)

    print("Vertices of graph:")
    print(graph.vertices())

    print("Edges of graph:")
    print(graph.edges())

    print('The path from vertex "a" to vertex "c":')
    path = graph.find_all_paths("a", "c")
    print(path)

    print('The path from vertex "a" to vertex "f":')
    path = graph.find_all_paths("a", "f")
    print(path)