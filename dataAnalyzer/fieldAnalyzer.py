# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 14:44:08 2018

@author: nxb15186
"""

from analyzer import Analyzer



class FieldAnalyzer(Analyzer):
    
    def __init__(self, fields = None, print_data = None,file_name = None, save_txt= None, save_summary_txt= None, use_existing_file = None):
        Analyzer.__init__(self, print_data= print_data, save_txt= save_txt, save_summary_txt= save_summary_txt,file_name=file_name,use_existing_file = use_existing_file)
        self.fields = fields
    




    
