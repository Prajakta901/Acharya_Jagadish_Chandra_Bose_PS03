import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix 
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))



train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')
validation_df = pd.read_csv('validation.csv')

train_df.dropna(inplace=True)
validation_df.dropna(inplace=True)
test_df.dropna(inplace=True) 

language_distribution = train_df["Language"].value_counts(normalize=True) * 100
print(language_distribution)

# sns.countplot(x=train_df['Language'])
# plt.title("Class Distribution Before Balancing")
# plt.xticks(rotation=90)
# plt.show() 


# Reduce max_features for faster vectorization
vectorizer = TfidfVectorizer(max_features=1000)  # Use only one vectorizer
X_train = vectorizer.fit_transform(train_df['Headline'])
X_val = vectorizer.transform(validation_df['Headline'])
X_test = vectorizer.transform(test_df['Headline'])

y_train = train_df['Language']
y_val = validation_df['Language']
y_test = test_df['Language']

# # Use MultinomialNB for faster predictions
model = MultinomialNB()
model.fit(X_train, y_train)

val_preds = model.predict(X_val)
print("Validation Accuracy:", accuracy_score(y_val, val_preds))
print(classification_report(y_val, val_preds))

test_preds = model.predict(X_test)
print("Test Accuracy:", accuracy_score(y_test, test_preds))
print(classification_report(y_test, test_preds))

def predict_language_with_normal(text):
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)[0]
    return prediction

input_text = "यह एक परीक्षण वाक्य है।" 
predicted_lang = predict_language_with_normal(input_text)
print(f"Predicted Language: {predicted_lang}") 

language_labels = [
    "Odia", "Nepali", "Hindi", "Assamese", "Sanskrit", "Malayalam",
    "Konkani", "English", "Kannada", "Telugu", "Marathi", "Gujarati",
    "Urdu", "Sindhi", "Punjabi", "Bengali", "Kashmiri", "Tamil"
]
language_sentences = [
    "ଏହି ଜଗତ ଅତି ସୁନ୍ଦର |",  
    "यो संसार धेरै सुन्दर छ।",  
    "यह दुनिया बहुत सुंदर है।",  
    "এই বিশ্ব খুব সুন্দর।",       
    "ഈ ലോകം അതിവളരെയോ മനോഹരമാണ്.",  
    "हें जग सुंदर आसा।",  
    "This world is very beautiful.",   
    "ಈ ಜಗತ್ತು ತುಂಬಾ ಸುಂದರವಾಗಿದೆ.",  
    "ఈ ప్రపంచం చాలా అందంగా ఉంది.", 
    "ही दुनिया खूप सुंदर आहे.",  
    "આ દુનિયા ખૂબ સુંદર છે.",    
    "یہ دنیا بہت خوبصورت ہے۔",  
    "اها دنيا تمام سهڻي آهي.",  
    "ਇਹ ਦੁਨਿਆ ਬਹੁਤ ਸੋਹਣੀ ਹੈ।",  
     "এই পৃথিবী খুব সুন্দর।",  
    "یہ دنیا بہت خوبصورت ہے۔", 
    "இந்த உலகம் மிகவும் அழகானது.", 
] 

for i, sentence in enumerate(language_sentences):
    actual_label = language_labels[i]
    predicted_lang = predict_language_with_normal(sentence)
    status = " Correct" if predicted_lang == actual_label else " Wrong"
    print(f"Sentence: {sentence}")
    print(f"Actual Language: {actual_label} | Predicted Language: {predicted_lang} | Status: {status}")
    print("-" * 80) 

def predict_language_with_sample(text):
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)[0]
    return prediction

input_text = "यह एक परीक्षण वाक्य है।"  
predicted_lang = predict_language_with_sample(input_text)
print(f"Predicted Language: {predicted_lang}") 

