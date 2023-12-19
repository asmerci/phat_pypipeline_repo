#!/usr/bin/env python
"""
Run Fakestars Task Description:
-------------------
This script is a component of a data processing pipeline designed for Flexible Image Transport System (FITS) files. It carries out several key tasks:

1. Retrieves the target and configuration associated with the job. The target is retrieved from the options of the firing event, and the configuration is used to set up the processing and logging paths.

2. Retrieves the data product for the fake star list from the event.

3. Retrieves the parameter file from the configuration dataproducts.

4. Generates a new parameter file with the fakestar parameters populated, including the name of the fakestar list.

5. Generates the necessary symbolic links to run an independent fake star run with the same data as was used for the original photometry run by run_dolphot.

6. Constructs and executes the Dolphot command using the parameters from the parameter file. The output of the Dolphot operation is logged to a file.

7. The DOLPHOT output from the fake stars is given a data product and counted to see if it is the last one in the group. If it is the last one, as event is fired. 

This script relies on the 'wpipe' library, a Python package designed for efficient pipeline management and execution.
"""

# Original script by Shellby Albrecht
# Modified by Myles McKay
import wpipe as wp
import os
import time
import sys
import subprocess
from glob import glob
# from astropy.io import fits


def register(task):
    _temp = task.mask(source="*", name="start", value=task.name)
    _temp = task.mask(source="*", name="new_fakestars", value="*")

import signal
def handler(signum, frame):
    print("Forever is over!")
    raise ValueError("end of time")

if __name__ == "__main__":
    my_pipe = wp.Pipeline()
    my_job = wp.Job()
    my_config = my_job.config
    my_target = my_job.target
    this_event = my_job.firing_event
    run_number = this_event.options["run_number"]
    to_run = this_event.options["to_run"]
    my_job.logprint(run_number)
    my_job.logprint(to_run)
    my_job.logprint(this_event.options)
    my_config = my_job.config
    logpath = my_config.logpath
    procpath = my_config.procpath

    # Get parameter file
    param_dp = wp.DataProduct.select(config_id=my_config.config_id, subtype="parameter")
    my_job.logprint(f'{param_dp.filename} is the original parameter file')

    param_path = param_dp.relativepath
    param_filename = param_dp.filename
    paramfile = param_path + "/" + param_filename
    paramcontents = np.loadtxt(paramfile)
    #make new parameter file with the fake star parameters set
    newsuf = "fakepar"+str(run_number)
    fake_param_filename = param_filename
    fake_param_filename.replace("param",newsuf)
    fake_param = param_file
    fake_param.replace("param",newsuf)
    with open(fake_param, 'w') as f:
        for line in paramcontents:
            f.write(line)
        f.write("FakeStars={fakelist}")    
        f.write("FakeMatch=2")    
        f.write("FakePSF=1.5")
    my_job.logprint(f'{fake_param} is the fakestar parameter file')  
    wp.DataProduct(my_config, filename=fake_param_filename, group="conf", data_type="fakepars", subtype="fake_param")
    #grab all the dolphot data products, to use for making links with run number
    dolphot_dps = wp.DataProduct.select(config_id=my_config.config_id, subtype="dolphot output")
    for dp in dolphot_dps:
        new_name = dp.filename
        new_name.replace("phot", "phot_"+str(run_number))
        link_command = "ln -s "+dp.filename+" "+procpath+"/"+new_name
        my_job.logprint(f'making link: {link_command}')
        os.system(link_command) 
        
    # # Run Dolphot
    dolphotout = procpath + "/" + my_target.name + ".phot" + "_" + str(run_number)
    logdp = my_job.logprint()
    logfile = logpath + "/" + logdp.filename
    my_job.logprint(f"Running DOLPHOT on {fake_param} and {dolphotout}")
    dolphot_command = "cd "+procpath+" && " + \
        my_config.parameters["dolphot_path"]+"dolphot " + dolphotout + \
        ' -p' + param_path + "/" + param_filename + " > "+logfile
    my_job.logprint(dolphot_command)
    dolphot_output = os.system(dolphot_command)
    # check that this gets file called just dolphotout
    phot_dp = wp.DataProduct(my_config, filename=dolphotout+".fake", group="proc", subtype="fake output")

    my_job.logprint(
        f"Created dataproduct for {dolphotout}.fake, {phot_dp}")
    compname = this_event.options["comp_name"]
    update_option = parent_job.options[compname]
    update_option += 1
    to_run = this_event.options["to_run"]
    my_job.logprint(f"parent_job options: {parent_job.options}")
    my_job.logprint(f"{update_option}/{to_run} TAGGED")

    if update_option == to_run:
        next_event = my_job.child_event(
          name="fakestars_done",
          options={"config_id": my_config.config_id, "memory": "150G"}
        )  # next event
        next_event.fire()
        time.sleep(150)

    
