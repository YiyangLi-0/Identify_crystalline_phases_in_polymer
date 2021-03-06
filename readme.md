# Objective

A distributed computing algorithm is developed to identify the crystalline and amorphous phases in a coarse-grained polymer system (coarse-grained linear polyethylene).
Distributed computing is separately implemented in both MPI (message passing interface) mode and multiprocessing mode. 
The bin-table technique is used in both modes to further improve computing efficiency. 
The [local p2 order parameter][ref-1] is computed for every particle in system, which is used to determine if a particle should be assigned to the crystalline phase.
The identified system is output in both wrapped and unwrapped coordinates.

This postprocessing code was used in my research projects #6 and #7, as shown in [my webpage](https://liyiyang.weebly.com/).


# Prerequisites

### MPI mode

&nbsp;&nbsp;&nbsp;&nbsp;1. Open MPI or MPICH or Intel MPI <br />
&nbsp;&nbsp;&nbsp;&nbsp;2. python3, numpy, mpi4py <br />

These packages should be installed on the master node as well as all the worker nodes in your cluster.

In addition, master node and worker nodes should have access to the folder of this project through network file system (NFS), and any node should be able to passwordlessly ssh to any other node in your network. 
Please read this [tutorial](https://www-users.cs.york.ac.uk/~mjf/pi_cluster/src/Building_a_simple_Beowulf_cluster.html#_install_and_setup_the_network_file_system) for more information.

### Multiprocessing mode

&nbsp;&nbsp;&nbsp;&nbsp;python3, numpy


# Usage

### MPI mode

Run distributed computing on all the worker nodes in your network.
The master node can also be utilized along side the worker nodes (this can be changed by modifying the ![hosts](./run/hosts) file.)

This program is tested with OpenMPI 3.0.1 and mpi4py 3.0.0 on Ubuntu 18.04.
As there is a [default mpiexec (1.10)](https://launchpad.net/ubuntu/bionic/+package/mpi-default-bin) shipped with Ubuntu 18.04, we need to specify the correct path of mpiexec to correctly run the program (we can also set symlink or alias).
Usage:
```
cd run
path/to/mpiexec -np <n> python3 ../src/main.py mpi
```
or
```
cd run
path/to/mpiexec --hostfile ./hosts -np <n> python3 ../src/main.py mpi
```
where `<n>` is the number of physical cores in your cluster.
To use the `--hostfile` option, you need to modify the ![hosts](./run/hosts) file to accommodate the setting of your cluster.

This program assumes that cores in every compute node have approximately equal computing power.
If the computing power of cores in different nodes are unequal, then to get best performance we can specify uneven workloads to different processes in our code, and use a ![ranks](./run/ranks) file to assign specific processes to specific cores:
```
cd run
path/to/mpiexec --hostfile ./hosts --rankfile ./ranks -np <n> python3 ../src/main.py mpi
```

#### Note

To make sure MPI uses both distributed-memory (inter-node communication) and shared-memory (intra-node communication) for efficient message passing, we can explicitly turn on the [vader BTL (Byte Transfer Layer)](https://www.open-mpi.org/faq/?category=sm) by adding the switch `--mca btl self,vader,tcp`.


### Multiprocessing mode

Run parallel computing only on your local node (ie, your workstation). Usage:
```
cd run
python3 ../src/main.py mp
```


# Code structure

. <br />
├── src <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── main.py <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── modules <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── __init__.py <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── parser.py <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── md_system.py <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── bin_table.py <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── identify_mpi.py <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── identify_mp.py <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── p2_parameters.py <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── postprocess.py <br />
├── data <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── cg-80blk-50chain.lammps <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── cg-80blk-50chain-1atm-300K-40ns.lammpstrj <br />
├── run <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── hosts <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── ranks <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── input <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── screen_output.png <br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── image.png <br />
└── vmd_scripts <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── color_scale.vmd <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── setuserfield.vmd


#### src/main.py

Main script that initializes input parameters, and launches either MPI or multiprocessing jobs to identify crystalline particles in polymer system.

#### src/modules/parser.py

Script providing functions to read parameters from the input file 'input'.

#### src/modules/md_system.py

A class to store molecular information of a coarse-grained linear polyethylene system.

#### src/modules/bin_table.py

A class to generate a bin table for a polymer system.

#### src/modules/identify_mpi.py

Script using MPI to identify possible crystalline particles, utilizing all worker nodes in cluster.

#### src/modules/identify_mp.py

Script using multiprocessing to identify possible crystalline particles, utilizing only master node.

#### src/modules/p2_parameters.py

Script to calculate local p2 order parameter for each atom i in a list of local particles to be handled by a parallel process.

#### src/modules/postprocess.py

Script to run on master process, that completes the identification of crystalline particles.

#### data/cg-80blk-50chain.lammps

A LAMMPS data file for a reference state of a polymer system.

#### data/cg-80blk-50chain-1atm-300K-40ns.lammpstrj

A LAMMPS trajectory file containing two snap shots (or time steps) of the evolution of the polymer system defined by the LAMMPS data file.

#### run/hosts

Configuration file listing all the nodes that will be used for distributed computing.

#### run/ranks

Configuration file that specifies which process/rank uses which core on which node.

#### run/input

Input file containing required parameters.

#### run/screen_output.png

A screenshot of output for the MPI mode.

#### run/image.png

An example randering of the polymer system with VMD. <br />

#### vmd_scripts/color_scale.vmd

A VMD script to define a custom color scale used for rendering crystalline particles (blue) and amorphous particles (yellow) at all time steps listed in the trajectory file.

#### vmd_scripts/setuserfield.vmd

A VMD script to set the values of 'user' field as the values in the 'vx' column of LAMMPS trajectory file, at every time step listed in the trajectory file.

### File output

After executing the code, an 'output' folder will be created under the 'run' folder, which contains four files:

. <br />
└── run <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── output <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── identified_wrapped.lammpstrj <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── identified_unwrapped.lammpstrj <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├── identified_crystalline_atoms <br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── crystallinty

#### run/output/identified_wrapped.lammpstrj

A LAMMPS trajectory file in which molecules/chains are wrapped into simulation box according to periodic boundary conditions; a 'vx' column is used to indicate if a particle belongs to crystalline phase.

#### run/output/identified_unwrapped.lammpstrj

A LAMMPS trajectory file in which molecules/chains are not wrapped into simulation box; a 'vx' column is used to indicate if a particle belongs to crystalline phase.

#### run/output/identified_crystalline_atoms

Each line lists the IDs of particles belongs to a crystalline chunk, for every time step listed in the trajectory file.
IDs are sorted according to particle connectivity.

#### run/output/crystallinty

Lists the crystallinty of polymer system at every time listed in the trajectory file.


# Example screen output (MPI mode)

I use a cluster with a master node and three compute nodes (cpnd-[0-2]), as listed in the ![hosts](./run/hosts) file.
The master node has 6 cores, while each compute node has 2 cores.
To use all the 12 cores for distribured computing, my computation is conducted by launching 12 parallel processes:
```
cd run
path/to/mpiexec --mca btl self,vader,tcp --hostfile ./hosts -np 12 python3 ../src/main.py mpi
```

which gives following screen output

![Screen output.](./run/screen_output.png)


# Visualization

I use VMD to visualize the identified polymer system.
For this, I installed:

&nbsp;&nbsp;&nbsp;&nbsp;1. tachyon <br />
&nbsp;&nbsp;&nbsp;&nbsp;2. VMD

Then open the VMD GUI interface with
```
cd run
vmd output/identified_wrapped.lammpstrj 
```
is opened. Now modify some settings as stated below: 

'Display' -> check 'Orthographic' <br />
'Display' -> uncheck 'Depth Cueing' <br />
'Display' -> 'Axes' -> 'Off'

'Extensions' -> 'Tk Console', this opens a console, from where execute these commands:
```
  play ../vmd_scripts/color_scale.vmd
  play ../vmd_scripts/setuserfield.vmd
  pbc box -center unitcell -shiftcenter {0.168269 0.168269 0.168269}  -color gray
```

'Graphics' -> 'Representations...', this opens a new panel: <br />
&nbsp;&nbsp;&nbsp;&nbsp;Modify 'Coloring Method' to 'Trajectory' -> 'User' -> 'User' <br />
&nbsp;&nbsp;&nbsp;&nbsp;Modify 'Drawing Method' -> 'VDW' (Sphere Scale 0.7) <br />
&nbsp;&nbsp;&nbsp;&nbsp;Modify 'Material' -> 'AOShiny' <br />
&nbsp;&nbsp;&nbsp;&nbsp;Click  'Create Rep' <br />
&nbsp;&nbsp;&nbsp;&nbsp;Modify 'Drawing Method' -> 'DynamicBonds' (Distance Cutoff 2.7)

'Display' -> 'Display Settings' -> check 'Shadows' On <br />
'Display' -> 'Display Settings' -> Check 'Amb. Occl.' On

'Graphics' -> 'Colors...' -> Categories 'Display' -> Names 'Background' -> Colors '8 White'

'Extensions' -> 'Tk Console', execute following command to render an image file:
```
   render Tachyon vmdscene.dat tachyon -aasamples 24 -fullshade -res 1000 1000 %s -format PNG -o image.png
```
Here are some example images rendered for the wrapped and unwrapped systems.
Images on the left are for time step 0.5 ns, and images on the right are for time step 40.0 ns, where yellow beads belong to amorphous phase and blue beads belong to crystalline phase.
![Example rendering.](./run/image.png)


[ref-1]: http://aip.scitation.org/doi/abs/10.1063/1.3608056?journalCode=jcp
