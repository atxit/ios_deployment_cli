# Jinja2 using MS excel

This is a tool that I created to build Cisco configuration files using a jinja2 template. Using a jinja2 template to create configuration files is nothing new however, I’ve adapted it to read from a MS spreadsheet, so the user does not need to access the python code. Most examples that I’ve seen require the variables to be added (manually) to a python dictionary, then filters through jinja2. This requires that the variables are inputted using a spreadsheet.

Supported versions:

Python3.6 (tested)
Python 2.7.15 (tested)

Required standard and non standard libraries and modules

re, pandas, sys, numpy, pyexcel, copy, jinja2 and os

#How to use

You will need the following files:

1)	Input excel file, example has been provided. The file format must be either .xls or xlsx
2)	Template.j2, example has been provided. The file must end in .j2. 
3)	Output can either support no file extension or a file extension. I prefer a file extension for reading on my local PC. 

#System Arguments

-i (input) inputfile.xls
-o (output) router.txt
-t (template) template

All three System Arguments must be supplied otherwise the python code will generate an error. 

python3.6 j2_create_conf.py -i j2_local_write.xlsx -t template.j2 -o test.txt

#XLS/XLSX input file


•	Var Names: need to be unique, if a duplicate is found, the code will stop with an error. 

•	Var Values: value to be applied to the jinja2 template and ultimately, the output file. 

•	Tab sheet name, no dependence. 

•	Do not add {{}} brackets to the excel 

•	Spaces are permitted under the var_value column

•	Spaces are not permitted under the var_name column


#Template file

Example configuration file in which the variables will be applied and ultimately, applied to a device.  


router ospf {{ospf_process}}

network {{ospf_net}} area {{ospf_area}}

router bgp {{bgp_asn}}

neighbor {{neighbor_1}} remote-as {{asn_65000}}

interface loop 0

description {{lb0_description}}


#Variable matching


Before the python code begins the process of applying the variables (through the jinja2 file), it validates that the supplied information from the excel spreadsheet aligns with the template files. All variables names must exist in both the template and the spreadsheet otherwise, the python code will stop with an error. 

#Output file


The output file is written to the locations listed under the system arguments -o.  

