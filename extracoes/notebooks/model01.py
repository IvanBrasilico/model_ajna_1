from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau

model = models.Sequential([
  layers.Conv2D(16, (5, 5), activation='relu',
                padding='same',
                input_shape=(144, 288, 3)),
  layers.MaxPooling2D(pool_size=(2, 4)),
  layers.Dropout(0.25),
  layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
  layers.MaxPooling2D(pool_size=(2, 2)),
  layers.Dropout(0.25),
  layers.Conv2D(64, (3, 3), activation='relu'),
  layers.MaxPooling2D(pool_size=(2, 2)),
  layers.Dropout(0.25),
  layers.Conv2D(128, (3, 3), activation='relu'),
  layers.Conv2D(128, (3, 3), activation='relu'),
  layers.Conv2D(128, (1, 1), activation='relu'),
  layers.MaxPooling2D(pool_size=(2, 2)),
  layers.Dropout(0.25),
  layers.Conv2D(256, (3, 3), activation='relu'),
  layers.Conv2D(256, (3, 3), activation='relu'),
  layers.Conv2D(512, (1, 1), activation='relu'),
  layers.Flatten(),
  layers.Dense(512, activation='relu'),
  layers.Dropout(0.4),
  layers.Dense(1, activation='sigmoid')
 
])