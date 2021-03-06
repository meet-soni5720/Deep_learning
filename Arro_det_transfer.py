# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 12:00:54 2019

@author: Meet
"""


from keras.applications import ResNet50
from keras.layers import MaxPooling2D
from keras.models import Model
from keras.layers import Dense
from keras.layers import Flatten,Dropout
from keras import regularizers
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.resnet50 import preprocess_input
from keras.preprocessing.image import load_img
from keras.utils.vis_utils import plot_model
from keras.preprocessing.image import img_to_array
from keras.applications.resnet50 import decode_predictions
import keras.backend as K
import numpy as np

# load model without classifier layers
model = ResNet50(weights ="imagenet",include_top=False, input_shape=(224, 224, 3))
# add new classifier layers
x=model.output 
x=MaxPooling2D()(x) 
for layer in model.layers:
    layer.trainable = False
x=Dense(units=256,activation="relu",kernel_regularizer = regularizers.l2(0.5))(x)
x = Dropout(0.4)(x)
x=Dense(units=256,activation="relu",kernel_regularizer = regularizers.l2(0.5))(x)
x = Dropout(0.4)(x)
x=Flatten()(x)
output = Dense(units=2,activation="softmax")(x)
model = Model(inputs=model.input, outputs=output)


# summarize
model.summary()
#plot_model(model, to_file='Resnet50.png')

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

image_size = 224
data_generator = ImageDataGenerator(preprocessing_function=preprocess_input,
                                   rescale=1./255,
                                   zoom_range = 0.2)


train_generator = data_generator.flow_from_directory(
        'D:/Arrow Detection/train',
        target_size=(image_size, image_size),
        batch_size=16,
        class_mode='categorical',
        color_mode = 'rgb',
        shuffle = True,)

validation_generator = data_generator.flow_from_directory(
       'D:/Arrow Detection/test',
        target_size=(image_size, image_size),
        class_mode='categorical',
        color_mode = 'rgb',
             )

model.fit_generator(
        train_generator,
        steps_per_epoch=10,
        epochs = 30,
        validation_data=validation_generator,
        validation_steps=3)
        
img = load_img('D:/Arrow Detection/test/left arrow/mars(26).jpg',target_size=(224,224))
# report details about the image
print(type(img))
print(img.format)
print(img.mode)
print(img.size)
# show the image
img.show()
# convert the image pixels to a numpy array
image = img_to_array(img)
# reshape data for the model
image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
print(image.shape)
# prepare the image for the VGG model
image = preprocess_input(image)
# predict the probability across all output classes
yhat = model.predict(image)
print(yhat)
print(np.argmax(yhat) + 1)
'''# convert the probabilities to class labels
label = decode_predictions(yhat)
# retrieve the most likely result, e.g. highest probability
label = label[0][0]
# print the classification
print('%s (%.2f%%)' % (label[1], label[2]*100))'''