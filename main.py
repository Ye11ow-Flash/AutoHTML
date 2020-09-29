from __future__ import absolute_import

import sys
import os
import shutil
import json
import numpy as np

from PIL import Image
import cv2

from keras.preprocessing.text import Tokenizer, one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical

from keras.preprocessing.image import ImageDataGenerator
from keras.models import model_from_json
from keras.preprocessing.sequence import pad_sequences

from grammar import *


MAX_LENGTH = 48
VOCAB_FILE = 'vocabulary.vocab'

class Major:

    def __init__(self, model_json_path=None, model_weights_path=None):
        
        file = open(VOCAB_FILE, 'r')
        text = file.read().splitlines()[0]
        file.close()
        tokenizer = Tokenizer(filters='', split=" ", lower=False)
        tokenizer.fit_on_texts([text])
        vocab_size = len(tokenizer.word_index) + 1
        self.tokenizer, self.vocab_size = tokenizer,vocab_size
        self.model = self.load_model(model_json_path, model_weights_path)
    
    def convert(self, output_folder, png_path, print_generated_output, get_sentence_bleu, original_gui_filepath):
        png_filename = os.path.basename(png_path)
        if png_filename.find('.png') == -1:
            raise ValueError("Image is not a png!")
        sample_id = png_filename[:png_filename.find('.png')]
        # Generate GUI
        generated_gui, gui_output_filepath = self.generate_gui(png_path, print_generated_output=0, output_folder=output_folder, sample_id=sample_id)

        # Generate HTML
        generated_html = self.generate_html(generated_gui, sample_id, print_generated_output=print_generated_output, output_folder=output_folder)

    def load_model(self, model_json_path, model_weights_path):
        json_file = open(model_json_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(model_weights_path)
        print("\nLoaded Model")
        return loaded_model

    def generate_gui(self, png_path, print_generated_output, sample_id, output_folder):
        # test_img_preprocessor = ImagePreprocessor()
        img_features = self.resize_img(png_path)
        assert(img_features.shape == (256,256,3))
        # img_features = test_img_preprocessor.get_img_features(png_path)
        # img_features == resized input image
        in_text = '<START> '
        photo = np.array([img_features])
        for i in range(150):
            sequence = self.tokenizer.texts_to_sequences([in_text])[0]
            sequence = pad_sequences([sequence], maxlen=MAX_LENGTH)
            yhat = self.model.predict([photo, sequence], verbose=0)
            yhat = np.argmax(yhat)
            word = self.word_for_id(yhat)
            if word is None:
                break
            in_text += word + ' '
            if word == '<END>':
                break

        generated_gui = in_text.split()
        gui_output_filepath = self.write_gui(generated_gui, sample_id, output_folder)

        return generated_gui, gui_output_filepath

    def generate_html(self, gui_array, sample_id, print_generated_output, output_folder):

        grammar = Grammar()
        compiled_website = grammar.compile(gui_array)

        if compiled_website != 'HTML Parsing Error':
            output_filepath = "{}/{}.html".format(output_folder, 'ui')
            with open(output_filepath, 'w') as output_file:
                output_file.write(compiled_website)
                print("Saved HTML Successfully")

    def word_for_id(self, integer):
        for word, index in self.tokenizer.word_index.items():
            if index == integer:
                return word
        return None

    def write_gui(self, gui_array, sample_id, output_folder):
        gui_output_filepath = "{}/{}.gui".format(output_folder, 'ui')
        with open(gui_output_filepath, 'w') as out_f:
            out_f.write(' '.join(gui_array))
        return gui_output_filepath

    def resize_img(self, png_file_path):
        img_rgb = cv2.imread(png_file_path)
        img_grey = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        img_adapted = cv2.adaptiveThreshold(img_grey, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 101, 9)
        img_stacked = np.repeat(img_adapted[...,None],3,axis=2)
        resized = cv2.resize(img_stacked, (200,200), interpolation=cv2.INTER_AREA)
        bg_img = 255 * np.ones(shape=(256,256,3))
        bg_img[27:227, 27:227,:] = resized
        bg_img /= 255
        return bg_img
