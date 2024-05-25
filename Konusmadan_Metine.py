import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import layers
import speech_recognition as sr
karakterler=[x for x in "abcçdefgğhıijklmnoöprsştuüvyz' "]
charnum=keras.layers.StringLookup(vocabulary=karakterler,oov_token="")
numar=keras.layers.StringLookup(vocabulary=charnum.get_vocabulary(),oov_token="",invert=True)
frame_length = 256
frame_step = 160
fft_length = 384
def CTCLoss(y_true,y_pred):
  batch_len=tf.cast(tf.shape(y_true)[0],dtype="int64")
  input_length=tf.cast(tf.shape(y_pred)[1],dtype="int64")
  label_length=tf.cast(tf.shape(y_true)[1],dtype="int64")

  input_length=input_length*tf.ones(shape=(batch_len,1),dtype="int64")
  label_length=label_length*tf.ones(shape=(batch_len,1),dtype="int64")

  loss=keras.backend.ctc_batch_cost(y_true,y_pred,input_length,label_length)
  return loss
def model_olustur(input_dim, output_dim, rnn_layers=5, rnn_units=128):
  input_spectrogram = layers.Input((None, input_dim), name="input")
  #Expand the dimension to use 2D CNN.
  x = layers.Reshape((-1, input_dim, 1), name="expand_dim")(input_spectrogram)
  #Convolution layer 1
  x = layers.Conv2D(
      filters=32,
      kernel_size=[11, 41],
      strides=[2, 2],
      padding="same",
      use_bias=False,
      name="conv_1",
  )(x)
  x = layers.BatchNormalization(name="conv_1_bn") (x)
  x = layers.ReLU(name="conv_1_relu") (x)
  x = layers.Conv2D(
      filters=32,
      kernel_size=[11, 21],
      strides=[1, 2],
      padding="same",
      use_bias=False,
      name="conv_2",
  )(x)
  x = layers.Reshape((-1, x.shape[-2]*x.shape[-1]))(x)
  # RNN layers
  for i in range(1, rnn_layers + 1):
    recurrent = layers.GRU(units=rnn_units,activation="tanh",recurrent_activation="sigmoid",use_bias=True,return_sequences=True,reset_after=True,name=f"gru_{i}",)
    x = layers.Bidirectional(recurrent, name=f"bidirectional_{i}", merge_mode="concat")(x)
    if i < rnn_layers:
      x = layers.Dropout(rate=0.5) (x)
  x = layers.Dense(units=rnn_units*2, name="dense_1")(x)
  x = layers.ReLU(name="dense_1_relu")(x)
  x = layers.Dropout (rate=0.5)(x)
  # Classification layer
  output=layers.Dense(units=output_dim + 1, activation="softmax")(x)
  # Model
  model=keras.Model(input_spectrogram, output, name="DeepSpeech_2")
  # Optimizer
  opt=keras.optimizers.Adam(learning_rate=1e-4)
  #Compile the model and return
  model.compile(optimizer=opt, loss=CTCLoss)
  return model

model=model_olustur(
    input_dim=fft_length // 2+1,
    output_dim=charnum.vocabulary_size(),
    rnn_units=512,
)
model.load_weights("epoch_100.h5")
def decode_batch_predictions(pred):
  input_len=np.ones(pred.shape[0])*pred.shape[1]
  results=keras.backend.ctc_decode(pred,input_length=input_len,greedy=True)[0][0]
  output_metin=[]
  for result in results:
    result=tf.strings.reduce_join(numar(result)).numpy().decode("utf-8")
    output_metin.append(result)
  return output_metin
def Sesden_Metine_Donusturme(ses):
    audio, _ = tf.audio.decode_wav(ses)
    audio = tf.squeeze(audio, axis=-1)
    audio = tf.cast(audio, tf.float32)
    spectrogram = tf.signal.stft(
        audio, frame_length=frame_length, frame_step=frame_step, fft_length=fft_length
    )
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.math.pow(spectrogram, 0.5)
    means = tf.math.reduce_mean(spectrogram, 1, keepdims=True)
    stddevs = tf.math.reduce_std(spectrogram, 1, keepdims=True)
    spectrogram = (spectrogram - means) / (stddevs + 1e-10)
    spectrogram = tf.expand_dims(spectrogram, 0)
    predictions = model.predict(spectrogram)
    metin = decode_batch_predictions(predictions)[0]
    return metin


fs = 16000

print("*"*100)
print("Kayıt Başladı..")
recognizer = sr.Recognizer()
with sr.Microphone(sample_rate=fs) as mic:
    print("dinleniyor...")
    ses = recognizer.listen(mic)
metin = Sesden_Metine_Donusturme(ses.get_wav_data())
print("Metin:", metin)

