# connect('nyadb')
#
# simple_report.save()
import datetime

from tensorflow.keras.models import load_model

m = load_model('/home/uiqkos/PycharmProjects/kaggle-digit-recognizer/notebooks/submissions/tuner_search_conv - 1631693154.729186/tuner_conv_model')

print(m.save_weights('w.h5'))
# Model.save_weights()

datetime.datetime.strftime()
