# useful code fragments for testing path simulator (pathsim.py)

import stem.descriptor.reader as sdr
import datetime
import os
import os.path
import stem.descriptor as sd
import stem.descriptor.networkstatus as sdn
import stem
import random
import sys
import collections
import pathsim

def timestamp(t):
    """Returns UNIX timestamp"""
    td = t - datetime.datetime(1970, 1, 1)
    ts = td.days*24*60*60 + td.seconds
    return ts

### read in consensuses and (old-style) processed descriptors ###
r_file = 'in/cons-2012-08-02-00/2012-08-02-00-00-00-consensus'
d_file = 'out/desc-2012-08-02-00/2012-08-02-00-00-00-descriptor'
descriptors = {}

cur_period_start = None
cur_period_end = None

cons_valid_after = None
cons_fresh_until = None
cons_bw_weights = None
cons_bwweightscale = None        
cons_rel_stats = {}

with open(d_file, 'r') as df:
    for desc in sd.parse_file(df, validate=False):
        descriptors[desc.fingerprint] = desc
with open(r_file, 'r') as cf:        
    for rel_stat in sd.parse_file(cf, validate=False):
        cons_valid_after = \
            timestamp(rel_stat.document.valid_after)
        cur_period_start = cons_valid_after
        cons_fresh_until = \
            timestamp(rel_stat.document.fresh_until)
        cur_period_end = cons_fresh_until
        cons_bw_weights = rel_stat.document.bandwidth_weights
        if ('bwweightscale' in rel_stat.document.params):
            cons_bwweightscale = rel_stat.document.params[\
                'bwweightscale']
        else:
            cons_bwweightscale = 10000  
        if (rel_stat.fingerprint in descriptors):
            cons_rel_stats[rel_stat.fingerprint] = rel_stat
######

### read in all descriptors from a month ###
sd_dir = 'in/server-descriptors-2012-08'
num_descriptors = 0    
num_relays = 0
all_descriptors = {}
with sdr.DescriptorReader(sd_dir, validate=True) as reader:
    for desc in reader:
        if (num_descriptors % 10000 == 0):
            print('{0} descriptors processed.'.format(num_descriptors))
        num_descriptors += 1
        if (desc.fingerprint not in all_descriptors):
            all_descriptors[desc.fingerprint] = {}
            num_relays += 1
        all_descriptors[desc.fingerprint][timestamp(desc.published)] = desc
print('#descriptors: {0}; #relays:{1}'.\
    format(num_descriptors,num_relays)) 
######

#### go through hibernate statuses for a given relay in all_descriptors ###
fprint = 'BC77196F4730442A96E36E1A13B3FF8DC14151EB' # RememberJobs
descs = all_descriptors[fprint]
desc_times = sorted(descs.keys())
for t in desc_times:
    print('{0} ({1}): {2}'.format(descs[t].published.strftime('%Y-%m-%d %H:%M:%S'), t, descs[t].hibernating))
######

###### look for hibernating statuses of a given relay ######
fprint = 'FD688C0692D87AC0D04D42FF4C606FF1AB420C9E'
for hs in hibernating_statuses:
    if (hs[1] == fprint):
        print(hs)
######