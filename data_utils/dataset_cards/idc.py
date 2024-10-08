from tensorflow.keras import utils
import numpy as np
import tensorflow as tf
import os
from PIL import Image
from sklearn.utils import shuffle


from ..dataset import Dataset



class IDC_Dataset(Dataset):
    
    def __init__(
        self,
        preferred_size=None,
        test_ratio=0.17,
        **kwargs
    ):
        
        Dataset.__init__(
            self,
            data_name='IDC',
            preferred_size=preferred_size
        )
        
        self.test_ratio = test_ratio
        self.preferred_shape = (50, 50, 3)
        
        return
    
    
    def prepare_data(
        self
    ):
        
        (x_train, y_train), (x_test, y_test) = self.load_data()
        
        print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)
        x_train = x_train.astype('float32')/255
        x_test = x_test.astype('float32')/255
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], x_train.shape[2], -1))
        x_test = np.reshape(x_test, (x_test.shape[0], x_train.shape[1], x_train.shape[2], -1))
        
        num_classes = int(np.max(y_train) + 1)
        y_train = utils.to_categorical(y_train, num_classes)
        y_test = utils.to_categorical(y_test, num_classes)
        
        return x_train, y_train, x_test, y_test
    
    
    def load_data(
        self
    ):
        
        x_train = np.load('../Datasets/'+self.data_name+'/x_train.npy')
        y_train = np.load('../Datasets/'+self.data_name+'/y_train.npy')
        
        x_test = np.load('../Datasets/'+self.data_name+'/x_test.npy')
        y_test = np.load('../Datasets/'+self.data_name+'/y_test.npy')
        
        return (x_train, y_train), (x_test, y_test)
    
    
    def get_class_names(self):
        return ['0', '1']
    
    
    def load_data_slow(
        self
    ):
        
        data_directory = '../Datasets/IDC/original/'
        filenames = os.listdir(data_directory)
        
        
        filepath = data_directory + filenames[0] + '/'
        x_all, y_all = self.get_xy_from_directory(filepath)
        
        for filename in filenames[1:]:
            
            filepath = data_directory + filename + '/'
            
            x, y = self.get_xy_from_directory(filepath)
            x_all = np.append(x_all, x, axis=0)
            y_all = np.append(y_all, y, axis=0)
            
            print(
                '\r', 
                np.array(x).shape, np.array(x_all).shape, 
                end=''
            )
        
        x_all, y_all = shuffle(x_all, y_all)
        
        test_size = int( self.test_ratio * len(x_all) )
        x_train = x_all[test_size:].copy()
        y_train = y_all[test_size:].copy()
        
        x_test = x_all[:test_size].copy()
        y_test = y_all[:test_size].copy()
        
        return (x_train, y_train), (x_test, y_test)
    
    
    def get_xy_from_directory(
        self, 
        directory_name, N=None
    ):
        
        images = []
        labels = []
        for class_num, class_name in enumerate(self.get_class_names()):
            
            file_names = os.listdir(directory_name+class_name)
            
            for file_name in file_names:
                
                image_ = Image.open(directory_name+class_name+'/'+file_name).convert('RGB')
                if self.preferred_size is not None:
                    image_ = image_.resize(self.preferred_size, Image.ANTIALIAS)
                
                if np.array(image_).shape == self.preferred_shape:
                    images.append(np.array(image_))
                    labels.append(class_num)
        
        images = np.array(images)
        labels = np.array(labels)
        
        return images, labels
    
    