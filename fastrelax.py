# This script is to fast relax a bunch of pdb files
  


# init the environment
import argparse
from pyrosetta import *
from pyrosetta import pose_from_file
from pyrosetta.rosetta.core.pack.task.operation import \
    ExtraRotamers, IncludeCurrent, RestrictToRepacking
from pyrosetta.rosetta.core.simple_metrics.metrics import RMSDMetric
from pyrosetta.rosetta.protocols.constraint_generator import \
    AddConstraints, CoordinateConstraintGenerator
from pyrosetta.rosetta.core.scoring import ScoreType
from pyrosetta.rosetta.core.scoring.symmetry import SymmetricScoreFunction
from pyrosetta.rosetta.protocols.relax import FastRelax
from os.path import basename, isdir, join
from os import makedirs

# argument parser
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdb_file", help="What PDB file do you want to relax?")
    parser.add_argument("-od", "--out_dir", 
        help="Name an output directory for decoys (Default: current directory)")
    parser.add_argument('-name', "--name", 
        help="What do you want to name the relaxed PDB? (Default appends \
        '_relaxed' to original name.)")
    parser.add_argument('-n', "--n_decoys", type=int, default=100, 
        help="How many decoys do you want? (Default: 100)")
    parser.add_argument('-cst', "--constraints", default=None,
        help="If EnzDes constraints are to be applied in addition to the \
        default coordinate constraints, specify the file")
    parser.add_argument('-lig', "--ligand", default=None,
        help="If there is a ligand, specify the params file")
    parser.add_argument("-sug", "--sugars", action="store_true", 
        help="Include sugars/glycans in the model.")
    parser.add_argument('-sym', "--symmetry", default=None,
        help="If the relax should be symmetric, specify the symdef file")
    parser.add_argument('-cwt', "--constraint_weight", type=float, default=None,
        help="Specify the constraints weight for coordinates and enzdes \
        (Default: 1.0)")
    args = parser.parse_args()
    return args

def apply_res_type_constraints(pose, penalty=0.5):
    """ Apply residue type constraints to a pose """
    from pyrosetta.rosetta.protocols.protein_interface_design import \
    FavorNativeResidue

    FavorNativeResidue(pose, penalty)
    return


def apply_symmetry(pose, symfile):
    """ Set up a pose for symmetric sampling/scoring """
    from pyrosetta.rosetta.protocols.symmetry import SetupForSymmetryMover

    sfsm = SetupForSymmetryMover(symmetry)
    sfsm.apply(pose)

    return pose


def apply_membrane(pose, membfile, symmetric=False):
    """ Applies AddMembraneMover to a pose """
    from pyrosetta.rosetta.protocols.membrane import AddMembraneMover
    from pyrosetta.rosetta.protocols.membrane.symmetry import \
        SymmetricAddMembraneMover

    if symmetric:
        add_memb = SymmetricAddMembraneMover(membfile)
        add_memb.apply(pose)
    else:
        add_memb = AddMembraneMover(membfile)
        add_memb.apply(pose)

    return pose

def apply_enzdes_constraints(pose, cst_file):
    """ 
    Applies the constraints form the input CST file to a pose. Returns 
    constraied pose.
    """
    from pyrosetta.rosetta.protocols.enzdes import ADD_NEW, AddOrRemoveMatchCsts

    cstm = AddOrRemoveMatchCsts()
    cstm.set_cst_action(ADD_NEW)
    cstm.cstfile(cst_file)
    cstm.apply(pose)

    return pose

def apply_coord_constraints(pose, sidechains=False, bounded=True, selection=None):
    """ 
    Applies backbone coordinate constraints to a selection of a pose Returns 
    constraied pose.
    """
    cg = CoordinateConstraintGenerator()
    cg.set_sidechain(sidechains)

    if bounded:
        cg.set_bounded(True)
        cg.set_bounded_width(0.1)
        cg.set_sd(0.5)

    if selection:
        cg.set_residue_selector(selection)

    ac = AddConstraints()
    ac.add_generator(cg)
    ac.apply(pose)

    return pose

