from model import TrafficFlowModel
import data as dt

mod = TrafficFlowModel(dt.graph, dt.O, dt.D, dt.demand, dt.free_time, dt.capacity)

mod.disp_detail()

mod.set_disp_precision(4)

mod.solve()

mod.report()