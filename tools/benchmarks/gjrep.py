#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import subprocess


# Import rejit utils.
dir_benchmarks = os.path.dirname(os.path.realpath(__file__))
dir_rejit = dir_benchmarks
while 'SConstruct' not in os.listdir(dir_rejit):
  dir_rejit = os.path.realpath(os.path.join(dir_rejit, '..'))
sys.path.insert(0, os.path.join(dir_rejit, 'tools'))
import utils



description = '''
Run grepping benchmarks.
grep and jrep must be in your path.'''

def validate_directory(path):
  if not os.path.isdir(path):
    raise argparse.ArgumentError("{0} invalid")
  return path

parser = argparse.ArgumentParser(description=description,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

engines_available = ['grep', 'jrep', 'git grep']
engines_default = ['grep', 'jrep']
parser.add_argument('--engines', action='store', nargs='+',
                    choices=engines_available, default=engines_default,
                    help='''
Space-separated list of grep utilities to benchmark. (To benchmark `git grep`,
the target directory must be within the current git repo, and use quotes to
escape the space.)
''')
parser.add_argument('-i', '--iterations', type=int, default=5,
                    help="Number of iterations to run for each benchmarks")
parser.add_argument('directory',
                    type=validate_directory,
                    help="Directory to recursively grep through"),

args = parser.parse_args()




regexps_easy = [
  "foobar",
  "éphémère",
  "unsigned",
  "A_quite_long_string_of_36_characters"
]
regexps_alt = [
  "alternation|words",
  "NOTfound|foobar|typedef|éphémère",
  "typedef|definition|definitively"
]
regexps_hard = [
  "[a-z]{3,10}.*gnu.*[a-z]{3,10}",
  "^\s*(void|unsigned|int)\s+func\s+\(",
]
# Use underscores '_' to limit the number of matches for small digits.
regexps_alt_linear = [
  "NOTfound|foobar|rare|typedef",
  "1__",
  "1__|22_",
  "1__|22_|333",
  "1__|22_|333|4444",
  "1__|22_|333|4444|55555",
  "1__|22_|333|4444|55555|666666",
  "1__|22_|333|4444|55555|666666|7777777",
  "1__|22_|333|4444|55555|666666|7777777|88888888",
  "1__|22_|333|4444|55555|666666|7777777|88888888|999999999",
]

regexps = regexps_easy + regexps_alt + regexps_hard + regexps_alt_linear



engines = [e for e in engines_available if e in args.engines]
engines_options_base = {
  'grep': ['--recursive', '--with-filename', '--line-number', '--extended-regexp'],
  'git grep': ['--untracked', '--extended-regexp'],
  'jrep': ['--recursive', '--with-filename', '--line-number']}
engines_options_extra = {
  'jrep': ['-j']
}

results = {}




def quotify(x):
  return '"' + x + '"'



class TimeResult:
  def __init__(self, time_output):
    self.sys = 0
    self.user = 0
    self.real = 0

    outs = time_output.split('\n')
    for line in outs:
      if len(line) == 0:
        continue
      (label, value) = line.split()
      if label == 'sys':
        self.sys = value
      if label == 'user':
        self.user = value
      if label == 'real':
        self.real = value

  def print_label(self):
    print 'sys: %s\tuser: %s\treal: %s' % (self.sys, self.user, self.real)

  def print_raw(self):
    print '%s\t%s\t%s' % (self.sys, self.user, self.real)

  def __eq__(self, other):
    return self.sys == other.sys and \
           self.user == other.user and \
           self.real == other.real

  def __lt__(self, other):
    if self.real != other.real:
      return self.real < other.real
    if self.user != other.user:
      return self.user < other.user
    if self.user != other.user:
      return self.user < other.user



def add_result(regexp, engine, res):
  if regexp not in results:
    results[regexp] = {}
  results[regexp][engine] = res



# Print the results. The list of results can be reduced via a function passed in
# argument. The result must be iterable.
def print_results(reduce_function = lambda x: x):
  print 'regexp\tengine\tsys\tuser\treal'
  # Benchmarks have been run in order, so keys have been added in reversed order
  # to the dictionary of results.
  for regexp in reversed(results.keys()):
    for engine in sorted(results[regexp].keys()):
      to_print = reduce_function(results[regexp][engine])
      for res in to_print:
        print '%s\t%s\t' % (regexp, engine),
        res.print_raw()



def run_benchmarks():
  # TODO: On OSX redirecting to /dev/null raises an error.
  out_file = open('/tmp/gjrep.py.out', 'w')
  for regexp in regexps:
    for engine in engines:
      options = ['']
      if engine in engines_options_extra:
        options = options + engines_options_extra[engine]
      for opt in options:
        results = []

        run_cmd = ['time', '-p', engine, opt] + engines_options_base[engine] + [quotify(regexp), args.directory, '>', '/tmp/gjrep.py.out']
        print ' '.join(run_cmd)

        for i in range(1, args.iterations + 1):
          p_cmd = subprocess.Popen(' '.join(run_cmd), stdout=out_file, stderr=subprocess.PIPE, shell=True)
          p_g = subprocess.Popen(['grep', 'real\\|user\\|sys'], stdin=p_cmd.stderr,
                                 stdout=subprocess.PIPE)
          p_cmd.wait()
          p_g.wait()
          time_output = p_g.communicate()[0]

          results.append(TimeResult(time_output))

        engine_name = engine
        if (len(opt) > 0):
          engine_name = engine_name + ' ' + opt
        add_result(regexp, ' '.join([engine, opt]), results)
  out_file.close()




run_benchmarks()
print_results(lambda x : [min(x)])
