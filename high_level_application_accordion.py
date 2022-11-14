'''
This is the high-level script which runs all the pieces of the pipeline to
obtain updated Layden coefficients [a, b, c, d]
'''

import os
import sys
import collections
from collections import OrderedDict
from configparser import ConfigParser, ExtendedInterpolation
from conf import *
from modules import *

from modules import (compile_normalization,
                      create_spec_realizations,
                      run_robo,
                      scrape_ew_and_errew,
                      teff_retrieval,
                      find_feh)


class ApplyCalib():
    '''
    This actually runs the reduction that generates a calibration
    '''
    def __init__(self):

        # dictionary to contain pipeline steps
        self._dict_steps = collections.OrderedDict()

        # read in choice of configuration data file for reduction;
        # set contents as attributes for sections to follow
        config_choice = ConfigParser(interpolation=ExtendedInterpolation()) # for parsing values in .init file
        # config for reduction to find a, b, c, d
        config_choice.read(os.path.join(os.path.dirname(__file__), 'conf', 'config_apply.ini')) ## ## THIS HAS TO BE MANUALLY SET BY USER HERE; NEED TO CHANGE THIS

        self._attribs = config_choice


    def add_step(self, module):
        '''
        Adds module to the list of things to do
        '''

        self._dict_steps.update({module.name:module})


    def run(self):
        '''
        Loop over steps and run, letting each step inherit the attributes
        from the config file
        '''

        for exec_id in self._dict_steps.values():
            exec_id.run_step(attribs = self._attribs)
