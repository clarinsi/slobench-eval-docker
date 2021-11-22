from os.path import join
import logging
import os
import tempfile
import subprocess
import argparse
import re

from pyrouge import Rouge155
from pyrouge.utils import log

try:
    _ROUGE_PATH = os.environ['ROUGE']
except KeyError:
    print('Warning: ROUGE is not configured')
    _ROUGE_PATH = None


# Method adapted from https://github.com/bheinzerling/pyrouge/blob/master/pyrouge/Rouge155.py 
def output_to_dict(output):
    """
    Convert the ROUGE output into python dictionary for further
    processing.
    """
    #0 ROUGE-1 Average_R: 0.02632 (95%-conf.int. 0.02632 - 0.02632)
    pattern = re.compile(
        r"(\d+) (ROUGE-\S+) (Average_\w): (\d.\d+) "
        r"\(95%-conf.int. (\d.\d+) - (\d.\d+)\)")
    results = {}
    for line in output.split("\n"):
        match = pattern.match(line)
        if match:
            sys_id, rouge_type, measure, result, conf_begin, conf_end = \
                match.groups()
            measure = {
                'Average_R': 'R',
                'Average_P': 'P',
                'Average_F': 'F1 Score'
                }[measure]
            rouge_type = rouge_type.upper().replace("-", ' ')            
            key = "{} {}".format(rouge_type, measure)
            results[key] = float(result)            
    return results

def eval_rouge(dec_dir, ref_dir, dec_pattern, ref_pattern,
               cmd='-c 95 -r 1000 -n 2 -m', system_id=1):
    """ evaluate by original Perl implementation"""
    
    # silence pyrouge logging
    assert _ROUGE_PATH is not None
    log.get_global_console_logger().setLevel(logging.WARNING)

    output_dict = {}
    with tempfile.TemporaryDirectory() as tmp_dir:
        Rouge155.convert_summaries_to_rouge_format(
            dec_dir, join(tmp_dir, 'dec'))
        Rouge155.convert_summaries_to_rouge_format(
            ref_dir, join(tmp_dir, 'ref'))
        Rouge155.write_config_static(
            join(tmp_dir, 'dec'), dec_pattern,
            join(tmp_dir, 'ref'), ref_pattern,
            join(tmp_dir, 'settings.xml'), system_id
        )
        cmd = (join(_ROUGE_PATH, 'ROUGE-1.5.5.pl')
               + ' -e {} '.format(join(_ROUGE_PATH, 'data'))
               + cmd
               + ' -a {}'.format(join(tmp_dir, 'settings.xml')))

        completed_process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output_dict = output_to_dict(completed_process.stdout)
    return output_dict
