# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 14:41:22 2018

@author: nxb15186
"""

from analyzer import Analyzer

class ParticlesAnalyzer(Analyzer):
    
    def __init__(self, particles = None, quantityList = None, bin_size = None, print_data = None,save_txt = None, save_summary_txt = None, file_name = None,use_existing_file = None):
        Analyzer.__init__(self,print_data=print_data, file_name = file_name, save_txt= save_txt, save_summary_txt = save_summary_txt,use_existing_file = use_existing_file)
        self.particles = particles
        self.quantityList = quantityList
        self.bin_size = bin_size






