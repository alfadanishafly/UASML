from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import nltk, pickle, requests, re, joblib
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('stopwords')
nltk.download('punkt')
@csrf_exempt

def check_hatespeech(request):
    if request.method == 'POST':
        data = request.POST.get('text', '')
        
        # Gunakan model machine learning untuk memeriksa kata-kata hatespeech
        is_hatespeech = check_with_machine_learning(data)
        
        # Mengembalikan respons JSON dengan hasil pemeriksaan
        return JsonResponse({'is_hatespeech': is_hatespeech})
    
    # Mengembalikan respons error jika ada masalah dalam permintaan
    return JsonResponse({'error': 'Invalid request'})

def check_with_machine_learning(text):
    # Muat model dari file model.pkl
    model = joblib.load(r'D:\KULIAH !!!!\SEMESTER 6\ML\extension\Hate Speech Classifier.joblib')

    # Preprocessing teks
    processed_text = preprocess_text(text)
    
    # Lakukan prediksi menggunakan model
    prediction = model.predict(processed_text)
    
    # Jika prediksi menunjukkan kata-kata sebagai hatespeech, kembalikan True, jika tidak kembalikan False
    return bool(prediction[0])

def preprocess_text(text):
    # Case folding
    # text = case_folding([text])[0]

    # Tokenisasi teks menjadi kata-kata
    tokens = word_tokenize(text)
    
    # Menghapus stopwords
    stop_words = set(stopwords.words('indonesian'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    
    # Menangani kata slang (jika diperlukan)
    # processed_tokens = replace_slang(lowercase_tokens)
    
    # Menggabungkan kata-kata menjadi teks yang sudah diproses
    processed_text = ' '.join(filtered_tokens)

    # Memuat model TF-IDF
    tfidf = joblib.load(r'D:\KULIAH !!!!\SEMESTER 6\ML\extension\Hate Speech TF-IDF Vectorizer.joblib')

    # Menerapkan TF-IDF pada teks
    tfidf_matrix = tfidf.transform([processed_text])
    
    return tfidf_matrix

def replace_slang(tokens):
    # Mengambil kamus kata slang dari URL
    response = requests.get('https://raw.githubusercontent.com/louisowen6/NLP_bahasa_resources/master/combined_slang_words.txt')
    slang_word = response.content.decode('utf-8')
    slang_dict = {}
    
    if response.status_code == 200:
        slang_lines = slang_word.split('\n')
        for line in slang_lines:
            if line:
                slang_word, expanded_word = line.split(': ')
                slang_dict[slang_word] = expanded_word.strip()
    
    processed_tokens = []
    for token in tokens:
        if token in slang_dict:
            processed_tokens.append(slang_dict[token])
        else:
            processed_tokens.append(token)
    
    return processed_tokens


def case_folding(data):
    temp_data = []
    
    for text in data:
        # Convert text to string if it's not already a string
        if not isinstance(text, str):
            text = str(text)
        
        # Removal of @name[mention]
        text = re.sub(r"(?:\@|https?\://)\S+", "", text)
        
        # Removal of links[https://blabala.com]
        text = re.sub(r"http\S+", "", text)
        
        # Removal of new line
        text = re.sub('\n', '', text)
        
        # Removal of RT
        text = re.sub('RT', '', text)
        
        # Removal of punctuations and numbers
        text = re.sub("[^a-zA-Z^']", " ", text)
        text = re.sub(" {2,}", " ", text)
        
        # Remove leading and trailing whitespace
        text = text.strip()
        
        # Remove whitespace with a single space
        text = re.sub(r'\s+', ' ', text)
        
        # Convert text to lowercase
        text = text.lower()
        
        temp_data.append(text)
    
    return temp_data
