# converters-vine

Vine is a tool developed by UBER labs and can be found in their 


'''
usage: stdPhylogeny2vine.py [-h] [-path PATH] [-file FILE NAME] [-verbose]
                            [-parentMethod METHOD] -parentTrait DATA NAME
                            -traits DATA NAME [DATA NAME ...]
                            [-updateColumnName DATA NAME]

Converts a JSON file in ALDS format to directories and files reuired for vine.

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
'''
