import re
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
# import nltk
# nltk.download('punkt')
#funtion remove emoji
def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F" # emoticons
                           u"\U0001F300-\U0001F5FF" # symbols & pictographs
                           u"\U0001F680-\U0001F6FF" # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF" # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           u"\U0001f926-\U0001f937"
                           u"\U00010000-\U0010ffff"
                           u"\u2640-\u2642"
                           u"\u2600-\u2B55"
                           u"\u200d"
                           u"\u23cf"
                           u"\u23e9"
                           u"\u231a"
                           u"\ufe0f"
                           u"\u3030"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

# function removes special characters
def standardize_data(row):
    if not isinstance(row, str):
        text = str(row)

    # Define the pattern to match unwanted characters
    pattern = r'[^a-zA-ZÀ-Ỹà-ỹ\s]'  # Keep letters, digits, spaces, and Vietnamese characters

    # Use regex to substitute unwanted characters with an empty string
    cleaned_text = re.sub(pattern, ' ', row)

    return str(cleaned_text.lower())

# function removes stretched letters
def remove_repetitive_characters(text):
    # Define regex pattern to match repetitive characters
    pattern = re.sub(r'(.)\1+', r'\1\1', text)  # Match one character followed by one or more occurrences of the same character
    return pattern

#Teencode normalization function.
def correct_spelling_teencode(text):
    # Dictionary of common teencode and their correct forms
    teencode_dict = {
        'chx': 'chưa',
        'z': 'vậy',
        'd': 'vậy',
        'k': 'không',
        'hok': 'không',
        'ko': 'không',
        'gòi': 'rồi',
        'tui': 'tôi',
        'bt': 'biết',
        'thik':'thích',
        'ch':'chưa',
        'bt': 'biết',
        'h':'giờ',
        'kh': 'không',
        'cx': 'cũng',
        'đỉm': 'điểm',
        'oce': 'ok',
        'oke': 'ok',
        'đc': 'được',
        'ns': 'nói',
        'tc': 'tính chất',
        'tch': 'tính chất',
        'tks': 'cảm ơn',
        'nc': 'nói chuyện',
        'thui': 'thôi',
        'ha': 'hình ảnh',
        'ik': 'đi',
        'auce': 'ok',
        'xink': 'xinh',
        'dth': 'dễ thương',
        'dthw': 'dễ thương',
        'nhe':'nha',
        'nthe': 'như thế',
        'dethun': 'dễ thương',
        'kcj': 'không có gì',
        'kcgi': 'không có gì',
        'ntn': 'như thế này',
        'ng': 'người',
        'mn': 'mọi người',
        'ng': 'mọi người',
        'nma': 'nhưng mà',
        'qlai': 'quay lại',
        'sp': 'sản phẩm',
        'tn': 'tin nhắn',
        'qtam': 'quan tâm',
        'th': 'thôi',
        'nch': 'nói chung',
        'mk': 'mình',
        'nhìu': 'nhiều',
        'tr': 'trời',
        'oi': 'ơi',
        'bth': 'bình thường',
        'sz': 'size',
        'fb': 'facebook',
        'vs': 'với',
        'nhma': 'nhưng mà',
        'tìn': 'tiền',
        'qt':'quan tâm'
         # Add more teencode mappings as needed
    }

    # Tokenize the text into words
    words = word_tokenize(text)

    # Replace teencode with correct forms
    corrected_words = [teencode_dict[word] if word in teencode_dict else word for word in words]

    # Join the corrected words back into a single string
    corrected_text = ' '.join(corrected_words)
    return corrected_text

# Read stopwords from file
with open("vietnamese-stopwords.txt", 'r', encoding='utf-8') as file:
    vietnamese_stopwords = file.readlines()
vietnamese_stopwords = [word.strip() for word in vietnamese_stopwords]

def remove_stopwords(text):
    ps = PorterStemmer()
    stemmed_words = [ps.stem(word) for word in word_tokenize(text) if word not in vietnamese_stopwords]
    review = " ".join(stemmed_words)
    return review

