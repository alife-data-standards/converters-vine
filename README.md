# Standard phylogeny to Vine converter

[![Build Status](https://travis-ci.org/alife-data-standards/converters-vine.svg?branch=master)](https://travis-ci.org/alife-data-standards/converters-vine)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c5cac40b322a484592b23e44fbfb8ba9)](https://www.codacy.com/app/ALife-Data-Standards/converters-vine?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=alife-data-standards/converters-vine&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/c5cac40b322a484592b23e44fbfb8ba9)](https://www.codacy.com/app/ALife-Data-Standards/converters-vine?utm_source=github.com&utm_medium=referral&utm_content=alife-data-standards/converters-vine&utm_campaign=Badge_Coverage)

Vine is a tool developed by UBER and can be found in their github for deep-neuroevolution in the visual_inspector directory:
https://github.com/uber-research/deep-neuroevolution/ and then into the visual_inspector directory

vine allows for the visualization of populations over time.

vine is a stand alone python tool so you can just pull the visual inspector directory and it has everything you need to run vine

you can read about vine here:
https://eng.uber.com/vine/

this repository contains a converter from standard phylogeny to vine (this will create a directory called vineData/<BR>
to run the converter you must have a standard phylogeny in JSON format. vine needs its data to be formatted in a particular way so we must provide three column names which will be the x and y values in the cloud plot and the "score". vine also has the concept of parents and offspring. For each time step (i.e. generation) there is one parent (think of this as the best organism) and a collection of offspring (the rest of the population). In order to determine which organism should be the parent in each time step a parentTrait must also be provided. Please see the usage below.

vine assumes that its data is in sequential order so if your data was on 10s (ever 10 generations) and was for example 0 to 100 on 10s, this would be remapped by the converter to 0 to 10 on 1s.

to use vine you can run the following line:
```
python visual_inspector/main_mujoco.py 0 100 vineData/
```
NOTE: the '0 100' part of the command will likely need to be changed to the range of your data.

# cliff note
vine has more features, particularly the ability to find patterns in higher than 2 dimensional data and plot this data. I will eventually dig into this, but if someone wants to get their hands dirty the help would be more than welcome! (cliff)

# Usage

```
usage: stdPhylogeny2vine.py [-h] [-path PATH] [-file FILE NAME] [-verbose]
                            [-parentMethod METHOD] -parentTrait DATA NAME
                            -traits DATA NAME [DATA NAME ...]
                            [-updateColumnName DATA NAME]

Converts a JSON file in ALDS format to directories and files required for vine.

optional arguments:
  -h, --help            show this help message and exit
  -path PATH            path to files - default : none (will read files in
                        current directory)
  -file FILE NAME       name of data file !! MUST BE IN JSON FORMAT !! default
                        : lineage.json
  -verbose              adding this flag will provide more text output while
                        running (useful if you are working with a lot of data
                        to make sure that you are not hanging) - default (if
                        not set) : OFF
  -parentMethod METHOD  method used to determine parents. options are: LOD
                        (attempts to establish LOD, and uses these as
                        parents), MAX(use org with max parentTrait on each
                        update)
  -parentTrait DATA NAME
                        name of data to be used to determine parent
  -traits DATA NAME [DATA NAME ...]
                        column names of data, first two values will be x and y
                        in cloud view, third will be shown as score. others
                        will be ignored)
  -updateColumnName DATA NAME
                        name of column in source data to use for "update" in
                        vine (i.e. time)
```
