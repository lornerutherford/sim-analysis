# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 14:40:30 2018

@author: Paul Scherkl
"""

class Analyzer(object):
    
    def __init__(self, print_data, file_name, save_txt, save_summary_txt, use_existing_file):
        self.outPath = None
        self.print_data = print_data
        self.save_txt = save_txt
        self.file_name = file_name
        self.use_existing_file = use_existing_file
        self.save_summary_txt  = save_summary_txt
