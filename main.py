from SNP_Simulator import SNP_Simulator

simulator = SNP_Simulator(total_flow=2, num_fractions=20)

order, _ = simulator.run_simulation()
simulator.save_results(order, fps=25)