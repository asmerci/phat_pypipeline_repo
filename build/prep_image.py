#!/usr/bin/env python
import wpipe as wp
from astropy.io import fits
import os

#! - It should take the data product ID it gets handed,
#! - get the file associated with it,
#! - and run the correct DOLPHOT masking routine for the camera that produced it.
#! - Then it should run the DOLPHOT splitgroups routine on the output,.
#! - Then it should run calcsky on the output from splitgroups.
#! - Finally, it needs to make data products for all of the output files,
#! - and check to see how many other prep_image tasks have completed for the target.
#! - Check against the total, and fire a done event if it's the last one.


def register(task):
    _temp = task.mask(source="*", name="start", value=task.name)
    _temp = task.mask(source="*", name="prep_image", value="*")


if __name__ == "__main__":
    my_pipe = wp.Pipeline()
    my_job = wp.Job()

    this_event = my_job.firing_event  # parent event obj
    parent_job = this_event.parent_job
    # config_id = this_event.options["config_id"]

    # EVENT INFORMATION
    my_job.logprint(f"This Event: {this_event}")
    my_job.logprint(f"This Event Options: {this_event.options}")

    # Call drizzled image from astrodrozzle dataproduct
    this_dp_id = this_event.options["dp_id"]
    this_dp = wp.DataProduct(int(this_dp_id), group="proc")
    my_job.logprint(
        f"Data Product: {this_dp.filename}, Path: {this_dp.target.datapath}")
    # proc_dir_path = this_dp.path
    # filepath = this_dp.path + "/" + this_dp.filename
    # my_job.logprint(f"Filepath: {filepath}")
    # this_dp_fits = fits.open(this_dp.options["filename"])

    # Change directory to DOLPHOT directory
    # os.chdir('/Users/mmckay/phd_projects/phat_pipeline_dev/dolphot2.0')
    # os.system(f"dolphot")

    compname = this_event.options['compname']
    update_option = parent_job.options[compname]
    update_option += 1
    to_run = this_event.options['to_run']

    #! Fire event to make DOLPHOT parameter file
    my_event = my_job.child_event(name="param_dolphot", options={
        "target_id": this_event.options["target_id"],
    },
    )
    my_event.fire()
    # if update_option == to_run:
    #     #! Fire event to make DOLPHOT parameter file
    #     my_event = my_job.child_event(name="param_dolphot", options={
    #         "target_id": this_event.options["target_id"],
    #     },
    #     )
    #     my_event.fire()
