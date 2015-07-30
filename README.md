[kepler]: https://kepler-project.org/
[cookiecutter]: https://github.com/audreyr/cookiecutter

cookiecutter-keplerpython
===========================

Cookiecutter template for a Kepler Workflow that runs a Python
script within the Python Actor. The workflow is compatible with CRBS
Workflow Service See:  https://github.com/audreyr/cookiecutter.


Usage
=====

Generate a Kepler Workflow project:

```Bash

cookiecutter https://github.com/slash-segmentation/cookiecutter-keplerpython

```

Workflow
========

The above will create a new workflow source tree that looks like the following:

```Bash

  README.md
  src/
      (repo name).kar
  test/
       README.md
       successful_run.bats
       test_helper.bash
       bin/
           command
        
```

* src/(repo name).kar

** This is the actual [Kepler][kepler] workflow.  The file name is set to the value set for **repo_name** when running [cookiecutter][cookiecutter] to generate the source tree. 

* test/

** Contains bats unit test to run the [Kepler][kepler] workflow via the command line and verify correct operation.

The **workflow** will look like the one in the screenshot below and include a single python actor redirected to a display actor

![Workflow](images/pythonworkflow.png)

Python Actor
============

Currently within the **Python Actor** is the following code.  The **fire** method is invoked by [Kepler][kepler].