# Mover functions

def fast_relax_mover(score_function, task_factory=None, movemap=None, 
    repeats=5):
    """
    Creates a FastRelax mover with a given score function. If a task factory 
    and/or movemap are provided, they will also be incorporated into the mover.
    By default, FastRelax goes through five ramping cycles, but this number can 
    be adjusted with the repeats option.
    """
    from pyrosetta.rosetta.protocols.relax import FastRelax

    # Make FastRelax mover with given score function
    fr = FastRelax(repeats)
    fr.set_scorefxn(score_function)

    # Set task factory
    if task_factory:
        fr.set_task_factory(task_factory)

    # Set move map
    if movemap:
        fr.set_movemap(movemap)

    return fr

def find_maybe_compressed_file(fi, unzip_file=False, zip_file=False):
    """
    Given a filename and path for a file that may be gzipped, returns a filename
    correcting for a .gz extension. Can unzip of zip the file if desired, in 
    which case the name will correspond to the desired condition of the file.
    """
    from os.path import isfile

    # Input name is correct
    if isfile(fi):
        outname = fi

    # Input name is uncompressed, file is compressed
    elif isfile(fi + '.gz'):
        outname = fi + '.gz'

    # Input name is compressed, file is uncompressed
    elif isfile(fi.rstrip('.gz')):
        outname = fi.rstrip('.gz')

    # File wasn't found either way
    else:
        err_text = 'Cannot find this file (zipped or unzipped): \n{}'
        raise ValueError(err_text.format(fi))

    # Unzipping
    if unzip_file:
        outname = unzip_file(outname)

    # Zipping
    if zip_file:
        outname = zip_file(outname)

    return outname

def load_pose(pdb, path=None, enzdes_cst=None, coord_cst=False, res_type_cst=0, 
    symmetry=None, membrane=None):
    """
    Loads a PDB or PDB.GZ file as a pose. If the pdb argument includes the path,
    no path argument is necessary. If a pdb basename and path argument are 
    given, will attempt to load the pdb from the specified path. Accepts 
    arguments to apply enzdes constraints, full-pose CA coordinate constraints, 
    residue type constraints of a given weight, symmetry, or membrane.
    """

    # Get PDB name with path, correcting for zipped/unzipped extension
    pdb_name = pdb
    if path:
        pdb_name = join(path, pdb)
    pdb_name = find_maybe_compressed_file(pdb_name)

    # Load pose
    pose = pose_from_file(pdb_name)

    # Applying enzdes constraints
    if enzdes_cst:
        pose = apply_enzdes_constraints(pose, enzdes_cst)

    # Applying coordinate constraints
    if coord_cst:
        pose = apply_coord_constraints(pose)

    # Applying residue type constraints
    if res_type_cst:
        apply_res_type_constraints(pose, penalty=res_type_cst)

    # Applying symmetry
    if symmetry: 
        pose = apply_symmetry(pose, symmetry)

    # Set up membrane
    if membrane:
        pose = apply_membrane(pose, membrane, symmetric=symmetry)

    return pose

def out_directory(path):
    if path == None:
        return './'
    elif not isdir(path):
        makedirs(path)
        return path

################################################################################
# Scoring functions

