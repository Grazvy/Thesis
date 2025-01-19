from SNP_Simulator import SNP_Simulator

#simulator = SNP_Simulator(total_flow=2, num_fractions=10)
simulator = SNP_Simulator(total_flow=3, num_fractions=100)

order, _ = simulator.run_simulation()
#simulator.save_results(order, fps=15)
simulator.save_results(order, fps=60, steps=8)
