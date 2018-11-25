from graph import TrafficNet
import numpy as np
import scipy.optimize as opt


class TrafficFlowMod:

    def __init__(self, g, O, D, demand, link_free_time, link_capacity):

        self.__network = TrafficNet(graph_dict= g, O= O, D= D)

        n_links = self.__network.num_of_links()
        n_paths = self.__network.num_of_paths()

        # Initialization of parameters
        self.__link_free_time = np.array(link_free_time)
        self.__link_capacity = np.array(link_capacity)
        self.__demand = np.array(demand)

        # alpha and beta
        self._alpha = 0.15
        self._beta = 4 

        # Convergent criterion
        self.__accuracy = 1e-6

        print(self)

    def solve(self):
        ''' Solve the traffic flow assignment model (user equilibrium)
            by Frank-Wolfe algorithm, all the necessary data must be 
            properly input into the model in advance. 
        '''
        # Step 0: based on the x0, generate the x1
        empty_flow = np.zeros(self.__network.num_of_links())
        link_flow = self.__all_or_nothing_assign(empty_flow)

        counter = 0

        while True:

            # Step 1 & Step 2: Use the link flow matrix -x to generate the time, then generate the auxiliary link flow matrix -y
            auxiliary_link_flow = self.__all_or_nothing_assign(link_flow)

            # Step 3: Linear Search
            opt_theta = self.__golden_section(link_flow, auxiliary_link_flow)
            print("opt_theta : %s" % opt_theta)

            # Step 4: Using optimal theta to update the link flow matrix
            new_link_flow = (1 - opt_theta) * link_flow + opt_theta * auxiliary_link_flow
            print(link_flow)
            print(new_link_flow)
            # Step 5: Check the Convergence, if FALSE, then return to Step 1
            if self.__is_convergent(link_flow, new_link_flow):
                break
            else:
                link_flow = new_link_flow
            
            counter += 1

        return new_link_flow, counter

    def __all_or_nothing_assign(self, link_flow):
        ''' Perform the all-or-nothing assignment of
            Frank-Wolfe algorithm in the User Equilibrium
            Traffic Assignment Model.
            This assignment aims to assign all the traffic
            flow, within given origin and destination, into
            the least time consuming path

            Input: link flow -> Output: new link flow
        '''
        link_time = self.__link_flow_to_link_time(link_flow)
        path_time = self.__link_time_to_path_time(link_time)
        # Find the minimal traveling time within group 
        # (splited by origin - destination pairs) and
        # assign all the flow to that path     
        path_flow = np.zeros(self.__network.num_of_paths())
        for OD_pair_index in range(self.__network.num_of_OD_pairs()):
            indice_grouped = []
            for path_index in range(self.__network.num_of_paths()):
                if self.__network.paths_category()[path_index] == OD_pair_index:
                    indice_grouped.append(path_index)
            sub_path_time = [path_time[ind] for ind in indice_grouped]
            min_in_group = min(sub_path_time)
            ind_min = sub_path_time.index(min_in_group)
            target_path_ind = indice_grouped[ind_min]
            path_flow[target_path_ind] = self.__demand[OD_pair_index]

        new_link_flow = self.__path_flow_to_link_flow(path_flow)

        return new_link_flow
        
    def __link_flow_to_link_time(self, link_flow):
        ''' Based on current self.__link_flow, use link 
            time performance function to compute the link 
            traveling time.
            The result will be recorded in self.__link_time
        '''
        n_links = self.__network.num_of_links()
        link_time = np.zeros(n_links)
        for i in range(n_links):
            link_time[i] = self.__link_time_performance(link_flow[i], self.__link_free_time[i], self.__link_capacity[i])
        print("link time: %s" % link_time)
        return link_time

    def __link_time_to_path_time(self, link_time):
        ''' Based on current link traveling time, i.e.
            self.__link_time, use link-path incidence matrix
            to compute the path traveling time.
            The result will be recorded in self.__path_time
        '''
        n_paths = self.__network.num_of_paths()
        path_time = link_time.dot(self.__network.LP_matrix()).transpose()
        print("path time: %s" % path_time)
        return path_time
    
    def __path_flow_to_link_flow(self, path_flow):
        ''' Based on current path flow, i.e. self.__path_flow,
            use link-path incidence matrix to compute the
            traffic flow on each link.
            The result will NOT be recorded in self.__link_flow
        '''
        link_flow = self.__network.LP_matrix().dot(path_flow).transpose()
        return link_flow

    def __link_time_performance(self, link_flow, t0, capacity):
        value = t0 * (1 + self._alpha * ((link_flow/capacity)**self._beta))
        return value

    def __link_time_performance_integrated(self, link_flow, t0, capacity):
        value = t0 * link_flow + self._alpha * t0 * link_flow**(self._beta + 1) / ((capacity**self._beta)*(self._beta + 1))
        return value

    def __object_function(self, mixed_flow):
        ''' Objective function in the linear search step 
            of the optimization model of user equilibrium 
            traffic assignment problem, the only variable
            is mixed_flow in this case.
        '''
        val = 0
        for i in range(self.__network.num_of_links()):
            val += self.__link_time_performance_integrated(link_flow= mixed_flow[i], t0= 
            self.__link_free_time[i], capacity= self.__link_capacity[i])
        return val

    def __golden_section(self, link_flow, auxiliary_link_flow, accuracy= 1e-6):
        LB = 0
        UB = 1
        goldenPoint = 0.618
        leftX = LB + (1 - goldenPoint) * (UB - LB)
        rightX = LB + goldenPoint * (UB - LB)
        while True:
            val_left = self.__object_function((1 - leftX) * link_flow + leftX * auxiliary_link_flow)
            val_right = self.__object_function((1 - rightX) * link_flow + rightX * auxiliary_link_flow)
            if val_left <= val_right:
                UB = rightX
            else:
                LB = leftX
            if abs(LB - UB) < accuracy:
                opt_theta = (rightX + leftX)/2.0
                return opt_theta
            else:
                if val_left <= val_right:
                    rightX = leftX
                    leftX = LB + (1 - goldenPoint) * (UB - LB)
                else:
                    leftX = rightX
                    rightX = LB + goldenPoint*(UB - LB)

    def __is_convergent(self, flow1, flow2):
        ''' Regard those two link flows lists as the point
            in Euclidean space R^n, then judge the convergence
            under given accuracy criterion
        '''
        err_rate = np.linalg.norm(flow1 - flow2) / np.linalg.norm(flow1)
        print("ERR: %.6f" % err_rate)
        if err_rate < self.__accuracy:
            return True
        else:
            return False
    
    def __dash_line(self):
        return "-" * 50 + "\n"
    
    def __str__(self):
        string = ""
        string += self.__dash_line()
        string += "LINK Information:\n"
        string += self.__dash_line()
        for i in range(self.__network.num_of_links()):
            string += "%d : link= %s, free time= %.2f, capacity= %s \n" % (i, self.__network.edges()[i], self.__link_free_time[i], self.__link_capacity[i])
        string += self.__dash_line()
        string += "OD Pairs Information:\n"
        string += self.__dash_line()
        for i in range(self.__network.num_of_OD_pairs()):
            string += "%d : OD pair= %s, demand= %d \n" % (i, self.__network.OD_pairs()[i], self.__demand[i])
        return string


