from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
from openmoc.options import Options
from assemblies import *

###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

options = Options()

num_threads = options.getNumThreads()
azim_spacing = 0.1
num_azim = 16
polar_spacing = 0.1
num_polar = 6
tolerance = options.getTolerance()
max_iters = options.getMaxIterations()
refines_z = 1

# 3 x 3 x 9 core to represent 3D core
lattices.append(Lattice(name='Full Geometry'))
lattices[-1].setWidth(width_x=21.42, width_y=21.42, width_z=7.14)
lattices[-1].setUniverses3D([[[assembly_rfl_unrod    , assembly_rfl_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_rfl_unrod    , assembly_rfl_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_rfl_unrod_btm, assembly_rfl_unrod_btm, assembly_rfl_unrod_cnr]],
                             [[assembly_rfl_unrod    , assembly_rfl_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_rfl_unrod    , assembly_rfl_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_rfl_unrod_btm, assembly_rfl_unrod_btm, assembly_rfl_unrod_cnr]],
                             [[assembly_rfl_unrod    , assembly_rfl_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_rfl_unrod    , assembly_rfl_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_rfl_unrod_btm, assembly_rfl_unrod_btm, assembly_rfl_unrod_cnr]],
                             [[assembly_uo2_unrod    , assembly_mox_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_mox_unrod    , assembly_uo2_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_rfl_unrod_btm, assembly_rfl_unrod_btm, assembly_rfl_unrod_cnr]],
                             [[assembly_uo2_unrod    , assembly_mox_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_mox_unrod    , assembly_uo2_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_rfl_unrod_btm, assembly_rfl_unrod_btm, assembly_rfl_unrod_cnr]],
                             [[assembly_uo2_unrod    , assembly_mox_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_mox_unrod    , assembly_uo2_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_rfl_unrod_btm, assembly_rfl_unrod_btm, assembly_rfl_unrod_cnr]],
                             [[assembly_uo2_unrod    , assembly_mox_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_mox_unrod    , assembly_uo2_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_rfl_unrod_btm, assembly_rfl_unrod_btm, assembly_rfl_unrod_cnr]],
                             [[assembly_uo2_unrod    , assembly_mox_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_mox_unrod    , assembly_uo2_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_rfl_unrod_btm, assembly_rfl_unrod_btm, assembly_rfl_unrod_cnr]],
                             [[assembly_uo2_unrod    , assembly_mox_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_mox_unrod    , assembly_uo2_unrod    , assembly_rfl_unrod_rgt],
                              [assembly_rfl_unrod_btm, assembly_rfl_unrod_btm, assembly_rfl_unrod_cnr]]])

# Refine lattice
template_2 = template
template = sum([[template_2[i]]*refines_z for i in range(len(template_2))], [])

# Fill root cell with lattice
root_cell.setFill(lattices[-1])


###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry()
geometry.setRootUniverse(root_universe)
geometry.initializeFlatSourceRegions()


###############################################################################
########################   Creating the TrackGenerator   ######################
###############################################################################

log.py_printf('NORMAL', 'Initializing the track generator...')

quad = EqualAnglePolarQuad()
quad.setNumPolarAngles(num_polar)

track_generator = TrackGenerator3D(geometry, num_azim, num_polar, azim_spacing,
                                 polar_spacing)
track_generator.setSegmentFormation(EXPLICIT_3D)
track_generator.setQuadrature(quad)
track_generator.setNumThreads(num_threads)
track_generator.generateTracks()


###############################################################################
###########################   Running a Simulation   ##########################
###############################################################################

solver = CPUSolver(track_generator)
solver.setConvergenceThreshold(tolerance)
solver.setNumThreads(num_threads)
solver.computeEigenvalue(max_iters)
solver.printTimerReport()


log.py_printf('TITLE', 'Finished')
