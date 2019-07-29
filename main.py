from model import TrafficFlowModel
import data as dt

# Initialize the model by data
mod = TrafficFlowModel(dt.graph, dt.origins, dt.destinations, 
dt.demand, dt.free_time, dt.capacity)

# Change the accuracy of solution if necessary
mod._conv_accuracy = 1e-6

# Display all the numerical details of
# each variable during the iteritions
mod.disp_detail()

# Set the precision of display, which influences
# only the digit of numerical component in arrays
mod.set_disp_precision(4)

# Solve the model by Frank-Wolfe Algorithm
mod.solve()

# Generate report to console
mod.report()

# Return the solution if necessary
mod._formatted_solution()