```Python

# This is a simple actor that copies the input to the output.
# You can remove the ports, add new ports, and modify the script.

import ptolemy.data
import time
import os


class Main :
  """Skeleton Actor compatible with CWS"""
  def fire(self) :
    """Skeleton implementation that follows best practices for CWS
        
        
    """       
    # Write out README.txt file with information about workflow
    readme = ReadMe(self)
    
    # appends more text to README.txt file
    readme.append('hi\n')

    # Create workflow.status file
    status = WorkflowStatus(self)
   
    # updates workflow.status file 
    # see WorkflowStatus class below for methods to update
    # status
    status.update()

    # grab input as a string but first check there is a token even
    # there
    input_val = ''
    if self.mycmd.numberOfSources() > 0:
      input_val = self.mycmd.get(0).stringValue()

    text_val = ''

    if self.text.numberOfSources() > 0:
      text_val = self.text.get(0).stringValue()

    # Output common CWS parameters to debug if enabled
    self.output_parameters()


    # write input back out as string
    self.output.broadcast(ptolemy.data.StringToken(input_val + ' : ' + text_val))
    

    return

  def output_parameters(self):
    """If debuging is enabled output CWS parameters"""
    if self.actor.isDebugging() :
      self.actor.debug(self.cws_outputdir.stringValue())
      self.actor.debug(self.cws_user.stringValue())
      self.actor.debug(self.cws_jobname.stringValue())
      self.actor.debug(self.cws_jobid.stringValue())
      self.actor.debug(self.cws_workflowname.stringValue())
      self.actor.debug(self.cws_notifyemail.stringValue())


class WorkflowFailed:
  """Generates Workflow Failed file"""
  def __init__(self,main_self):
    """Constructor"""
    self._failed_file = os.path.join(main_self.cws_outputdir.stringValue(), 'WORKFLOW.FAILED.txt')

  def write_failed_file(self,simple_message,detailed_message):
    """Writes WORKFLOW.FAILED.txt file"""
    out = open(self._failed_file,'w')
    out.write('simple.error.message=' + simple_message + '\n')
    out.write('detailed.error.message=' + detailed_message + '\n')
    out.flush()
    out.close()


class ReadMe:
  """Opens and appends to README.txt file"""

  def __init__(self, main_self):
    """Constructor"""
    self._mainself = main_self
    self._readmepath = os.path.join(self._mainself.cws_outputdir.stringValue(), 'README.txt')
    self._write_readme_header()

  def append(self, str):
    """Appends to readme.txt file"""
    readme = open(self._readmepath,'a')
    readme.write(str)
    readme.flush()
    readme.close()

  def _write_readme_header(self):
    """Writes README.txt header"""
    readme = open(self._readmepath, 'w')
    readme.write(self._mainself.cws_workflowname.stringValue() + '\n\n')
    readme.write('Job Name: ' + self._mainself.cws_jobname.stringValue() + '\n')
    readme.write('User: ' + self._mainself.cws_user.stringValue() + '\n')
    readme.write('Notify Email: ' + self._mainself.cws_notifyemail.stringValue() + '\n')
    readme.write('Workflow Job Id: ' + self._mainself.cws_jobid.stringValue() + '\n')
    readme.write('\nTODO: Add additional parameters here \n')
    readme.write('\n\n')
    readme.write('------------------------------------------\n\n')
    readme.write('Below is a description of files generated by the ' + self._mainself.cws_workflowname.stringValue() + ':\n\n')
    readme.write('WORKFLOW.FAILED.txt\n')
    readme.write('  -- If exists, the workflow failed.  Contents of this file describes the error.\n')
    readme.write('\nTODO: Add descriptions of additional files created by this workflow here \n')
    readme.write('\nOutput Log of Job\n==========================\n')
    readme.flush()


class WorkflowStatus:
  """Contains status information about Running Workflow"""

  def __init__(self,main_self):
    """Constructor"""
    self._cws_outputdir_str = main_self.cws_outputdir.stringValue()
    self._workflow_status_path = os.path.join(self._cws_outputdir_str, 'workflow.status')
    self._est_wall_seconds = '0'
    self._est_wall_seconds_help = 'Estimated walltime this job will run'
    self._est_total_cpu_seconds = '0'
    self._est_total_cpu_seconds_help = 'Estimated total cpu in seconds this workflow will consume'
    self._est_total_diskspace = '0'
    self._est_total_diskspace_help = 'Estimated total diskspace in bytes'
    self._phase = 'Unknown'
    self._phase_help = ''
    self._phase_list = 'Unknown'
    self._phase_list_help = 'Comma delimited list of phases this workflow runs through'
    self._cpu_seconds_per_cluster_list = ''
    self._cpu_seconds_per_cluster_list_help = 'Amount of cpu consumed in seconds per cluster'
    self._disk = '0'
    self._disk_help = 'Diskspace consumed by job'


  def _open(self):
    """Opens workflow.status file"""
    self._workflow_status_handle = open(self._workflow_status_path,'w')
    return self._workflow_status_handle
   
  def _close(self):
    """Flushes and closes workflow.status file"""
    if self._workflow_status_handle:
      self._workflow_status_handle.flush()
      self._workflow_status_handle.close()
     
  def set_est_walltime(self, walltime):
    self._est_wall_seconds = walltime

  def set_est_total_cpu(self, totalcpu):
    self._est_total_cpu_seconds =totalcpu

  def set_est_total_diskspace(self, diskspace):
    self._est_total_diskspace = diskspace

  def set_phase(self, phase):
    self._phase = phase

  def set_phase_help(self, phasehelp):
    self._phase_help = phasehelp

  def set_cpu_per_cluster(self, cpu):
    self._cpu_seconds_per_cluster_list = cpu

  def set_diskspace(self, diskspace):
    self._diskspace = diskspace

  def update_phase(self, phase):
    self.set_phase(phase)
    self.update()

  def update(self):
    """Updates workflow.status file with changes"""
    writer = self._open()

    writer.write('#Time this file was updated\n')
    writer.write('time = ' + str(int(time.time())) + '\n\n')

    writer.write('# This is the wall time the workflow will take to run\n')
    writer.write('estimated.walltime.seconds = ' + str(self._est_wall_seconds) + '\n')
    writer.write('estimated.walltime.seconds.help = ' + self._est_wall_seconds_help + '\n\n')

    writer.write('# This is the estimated total cpu time the workflow will take to run\n')
    writer.write('estimated.total.cpu.seconds = ' + str(self._est_total_cpu_seconds) + '\n')
    writer.write('estimated.total.cpu.seconds.help = ' + self._est_total_cpu_seconds_help + '\n\n')

    writer.write('# Estimated total disk space for job\n')
    writer.write('estimated.total.diskspace = ' + str(self._est_total_diskspace) + '\n')
    writer.write('estimated.total.diskspace.help = ' + self._est_total_diskspace_help + '\n\n')

    writer.write('# Denotes current phase of processing, should be a phase in phase.list below\n')
    writer.write('phase = ' + self._phase + '\n')
    writer.write('phase.help = ' + self._phase_help + '\n\n')

    writer.write('# Lists the phases that this workflow runs through\n')
    writer.write('phase.list = ' + self._phase_list + '\n')
    writer.write('phase.list.help = ' + self._phase_list_help + '\n\n')

    writer.write('#\n# the format of this field is clustername:seconds,clustername:seconds\n')
    writer.write('# If clustername is not known just use \'unknown\'\n#\n')
    writer.write('cpu.seconds.consumed.per.cluster.list = ' + self._cpu_seconds_per_cluster_list + '\n')
    writer.write('cpu.seconds.consumed.per.cluster.list.help = ' + self._cpu_seconds_per_cluster_list_help + '\n\n')

    writer.write('# Actual disk space consumed by Workflow\n')
    writer.write('diskspace.consumed = ' + str(self._disk) + '\n')
    writer.write('diskspace.consumed.help = ' + self._disk_help + '\n')

    self._close() 


```
