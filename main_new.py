from model import TrafficFlowMod
import data as dt

mod = TrafficFlowMod(dt.graph, dt.O, dt.D, dt.demand, dt.free_time, dt.capacity)

ret = mod.solve()

print(ret[0])
print(ret[1])
