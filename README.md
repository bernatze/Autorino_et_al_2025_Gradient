Code scripts for the generation of 2D cell tilings and lattices used in
Autorino C. et al 2025, "A closed feedback between tissue phase transitions and morphogen gradients drives patterning dynamics"

Brief description:

"Lattice_Non_Uniform_Prob.py" generates networks with and without connectivity gradient,
--recall that "pebble.py" ( https://github.com/coldlaugh/pebblegame-algorithm/blob/master/pebble.pyx.) and "lattice.py" are needed for this file to run. 
The scripts "Generate_random_tiling_Mono_exact.py" and "Run_tiling_Rand_2D_exact.py" 
create the cell tilings to be read for the surface evolver software 
"Sim_RandomWeilbull_Sequential.py" generates a .fe file that, using Surface Evolver, makes the tiling evolve without alpha gradient. 
"Sim_RandomWeibull_alphagradient.py" generates a file that makes the tiling evolve with alpha gradient.
