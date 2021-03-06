#!/usr/bin/env python3
import multiprocessing
# Custom modules.
from . import md_system
from . import bin_table
from . import p2_parameters


def possible_crys_atoms(mds, bins, inp):
    """ Manage child processes to identify possible crystalline atoms.
    """
    # Number of child processes.
    n_proc = multiprocessing.cpu_count()
    
    ''' Create and submit jobs. '''
    jobs  = [None for _ in range(n_proc)]
    pipes = [None for _ in range(n_proc)]
    master_pca = []

    # Partition atoms for parallel processing.
    chunked_atoms = md_system.distribute_atoms(range(mds.n_atom), n_proc)

    # Initialize a list to store the ids of possible crystalline atoms
    # (pca) for every child process.
    L   = max([len(_) for _ in chunked_atoms])  # Length of pca.
    pca = [-1 for _ in range(L)]

    for i in range(n_proc):
        loc_atoms = chunked_atoms[i]

        # Create and submit jobs.
        parent, child = multiprocessing.Pipe(duplex=False)
        p = multiprocessing.Process(
                name   = 'local-rank_{}'.format(i),
                target =  parallel_job,
                args   = (mds, bins, inp, loc_atoms, pca, child))
        p.start()
        child.close()
        jobs[i]  = p
        pipes[i] = parent

    for i,parent in enumerate(pipes):
        # SEQUENTIALLY wait for each child process to complete and collect data
        master_pca.extend(parent.recv())
        jobs[i].join()

    master_pca = list(set(master_pca))  # Trim additional -1s.
    master_pca.remove(-1)
    return master_pca  # 0-indexed.

def parallel_job(mds, bins, inp, loc_atoms, pca, child):
    """ Identify possible crystalline atoms and modify pca.
    """
    proc = multiprocessing.current_process().name
    p2_parameters.p2_parameters(mds, bins, inp, loc_atoms, pca, proc)
    child.send(pca)  # Send to the parent end of pipe.
    child.close()


if __name__ == '__main__':
    pass
