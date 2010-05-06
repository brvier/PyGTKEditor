#!/usr/bin/python

#pylint result fixer
#By Khertan

import sys

def extract_filename_and_line_number(line):
  filename = line[:line.index(':')]
  rest = line[line.index(':')+1:]
  linenumber = rest[:rest.index(':')]
  return filename,int(linenumber)-1

def fix_comma(line,cindex):
  return line[:cindex+1]+' '+line[cindex+1:]

def get_file_line(filename,lindex):
  code_file = open(filename,'r')
  code_lines = code_file.read().split('\n')
  code_file.close()
  return code_lines[lindex]

def set_file_line(filename,lindex,line):
  code_file = open(filename,'r')
  code_lines = code_file.read().split('\n')
  code_file.close()
  code_lines[lindex] = line
  code_file = open(filename,'w')
  code_file.write('\n'.join(code_lines))
  code_file.close()
  return

def fix():
  argv = sys.argv
  argv.pop(0)

  results_path = argv.pop(0)
  results_file = open(results_path,'r')
  results_lines = results_file.read().split('\n')
  results_file.close()

  #do fix
  for index,line in enumerate(results_lines):
    if 'Comma not followed by a space' in line:
      print extract_filename_and_line_number(line)
      cindex = results_lines[index+2].index('^^')
      filename,linenumber = extract_filename_and_line_number(results_lines[index])
      print filename,linenumber
      codeline = get_file_line(filename,int(linenumber))
      codeline = fix_comma(codeline,cindex)
      set_file_line(filename,int(linenumber),codeline)

if __name__ == "__main__":
  fix()