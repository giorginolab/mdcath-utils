import h5py
import mdtraj as md
import tempfile
import numpy as np
import argparse


def convert_to_mdtraj(h5, temp, replica):
    """
    Convert data from an H5 file to an MDTraj trajectory object.

    This function extracts the first protein atom structure and coordinates 
    for a given temperature and replica from an H5 file and creates an MDTraj 
    trajectory object. This object can be used for further molecular dynamics 
    analysis.

    Parameters:
    h5 : h5py.File
        An opened H5 file object containing protein structures and simulation data.
    temp : int or float
        The temperature (in Kelvin) at which the simulation was run. This is used 
        to select the corresponding dataset within the H5 file.
    replica : int
        The replica number of the simulation to extract data from. This is used 
        to select the corresponding dataset within the H5 file.

    Returns:
    md.Trajectory
        An MDTraj trajectory object containing the loaded protein structure and 
        simulation coordinates.

    Example:
    -------
    import h5py
    import mdtraj as md

    # Open the H5 file
    with h5py.File('simulation_data.h5', 'r') as h5file:
        traj = convert_to_mdtraj(h5file, 300, 1)

    # Now 'traj' can be used for analysis with MDTraj
    """
    code = [_ for _ in h5][0]
    with tempfile.NamedTemporaryFile(suffix=".pdb") as pdbfile:
        pdb = h5[code]["pdbProteinAtoms"][()]
        pdbfile.write(pdb)
        trj = md.load(pdbfile.name)
    coords = h5[code][f"sims{temp}K"][f"{replica}"]["coords"][:]
    trj.xyz = coords.copy()/10.0
    trj.time = np.arange(1, coords.shape[0]+1)
    return trj

def convert_to_files(fn, 
                     basename=None, 
                     temp_list=[320, 348, 379, 413, 450],
                     replica_list=[0,1,2,3,4]):
    """
    Converts data from an H5 file to separate PDB and XTC files based on specified temperatures and replicas.

    This function reads protein atom structures and simulation data from an H5 file and writes a single PDB file
    and multiple XTC files. Each XTC file corresponds to a specific temperature and replica combination. The 
    function uses `convert_to_mdtraj` to generate MDTraj trajectory objects which are then saved in the XTC format.

    Parameters:
    fn : str
        The file name or path to the H5 file containing the simulation data.
    basename : str
        The base name to use for output files.  If None, it is taken from the domain ID.
    temp_list : list of int, optional
        A list of temperatures (in Kelvin) for which the simulations were run. Defaults to [320, 348, 379, 413, 450].
    replica_list : list of int, optional
        A list of replica numbers to extract data for. Defaults to [0, 1, 2, 3, 4].

    Outputs:
    Creates a PDB file named `{basename}.pdb` and multiple XTC files named `{basename}_{temp}_{replica}.xtc`, 
    where `{temp}` and `{replica}` are values from `temp_list` and `replica_list`.

    Example:
    -------
    # Convert data to files with base name 'protein_simulation'
    convert_to_files('simulation_data.h5', 'protein_simulation')
    """

    h5 = h5py.File(fn)
    code = [_ for _ in h5][0]

    if not basename:
        basename = code

    pdbpath = f"{basename}.pdb"
    with open(pdbpath, "wb") as pdbfile:
         pdb = h5[code]["pdbProteinAtoms"][()]
         pdbfile.write(pdb)
         print(f"Wrote {pdbpath}")
    
    for temp in temp_list:
        for replica in replica_list:
            xtcpath = f"{basename}_{temp}_{replica}.xtc"
            trj = convert_to_mdtraj(h5, temp, replica)
            trj.save_xtc(xtcpath)
            print(f"Wrote {xtcpath}")


def main():
    parser = argparse.ArgumentParser(description='Convert H5 file data to PDB and XTC files.')
    parser.add_argument('fn', type=str, help='File name or path to the H5 file containing simulation data.')
    parser.add_argument('--basename', type=str, help='Base name for output files, defaults to domain ID from H5 file.', default=None)
    parser.add_argument('--temp_list', type=int,  nargs='+', help='List of temperatures.',
                        default=[320, 348, 379, 413, 450])
    parser.add_argument('--replica_list', type=int, nargs='+', help='List of replicas.',
                        default=[0,1,2,3,4])
    
    args = parser.parse_args()

    convert_to_files(args.fn, args.basename, args.temp_list, args.replica_list)

if __name__ == "__main__":
    main()

