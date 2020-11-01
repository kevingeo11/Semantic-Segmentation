import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Conv2DTranspose
from keras.models import Sequential
from keras import Model
from keras import Input
from keras.layers import concatenate
from keras.utils import plot_model

def build_model(inp_size, nlabels):
    input_layer = Input(inp_size)
    conv1 = Conv2D(64, (3, 3), activation="relu", padding="same")(input_layer)
    conv1 = Conv2D(64, (3, 3), activation="relu", padding="same")(conv1)
    pool1 = MaxPooling2D((2, 2))(conv1)
    pool1 = Dropout(0.25)(pool1)

    conv2 = Conv2D(128, (3, 3), activation="relu", padding="same")(pool1)
    conv2 = Conv2D(128, (3, 3), activation="relu", padding="same")(conv2)
    pool2 = MaxPooling2D((2, 2))(conv2)
    pool2 = Dropout(0.5)(pool2)

    conv3 = Conv2D(256, (3, 3), activation="relu", padding="same")(pool2)
    conv3 = Conv2D(256, (3, 3), activation="relu", padding="same")(conv3)
    pool3 = MaxPooling2D((2, 2))(conv3)
    pool3 = Dropout(0.5)(pool3)

    conv4 = Conv2D(512, (3, 3), activation="relu", padding="same")(pool3)
    conv4 = Conv2D(512, (3, 3), activation="relu", padding="same")(conv4)
    pool4 = MaxPooling2D((2, 2))(conv4)
    pool4 = Dropout(0.5)(pool4)

    # Middle
    convm = Conv2D(1024, (3, 3), activation="relu", padding="same")(pool4)
    convm = Conv2D(1024, (3, 3), activation="relu", padding="same")(convm)
    
    deconv4 = Conv2DTranspose(512, (3, 3), strides=(2, 2), padding="same")(convm)
    uconv4 = concatenate([deconv4, conv4])
    uconv4 = Dropout(0.5)(uconv4)
    uconv4 = Conv2D(512, (3, 3), activation="relu", padding="same")(uconv4)
    uconv4 = Conv2D(512, (3, 3), activation="relu", padding="same")(uconv4)

    deconv3 = Conv2DTranspose(256, (3, 3), strides=(2, 2), padding="same")(uconv4)
    uconv3 = concatenate([deconv3, conv3])
    uconv3 = Dropout(0.5)(uconv3)
    uconv3 = Conv2D(256, (3, 3), activation="relu", padding="same")(uconv3)
    uconv3 = Conv2D(256, (3, 3), activation="relu", padding="same")(uconv3)

    deconv2 = Conv2DTranspose(128, (3, 3), strides=(2, 2), padding="same")(uconv3)
    uconv2 = concatenate([deconv2, conv2])
    uconv2 = Dropout(0.5)(uconv2)
    uconv2 = Conv2D(128, (3, 3), activation="relu", padding="same")(uconv2)
    uconv2 = Conv2D(128, (3, 3), activation="relu", padding="same")(uconv2)

    deconv1 = Conv2DTranspose(64, (3, 3), strides=(2, 2), padding="same")(uconv2)
    uconv1 = concatenate([deconv1, conv1])
    uconv1 = Dropout(0.5)(uconv1)
    uconv1 = Conv2D(64, (3, 3), activation="relu", padding="same")(uconv1)
    uconv1 = Conv2D(64, (3, 3), activation="relu", padding="same")(uconv1)
    
    output_layer = Conv2D(nlabels, (1,1), padding="same", activation="sigmoid")(uconv1)
    
    model = Model(inputs = input_layer, outputs = output_layer)

    return model


model = build_model((128,128,1), 28)
print(model.summary())