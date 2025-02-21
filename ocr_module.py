import halcon as ha
import numpy as np
import os
from PIL import Image as im

# Initialization code
def initialize_ocr():
    global deep_ocr
    Data_path = '/home/logos/Desktop/DATASET-HARD-DISK'
    filenames = os.listdir(Data_path)
    img = ha.read_image(Data_path+'/'+filenames[0])
    x, y = ha.get_image_size(img)
    
    deep_ocr = ha.create_deep_ocr([],[])
    ha.set_deep_ocr_param(deep_ocr,'detection_tiling','true')
    ha.set_deep_ocr_param(deep_ocr,'detection_tiling_overlap',124)
    ha.set_deep_ocr_param(deep_ocr,'detection_min_character_score',0.4)
    ha.set_deep_ocr_param(deep_ocr,'detection_min_link_score',0.4)
    ha.set_deep_ocr_param(deep_ocr,'detection_min_word_area',70)
    ha.set_deep_ocr_param(deep_ocr,'detection_min_word_score',0.5)
    ha.set_deep_ocr_param(deep_ocr,'detection_sort_by_line','true')
    ha.set_deep_ocr_param(deep_ocr,'detection_image_width',2000)
    ha.set_deep_ocr_param(deep_ocr,'detection_image_height',3000)
    
    dldevicehandle = ha.query_available_dl_devices(['type', 'ai_accelerator_interface'], ['gpu', 'tensorrt'])
    detectionConverted = ha.read_dl_model("/home/logos/MVTec/HALCON-24.11-Progress-Steady/bin/aarch64-linux/convDetModelRt16_2000_3000_124.hdl")
    recognitionConverted = ha.read_dl_model("/home/logos/MVTec/HALCON-24.11-Progress-Steady/bin/aarch64-linux/convRecModelRt16_2000_3000_124.hdl")
    #detectionConverted = ha.read_dl_model('/home/logos/MVTec/HALCON-24.11-Progress-Steady/bin/aarch64-linux/ConvDetModelRt16_4k_tile_over_256.hdl')
    #recognitionConverted = ha.read_dl_model('/home/logos/MVTec/HALCON-24.11-Progress-Steady/bin/aarch64-linux/convRecModelRt16_4k_tile_over_256.hdl')
    
    ha.set_deep_ocr_param(deep_ocr,'detection_model',detectionConverted)
    ha.set_deep_ocr_param(deep_ocr,'recognition_model', recognitionConverted)
    ha.set_deep_ocr_param(deep_ocr, 'device', dldevicehandle[0])
    
    print("\nOCR initialized correctly\n")
    #print(f'working with images of width {x} and height {y}')

def check_output(ocr_result):
    n_words_detected = len(ocr_result)
    if (n_words_detected == 0):
        print("ERROR: No Text Detected, check Hard-Disk Orientation")
        
    else:
        for word in ocr_result:
            if word == 'sn' or word=='SN' or word=="S/N" or word=='S/N:' or word=='s/n' or word=='s/n:' or word=='sn:' or word=='SN:' or word=='serial':
                return True
                break
            
                
                
    

# def execute_ocr(filename):
#     while 
#     if ha.file_exists(filename):

# OCR function
def run_ocr(Image):
    
    Data_path = '/home/logos/Desktop/DATASET-HARD-DISK'
    filenames = os.listdir(Data_path)
    
    #img = ha.read_image(Data_path+'/'+filenames[0])

    x, y = ha.get_image_size(Image)
    print('correctly read the models\n')
    DisplayWidth = 1024
    DisplayHeight = 1024

    Mode = 'auto'
    Width, Height = ha.get_image_size(Image)
    start = ha.count_seconds()
    DeepOcrResults = ha.apply_deep_ocr(Image, deep_ocr, 'auto')

    end = ha.count_seconds()
    total = end-start
    print('execution time ocr: ', total)
    image = ha.get_dict_object(DeepOcrResults, 'image')

    RecognizedWords = ha.get_dict_tuple(DeepOcrResults, 'words')
    word = ha.get_dict_tuple(RecognizedWords, 'word')
    Bboxs = ha.get_dict_tuple(DeepOcrResults, 'words')
    row = ha.get_dict_tuple(Bboxs, 'row')
    col = ha.get_dict_tuple(Bboxs, 'col')
    phi = ha.get_dict_tuple(Bboxs, 'phi')
    length1 = ha.get_dict_tuple(Bboxs, 'length1')
    length2 = ha.get_dict_tuple(Bboxs, 'length2')
    
    # img = ha.himage_as_numpy_array(image)
    # img = im.fromarray((img+126).astype(np.uint8))
    # img.show()
    
    return word

# Initialize OCR when the module is imported
initialize_ocr()

# Only execute this block when running directly
if __name__ == "__main__":
    run_ocr()
