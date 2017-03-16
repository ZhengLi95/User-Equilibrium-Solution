import datetime
import data_transfer as dt
import functions as fs


#============================================================================
# You can revise the accuracy and the location of the data file as prefer

# The accuracy of the linear program solution
lp_accuracy = 1e-4

# The accuracy of the solution
cp_accuracy = 1e-8

# The location of the resource data file
data_loc = 'data.xls'

# The location of the output file
output_loc = 'output.xls'

#============================================================================


# Read the basic info from the data file:
# Create the Node-Link Incidence Matrix
NL_matrix = dt.CreateNLMatrix(data_loc)
# Create the list of capacity, t0 and demands
capacity, t0 = dt.ReadBasicData(data_loc)
demands = dt.ReadDemands(data_loc)
# Get the basic parameters - alpha & Beta
alpha, beta = dt.ReadParams(data_loc)

# Create the Link-Path Incidence Matrix
LP_matrix, paths_grouped = fs.CreateLPMatrix(NL_matrix, demands)

# Step 0: based on the x0, generate the x1
empty_link_flow = fs.GetEmptyLinkFlow(NL_matrix)
link_flow = fs.AllOrNothingAssign(empty_link_flow, LP_matrix, paths_grouped, demands, alpha, beta, t0, capacity)

counter = 0
begin = datetime.datetime.now()

while True:

    # Step 1 & Step 2: Use the link flow matrix -x to generate the time, then generate the auxiliary link flow matrix -y
    auxiliary_link_flow = fs.AllOrNothingAssign(link_flow, LP_matrix, paths_grouped, demands, alpha, beta, t0, capacity)

    # Step 3: Linear Search
    opt_theta = fs.GoldenSectionMethod(link_flow, auxiliary_link_flow, alpha, beta, t0, capacity, lp_accuracy, NL_matrix)

    # Step 4: Using optimal theta to update the link flow matrix
    new_link_flow = (1-opt_theta)*link_flow + opt_theta*auxiliary_link_flow

    # Step 5: Check the Convergence, if FALSE, then return to Step 1
    if fs.CheckConvergence(link_flow, new_link_flow, cp_accuracy):
        link_flow, link_time, path_time, vc_ratio, total_time = fs.CreateParameters4Evaluation(
            link_flow, LP_matrix, alpha, beta, t0, capacity
        )
        over = datetime.datetime.now()
        break
    else:
        link_flow = new_link_flow
        counter += 1

# Print the answers into the specific .xls file
dt.PrintAnswers2XLS(output_loc, link_flow, link_time, path_time, vc_ratio, total_time, NL_matrix, LP_matrix)

print('Iteration Times: ' + str(counter))
print('Running Time: ' + str(over-begin))





