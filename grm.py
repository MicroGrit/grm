#!/Users/wenxian/opt/anaconda3/bin/python
# -*- coding: utf-8 -*-
import csv
import re
import argparse
import os

'''
Ref: https://docs.python.org/zh-cn/3/library/csv.html

'''

__version__ = "v0.1"

COLOR = {
    # basic colors
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    # bright colors
    'bright_black': '\033[90m',
    'bright_red': '\033[91m',
    'bright_green': '\033[92m',
    'bright_yellow': '\033[93m',
    'bright_blue': '\033[94m',
    'bright_magenta': '\033[95m',
    'bright_cyan': '\033[96m',
    'bright_white': '\033[97m',
    # misc
    'end': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m'
}

grm_description = COLOR['red']+COLOR['bold'] \
    + 'Generate UVM Register Model(grm)'\
    + COLOR['end']


ralf_end = "}\n"
reg_end = "}\n\n"

reg_format = ""
field_format = ""
mem_format = ""

def format_msg(color,message):
    return color+message+COLOR['end']

def gen_mem_format():
    pass

def gen_field_format():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="grm",description=grm_description)
    parser.add_argument('-f', type=str, help='input regmodel .csv file')
    args = parser.parse_args()

    print(parser.description)
    print(format_msg(COLOR['yellow']+COLOR['bold'],"Input:"), os.path.abspath(args.f))

    modlue_name = os.path.basename(args.f).split('.')
    ralf_file_name = modlue_name[0] +'.ralf'

    user_reg_model_name = modlue_name[0]
    ralf_header = f"block {user_reg_model_name} {{\n" \
        + f"\tbytes\t4;\n" \
        + f"\tendian\tlittle;\n\n"
    
    with open(args.f,'r', newline='', encoding='utf-8-sig') as csv_file, \
        open(ralf_file_name,'w',encoding='utf-8') as ralf_file:

        ralf_file.write(ralf_header)
        rows = csv.reader(csv_file)
        # print(csv_file)
        next(csv_file) # ignore csv file header

        for row in rows:
            if(row[1]=='reg'):
                reg_format = "register "+row[2]+ " @"+row[0] +" {\n" \
                    +"\tbytes 4;\n"
                match = re.search(r'\[(?P<left>\d+)\:(?P<right>\d+)\]',row[6]) #[left:right]
                # print(match.group('left'),match.group('right'))
                bitwidth = int(match.group('left')) - int(match.group('right')) + 1
                field_format = ""
                field_format = \
                    "\tfield "+row[5] + " @"+match.group('right')+" {\n" \
                    + "\t\tbits \t"+ str(bitwidth) +"\t;\n" \
                    + "\t\taccsss \t" + row[8] +"\t;\n" \
                    + "\t\treset \t" + row[7] +"\t;\n" \
                    + "\t}\n"
                reg_format=reg_format+field_format
                ralf_file.write(reg_format)
            elif(row[1]=='mem'):
                mem_format = ""
                mem_name=row[2]
                addroffset=row[0]
                mem_size= row[9]
                mem_bits=row[10]
                mem_access=row[8]
                mem_format = f'memory {mem_name} @{addroffset} {{\n' \
                    + f"\tsize\t{mem_size};\n" \
                    + f"\tbits\t{mem_bits};\n" \
                    + f"\taccress\t{mem_access};\n" \
                    + f"}}\n\n"
                ralf_file.write(mem_format)
            else:
                match = re.search(r'\[(?P<left>\d+)\:(?P<right>\d+)\]',row[6]) #[left:right]
                bitwidth = int(match.group('left')) - int(match.group('right')) + 1
                field_format = ""
                field_format = \
                    "\tfield "+row[5] + " @"+match.group('right')+" {\n" \
                    + "\t\tbits \t"+ str(bitwidth) +"\t;\n" \
                    + "\t\taccsss \t" + row[8] +"\t;\n" \
                    + "\t\treset \t" + row[7] +"\t;\n" \
                    + "\t}\n"
                ralf_file.write(field_format)
                if(int(match.group('right') == 0)):
                    ralf_file.write(reg_end)
        ralf_file.write(ralf_end)
        print(format_msg(COLOR['yellow']+COLOR['bold'],"Output: "),ralf_file_name)