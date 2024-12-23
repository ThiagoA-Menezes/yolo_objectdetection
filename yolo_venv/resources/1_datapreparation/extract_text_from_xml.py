# %%
# Import Libraries

import os
from glob import glob
import pandas as pd
from functools import reduce 
from xml.etree import ElementTree as et


print("Libraries Imported")
# %%
import warnings
warnings.filterwarnings('ignore')

# %%
# Load all the XML files and Store in a list
#xml_list = glob("./data_images/annotations/*.xml")
xml_list = glob("./data_images/*.xml")

# Data Cleaning. replace \\ with /
# This could be useful if you are working on Windows
# xml_list = list(map(lambda x: x.replace("\\", "/"), xml_list))

# %%
# read xml files 
# from each xml file we need to extract 
# filename, size(width, height), object(name, xmin, xmax, ymin, ymax)

#tree = et.parse('./data_images/000001.xml')
#root = tree.getroot()
##print(root)
#
## extract filename
#image_name = root.find('filename').text
#
## width and height of the image
#width = root.find('size').find('width').text
#height = root.find('size').find('height').text
##print(width, "x", height)
#
## %%
#objs = root.findall('object')
# %%
# Extracting the first object and put in a list
# obj = objs[0]
# name = obj.find('name').text
# bndbox = obj.find('bndbox')
# xmin = bndbox.find('xmin').text
# xmax = bndbox.find('xmax').text
# ymin = bndbox.find('ymin').text
# ymax = bndbox.find('ymax').text
# 
# [name, xmin, xmax, ymin, ymax]
# %%
# Now, we will extract the information from all the XML files and store them in a list of dictionaries.
# for obj in objs:
#     name = obj.find('name').text
#     bndbox = obj.find('bndbox')
#     xmin = bndbox.find('xmin').text
#     xmax = bndbox.find('xmax').text
#     ymin = bndbox.find('ymin').text
#     ymax = bndbox.find('ymax').text
#     #print([name, xmin, xmax, ymin, ymax])
# 
# # %%
# image_name = root.find('filename').text
# width = root.find('size').find('width').text
# height = root.find('size').find('height').text
# objs = root.findall('object')
# parser = []
# for obj in objs:
#     name = obj.find('name').text
#     bndbox = obj.find('bndbox')
#     xmin = bndbox.find('xmin').text
#     xmax = bndbox.find('xmax').text
#     ymin = bndbox.find('ymin').text
#     ymax = bndbox.find('ymax').text
#     parser.append([image_name, width, height, name, xmin, xmax, ymin, ymax])
# %%
#display(parser)
# %%
# Now, we will tranform the list into a function

def extract_text(filename):
    tree = et.parse(filename)
    root = tree.getroot()

    #extract filename
    image_name = root.find('filename').text
    #width and height of the image
    width = root.find('size').find('width').text
    height = root.find('size').find('height').text
    objs = root.findall('object')
    parser = []
    for obj in objs:
        name = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = bndbox.find('xmin').text
        xmax = bndbox.find('xmax').text
        ymin = bndbox.find('ymin').text
        ymax = bndbox.find('ymax').text
        parser.append([image_name, width, height, name, xmin, xmax, ymin, ymax])
    
    return parser

# %%
parser_all = list(map(extract_text, xml_list))
# %%
# We're going to use a lambda function to flatten the list of lists
data = reduce(lambda x,y : x+y, parser_all)
# %%
df = pd.DataFrame(data, columns=['filename', 'width', 'height', 'name', 'xmin', 'xmax', 'ymin', 'ymax'])
# %%
df.head(5)
# %%
df.shape
# %%
df['name'].value_counts()

# %%

names = df['name'].unique()
print(names)
# %%
df.info()
# %%
# Type Conversions 
cols = ['width', 'height', 'xmin', 'xmax', 'ymin', 'ymax']
df[cols] = df[cols].astype(int)
df.info()
# %%
# Center x, center y
df['center_x'] = ((df['xmax']+df['xmin'])/2)/df['width']
df['center_y'] = ((df['ymax']+df['ymin'])/2)/df['width']

#widht and height of the bounding box
df['w'] = (df['xmax']-df['xmin'])/df['width']
df['h'] = (df['ymax']-df['ymin'])/df['height']
# %%
df.head()
# %%
# Split the data into train and test
images = df['filename'].unique()
# %%
len(images)
# %%
# 80% of the data will be used for training and 20% for testing
img_df = pd.DataFrame(images, columns=['filename'])
img_train = tuple(img_df.sample(frac=0.8, random_state=42)['filename']) #shuffle and pick 80% of the data
img_test = tuple(img_df.query(f'filename not in {img_train}')['filename']) # take the rest of the data
# %%
len(img_train) , len(img_test)
# %%
train_df = df.query(f'filename in {img_train}')

# %%
test_df = df.query(f'filename in {img_test}')
# %%
train_df.head()
# %%
test_df.head()
# %%
# Assign id numbers to object names

def label_encoding(x):
    labels = {'person': 0, 'car': 1, 'chair': 2, 'bottle': 3, 'pottedplant': 4, 'bird': 5, 'dog': 6,
              'sofa': 7, 'bicycle': 8, 'horse': 9, 'boat': 10, 'motorbike': 11, 'cat': 12, 'tvmonitor': 13,
              'cow' : 14, 'sheep': 15, 'aeroplane': 16, 'train': 17, 'diningtable': 18, 'bus': 19, 'troley' : 20}
    return labels[x]

# %%
train_df['id'] = train_df['name'].apply(label_encoding)
test_df['id'] = test_df['name'].apply(label_encoding)
# %%
train_df.head()
# %%
import os 
from shutil import move

def ensure_directories_exist(directories):
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f" Pasta Criada: {directory}")
        else:
            print(f" Pasta já existe: {directory}")

train_folder = './data_images/train'
test_folder = './data_images/test'

ensure_directories_exist([train_folder, test_folder])

#os.mkdir(train_folder)
#os.mkdir(test_folder)
cols = ['filename', 'id', 'center_x', 'center_y', 'w', 'h']
groupby_obj_train = train_df[cols].groupby('filename')
groupby_obj_test = test_df[cols].groupby('filename')
# groupby_obj_train.get_group('007826.jpg').set_index('filename').to_csv('sample.txt', index=False, header=False)
# save each image in train/test folder and respective labels in .txt
def save_data(filename, folder_path, groupby_obj):
    # move image
    src = os.path.join('data_images', filename)
    dst = os.path.join(folder_path, filename)
    move(src, dst) # move image to destination folder

    # save the labels
    base_filename = os.path.splitext(filename)[0]  # remove the extension
    text_filename = os.path.join(folder_path, base_filename + '.txt')
    
    #get data from groupby object using the original filename
    groupby_obj.get_group(filename).set_index('filename').to_csv(
        text_filename, index=False, header=False, sep=' ')

#print(os.path.splitext('/data_images/000001.jpg')[0]+'.txt')

filename_series = pd.Series(groupby_obj_train.groups.keys())
filename_series.apply(save_data, args=(train_folder, groupby_obj_train))
# %%
# Lets do the same for the test data
filename_series_test = pd.Series(groupby_obj_test.groups.keys())
filename_series_test.apply(save_data, args=(test_folder, groupby_obj_test))

