from evo.core import metrics
from evo.core.units import Unit
from evo.tools import log
log.configure_logging(verbose=True, debug=True, silent=False)

import pprint
import numpy as np

from evo.tools import plot
import matplotlib.pyplot as plt

# temporarily override some package settings
from evo.tools.settings import SETTINGS
SETTINGS.plot_usetex = False

plot.apply_settings(SETTINGS)
# %matplotlib inline
# %matplotlib widget  # For vscode: % matplotlib widget

from evo.tools import file_interface

ref_file = "GPS.txt"
est_file = "ORBSLAM3.txt"

traj_ref = file_interface.read_tum_trajectory_file(ref_file)
traj_est = file_interface.read_tum_trajectory_file(est_file)

from evo.core import sync

max_diff = 0.5

traj_ref, traj_est = sync.associate_trajectories(traj_ref, traj_est, max_diff)

import copy

traj_est_aligned = copy.deepcopy(traj_est)
traj_est_aligned.align(traj_ref, correct_scale=True, correct_only_scale=False)

fig = plt.figure()
traj_by_label = {
    "estimate (aligned)": traj_est_aligned,
    "reference": traj_ref
}
plot.trajectories(fig, traj_by_label, plot.PlotMode.xz)
plt.show()

pose_relation = metrics.PoseRelation.point_distance

# normal mode
delta = 1
delta_unit = Unit.frames

# all pairs mode
all_pairs = False  # activate

data = (traj_ref, traj_est_aligned)

rpe_metric = metrics.RPE(pose_relation=pose_relation, delta=delta, delta_unit=delta_unit, all_pairs=all_pairs)
rpe_metric.process_data(data)

rpe_stats = rpe_metric.get_all_statistics()
pprint.pprint(rpe_stats)

