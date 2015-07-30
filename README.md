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

The above will create a new directory containing the following:

```Bash

  README.md
  src/
      workflow.kar
  test/
       README.md
       successful_run.bats
       test_helper.bash
       bin/
           command
        
```

The **workflow** will look like the one in the screenshot below and include a single python actor redirected to a display actor

![Workflow](images/pythonworkflow.png)