def get_sf(rep_type='hard', symmetry=False, membrane=0, constrain=1.0, 
    hbnet=0):
    """
    Determines the appropriate score function to use, based on a rep_type
    that is either hard (ref2015) or soft (ref2015_soft), whether symmetry 
    and/or membrane modeling are in use, and whether constraints are desired.
    If setting membrane and/or hbnet, change value to desired nonzero weight.
    """
    from pyrosetta import create_score_function, ScoreFunction
    from pyrosetta.rosetta.core.scoring import ScoreType
    from pyrosetta.rosetta.core.scoring.symmetry import SymmetricScoreFunction

    score_types = {'hard': 'ref2015', 'soft': 'ref2015_soft'}
    assert rep_type in score_types

    # Create base empty score function symmetrically or asymmetrically
    if symmetry: # Declare symmetric score functions
        score_function = SymmetricScoreFunction()
    else:
        score_function = ScoreFunction()

    # Add main score weights
    if rep_type == 'hard':
        score_function.add_weights_from_file('ref2015')
    elif rep_type == 'soft':
        score_function.add_weights_from_file('ref2015_soft')
        if membrane: # Set up a soft-rep version of franklin2019 manually
            score_function.set_weight(ScoreType.fa_water_to_bilayer, membrane)

    # Add membrane weights if appliccable
    if membrane:
        score_function.add_weights_from_file('franklin2019')

    # The score functions do not have constraint weights incorporated in 
    # themselves. If requisite, the constraint weights are added.
    if constrain:
        score_function.set_weight(ScoreType.atom_pair_constraint, constrain)
        score_function.set_weight(ScoreType.coordinate_constraint, constrain)
        score_function.set_weight(ScoreType.angle_constraint, constrain)
        score_function.set_weight(ScoreType.dihedral_constraint, constrain)
        score_function.set_weight(ScoreType.metalbinding_constraint, constrain)
        score_function.set_weight(ScoreType.chainbreak, constrain)
        score_function.set_weight(ScoreType.res_type_constraint, constrain)

    # Optionally adding in hbnet
    if hbnet:
        sf.set_weight(ScoreType.hbnet, hbnet)

    return score_function

def main(args):
    # Destination folder for PDB files
    od = out_directory(args.out_dir)

    # Determining file name
    if args.name: 
        file_name = args.name
    else:
        file_name = basename(args.pdb_file).replace('.pdb', '').replace('.gz', '')
        file_name += '_relaxed'

    out_name = join(od, file_name)

    # Loading pose and applying constraints, symmetry, 
    pose = load_pose(args.pdb_file, enzdes_cst=args.constraints, 
        coord_cst=True, symmetry=args.symmetry, membrane=None)

    # Setting up the scorefunction with the desired constraint weights
    sf = get_sf(rep_type='hard', symmetry=args.symmetry, membrane=0, 
        constrain=args.constraint_weight)

    # Creating FastRelax protocol with the given score function
    fr = FastRelax()
    fr.set_scorefxn(sf)

    # Packer tasks
    tf = standard_task_factory()
    tf.push_back(RestrictToRepacking())
    tf.push_back(IncludeCurrent())
    tf.push_back(ExtraRotamers(0, 1, 1))
    tf.push_back(ExtraRotamers(0, 2, 1))
    fr.set_task_factory(tf)

    # RMSD metric
    rmsdm = RMSDMetric()
    rmsdm.set_comparison_pose(pose)

    # Running relax set
    jd = PyJobDistributor(out_name, args.n_decoys, sf)
    while not jd.job_complete:
        pp = Pose(pose)
        fr.apply(pp)
        rmsdm.apply(pp)
        jd.output_decoy(pp)



    print("Starting relax {}".format(pdb_name))
    pose = fastrelax(pose, sf, mm, taskfactory=tf)
    
if __name__ == '__main__':
    args = parse_args()

    opts = '-ex1 -ex2 -use_input_sc -flip_HNQ -no_optH false'
    if args.constraints:
        opts += ' -enzdes::cstfile {}'.format(args.constraints)
        opts += ' -run:preserve_header'
    if args.ligand:
        opts += ' -extra_res_fa {}'.format(args.ligand)
    if args.sugars:
        opts += ' -include_sugars'
        opts += ' -auto_detect_glycan_connections'
        opts += ' -maintain_links '
        opts += ' -alternate_3_letter_codes rosetta/Rosetta/main/database/input_output/3-letter_codes/glycam.codes'
        opts += ' -write_glycan_pdb_codes'
        opts += ' -ignore_zero_occupancy false '
        opts += ' -load_PDB_components false'
        opts += ' -no_fconfig'
    init(opts)

    main(args)
