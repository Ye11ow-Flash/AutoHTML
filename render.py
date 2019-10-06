#!/usr/bin/env python
import sys
import os
from argparse import ArgumentParser
from os.path import basename

from main import *

# def build_parser():
#   parser = ArgumentParser()
#   parser.add_argument('--png_path', type=str,
#                       dest='png_path', help='png filepath to convert into HTML',
#                       required=True)
#   parser.add_argument('--output_folder', type=str,
#                       dest='output_folder', help='dir to save generated gui and html',
#                       required=True)
#   parser.add_argument('--model_json_file', type=str,
#                       dest='model_json_file', help='trained model json file',
#                       required=True)
#   parser.add_argument('--model_weights_file', type=str,
#                       dest='model_weights_file', help='trained model weights file', required=True)
#   parser.add_argument('--style', type=str,
#                       dest='style', help='style to use for generation', default='default')
#   return parser

def main(png_path):
    # parser = build_parser()
    # options = parser.parse_args()
    # png_path = sys.argv[2]
    # print(png_path)
    output_folder = './templates'
    model_json_file = './model/model_json.json'
    model_weights_file = './model/weights.h5'
    converter = Major(model_json_path=model_json_file,
                      model_weights_path = model_weights_file)
    converter.convert(output_folder, png_path=png_path,print_generated_output=0, 
                                  get_sentence_bleu=0, original_gui_filepath='./templates/')
    return './templates/ui.html'
if __name__ == "__main__":
  png_path = sys.argv[1]
  # print(sys.argv)
  main(png_path)