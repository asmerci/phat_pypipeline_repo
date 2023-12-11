# phat_pypipeline_repo

# Authors:

- Myles McKay
- Ben Williams
- Shelby Albrecht
- Adrien Thob
- Tristan
- Zhuo Chen

# Description:

Photometry pipeline for HST and JWST data products. The pipeline has a similar structure to AWS based photomerty pipeline by Ben Williams and Keith Rosema but simplifies it by being written in Python.

# How it works

- User stores there HST and JWST calibrated dataproducts ('\*flc.fits') in a directory called 'Unsorted'

## Workflow

The workflow gives instructions on the steps you should take to get started with the sample pipeline. The steps are as follows:

```mermaid
graph LR

sort.py --> tag_image.py --> astrodrizzle.py --> find_reference.py --> prep_image.py --> make_param.py --> run_dolphot.py

```

## Layout``

| Task              | Description                                      | Link                                  |
| ----------------- | ------------------------------------------------ | ------------------------------------- |
| sort.py           | Sort all the input image by target               | [Click Here](build/sort.py)           |
| tag_image.py      | Steps to set up GKE and AKS                      | [Click Here](build/tag_image.py)      |
| astrodrizzle.py   | Steps to set up the Harness Delegate             | [Click Here](build/astrodrizzle.py)   |
| find_reference.py | Learn about Secrets and steps to set them up     | [Click Here](build/find_reference.py) |
| prep_image.py     | Steps the to set up Docker and GitHub Connectors | [Click Here](build/prep_image.py)     |
| make_param.py     | Steps the to set up Docker and GitHub Connectors | [Click Here](build/make_param.py)     |
| run_dolphot.py    | Steps the to set up Docker and GitHub Connectors | [Click Here](build/run_dolphot.py)    |

_Important Note_

All input FITS files must be in a directory called Unsorted/ to work properly
