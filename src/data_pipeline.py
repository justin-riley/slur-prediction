from text_handlers import *
from pandas import read_csv

data_dir = '/home/justin/.local/share/xdg/media/documents/textfiles/galvanize/slur-prediction/'
filename='data_with_n_grams.csv'

data = read_csv(data_dir+filename)

blowup_cols = [col for col in data if col.endswith('gram')]

for col in blowup_cols:
    data = make_dummies(data,col)

print(data.shape)
