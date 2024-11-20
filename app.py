from flask import Flask
from flask_cors import CORS
from routes.comments import comments_bp
from model import *

import re
import emoji
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.base import TransformerMixin, BaseEstimator

class TextPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self):
        # Initialize any components or settings here if needed
        self.stop_words = set(stopwords.words('english'))
        self.hinglish_stopwords = {
      'main', 'tum', 'wo', 'kya', 'ka', 'ki', 'ke', 'hai', 'ho', 'tha', 'thi', 'the', 'ko',
      'mein', 'se', 'par', 'aur', 'ye', 'ha', 'hai', 'bhi', 'nahi', 'ko', 'tha', 'hota',
      'hoti', 'kiya', 'kiye', 'kar', 'raha', 'rahe', 'rahi', 'karte', 'karna', 'wala',
      'wale', 'wali', 'liye', 'gaya', 'gayee', 'sath', 'us', 'un', 'unka', 'unki', 'unka',
      'tumhe', 'mujhe', 'tujhe', 'aap', 'ham', 'hum', 'kaun', 'koi', 'kyu', 'kyun', 'aisa',
      'waise', 'sab', 'ab', 'tab', 'jab', 'tumhara', 'hamara', 'aaj', 'kal', 'yahan',
      'wahan', 'kuch', 'kaafi', 'bahut', 'zyada', 'thoda', 'chhota', 'bada', 'chahiye',
      'jaise', 'yahi', 'vohi', 'har', 'kisi', 'is', 'uska', 'unke', 'unki', 'kaise', 'kaisi',
      'kaisa', 'kuchh', 'zaroori', 'hoon', 'thik', 'abhi', 'itna', 'aisa', 'waqt', 'yahaan',
      'keval', 'zarurat', 'vaise', 'agar', 'ab', 'apna', 'apne', 'kyun', 'kis', 'kiska',
      'kisne', 'kon', 'kaunsa', 'kaunsi', 'kaunse', 'unki', 'unka', 'koi', 'jo', 'jis',
      'uske', 'jinke', 'inko', 'unko', 'karke', 'karte', 'karne', 'karna', 'kuch', 'kaafi',
      'bahot', 'ek', 'baad', 'bad', 'hoon', 'thi', 'hua', 'ho', 'tha', 'jise', 'ka', 'ki',
      'jo', 'unki', 'us', 'apne', 'hamare', 'jaise', 'kaam', 'hai', 'par', 'waqt', 'bada',
      'hoga', 'hone', 'ke', 'liye', 'kisi', 'tak', 'kya', 'ja', 'woh', 'ye', 'fir', 'ab',
      'ho', 'tha', 'thi', 'tha', 'par', 'ya', 'yahaan', 'hote', 'kar', 'tha', 'ya', 'fir',
      'aur', 'wohi', 'kisi', 'unko', 'jaise', 'bhi', 'de', 'jahan', 'kaafi', 'upar', 'neeche',
      'yehi', 'vo', 'jo', 'jao', 'chal', 'ho', 'bahar', 'andar', 'dur', 'pass', 'kam', 'zyada',
      'rahe', 'rahi', 'reh', 'jana', 'jaane', 'chalna', 'rukna', 'lena', 'dena', 'hona',
      'rehna', 'jana', 'pahuch', 'aana', 'chale', 'baithe', 'uthe', 'uthna', 'aate', 'jaate',
      'dekho', 'dekha', 'jaana', 'pura', 'poora', 'kitna', 'kitni', 'kitne', 'jo', 'ab',
      'tak', 'jaake', 'kaise', 'bahut', 'poora', 'aadha', 'bada', 'chhota', 'bade', 'chhote',
      'zyada', 'thoda', 'zyaada', 'bhi', 'ho', 'hote', 'kar', 'ja', 'se', 'par', 'mein', 'aur',
      'ab', 'fir', 'ke', 'liye', 'nahi', 'hoon', 'hai', 'ho', 'jao', 'thi', 'tha', 'yeh',
      'woh', 'ismein', 'aap', 'tum', 'hum', 'unko', 'inke', 'unka', 'kuch', 'jaisa', 'waise',
      'kaun', 'kis', 'ko', 'kyu', 'se', 'kisne', 'kuch', 'usko', 'kaha', 'yahan', 'aapko',
      'hamko', 'tujhe', 'mujhe', 'kaun', 'jaise', 'is', 'ko', 'in', 'un', 'ka', 'koi', 'kuch',
      'kya', 'kyun', 'ho', 'jab', 'kis', 'par', 'kaun', 'kuch', 'unko', 'inko', 'karke',
      'thoda', 'bada', 'chhota', 'apne', 'uske', 'unki', 'inke', 'kaha', 'kar', 'ke', 'liye',
      'le', 'par', 'fir', 'ye', 'wo', 'jo', 'kis', 'waise', 'zindagi', 'ghar', 'chal', 'idhar',
      'udhar', 'samay', 'jagah', 'kaha', 'piche', 'aage', 'aaj', 'kal', 'hoon', 'fir', 'abhi',
      'kitna', 'jaisa', 'vaisa', 'aisa', 'aisey', 'dekha', 'dekhi', 'dekho', 'chal', 'chala',
      'gaya', 'gayee', 'raha', 'rahe', 'rahi', 'jaata', 'jaati', 'karti', 'karta', 'kar',
      'karte', 'karna', 'jaana', 'aana', 'bol', 'bola', 'boli', 'bolta', 'bolte', 'bolti',
      'hoon', 'karke', 'karte', 'ke', 'liye', 'ek', 'do', 'teen', 'char', 'paanch', 'chhe',
      'saath', 'aath', 'nau', 'das', 'gyaarah', 'baarah', 'ka', 'mein', 'ke', 'liye', 'par',
      'ya', 'aur', 'lekin', 'agar', 'jo', 'jab', 'fir', 'aise', 'kyu', 'kya', 'sab', 'kyon',
      'thoda', 'jyada', 'tum', 'mai', 'tha', 'the', 'hai', 'hoon', 'ho', 'thi', 'tha', 'usne',
      'usko', 'apne', 'unka', 'unki', 'unka', 'uske', 'jinke', 'ye', 'vo', 'jo', 'kisi', 'kaise',
      'kaun', 'kya', 'kyun', 'kisne', 'jisme', 'inke', 'inke', 'wohi', 'jaise', 'aise', 'vah',
      'yehi', 'abhi', 'thik', 'saath', 'ye', 'vo', 'yeh', 'yahaan', 'vahaan', 'vah', 'jab',
      'aata', 'aate', 'jata', 'jaate', 'aati', 'jati', 'pehle', 'badme', 'poora', 'adhura',
      'bahot', 'aadha', 'kaafi', 'kitna', 'kitni', 'kitne', 'aur', 'par', 'kar', 'karte',
      'karke', 'karna', 'uske', 'iske', 'inke', 'bade', 'chhote', 'aise', 'jaise', 'ab', 'tab',
      'sab', 'sirf', 'jise', 'jis', 'inhe', 'unhe', 'isse', 'usse', 'kitna', 'kitni', 'kitne',
      'kuch', 'sabhi', 'sabse', 'zyada', 'thoda', 'hoon', 'hai', 'ho', 'tha', 'thi', 'the',
      'kisi', 'aaj', 'kal', 'wohi', 'tumhe', 'mujhe', 'hamko', 'aapko', 'jinka', 'uske',
      'inke', 'uske', 'inke', 'kuch', 'isme', 'usme', 'kis', 'kaise', 'kahan', 'kahaan', 'usko',
      'inko', 'aap', 'unke', 'inhe', 'unko', 'aise', 'waise', 'jab', 'fir', 'par', 'yahaan',
      'vahaan', 'ismein', 'usmein', 'iske', 'iske', 'waqt', 'samay', 'samay', 'samjha',
      'samjhi', 'samajh', 'samajhna', 'samajhte', 'samjhte', 'samjhna', 'samajhkar', 'samjhaane',
      'samjhane', 'kar', 'karte', 'kiya', 'kiye', 'kiye', 'karna', 'karte', 'dekhna', 'dekhte',
      'dikhte', 'dikhte', 'dikha', 'dikhaya', 'dikhaaye', 'chal', 'chalne', 'chalte', 'jana',
      'jaa', 'jaa', 'gaye', 'gaya', 'aa', 'aaya', 'aa', 'jaye', 'chale', 'chala', 'gayi', 'gaye',
      'kar', 'karte', 'kiya', 'kiye', 'karte', 'dikh', 'dikha', 'dekh', 'dekha', 'dikhaya',
      'chal', 'chalne', 'chala', 'jana', 'jaane', 'pooch', 'poocha', 'poochte', 'poochna',
      'puchha', 'puchhna', 'pucha', 'puchhna', 'puchho', 'pucho', 'puchha', 'kuch', 'isse',
      'usne', 'kar', 'jaisa', 'aisa', 'jaise', 'ab', 'tab', 'samay', 'samajh', 'jaane', 'jaa',
      'gaye', 'jaa', 'chala', 'gayi', 'kiya', 'kiye', 'kiya', 'karte', 'karna', 'dekha', 'dikha',
      'dikhaya', 'aaya', 'aa', 'aayi', 'gayi', 'chali', 'chale', 'chalna', 'pucha', 'poocha',
      'poochha', 'samajh', 'samajhte', 'samajhne', 'samjha', 'samjhaya', 'samajhte', 'samjhna',
      'karna', 'karne', 'karte', 'hona', 'hote', 'ho', 'tha', 'thi', 'the', 'hua', 'hue', 'kar',
      'karke', 'karte', 'karna', 'kiye', 'kaam', 'yehi', 'waise', 'aise', 'vaise', 'aisi', 'kitna',
      'kitni', 'kitne', 'bahut', 'poora', 'aadha', 'thoda', 'kaafi', 'zyada', 'zyaada', 'bahut',
      'pura', 'poora', 'kis', 'kya', 'kyun', 'kaise', 'kaun', 'ab', 'tab', 'fir', 'kar', 'karte',
      'karna', 'kiya', 'kiye', 'karke', 'kaafi', 'bahut', 'kam', 'zyada', 'ka', 'ki', 'ke', 'hoon',
      'hu', 'hai', 'ho', 'hoon', 'the', 'thi', 'tha', 'unka', 'inki', 'unka', 'inke', 'inke',
      'unki', 'unka', 'inke', 'unki', 'inke', 'yeh', 'vah', 'ismein', 'ismein', 'uske', 'inke',
      'inke', 'ab', 'ja', 'jaa', 'jaao', 'aayi', 'aa', 'aaye', 'pooch', 'poocha', 'poocha', 'karke'
    }
        self.normalization_dict = {
        'nahi':'not',
        'nhi':'not',
        'tum': 'tu',  # Normalizing 'tum' to 'tu'
        'kaafi': 'kafi',  # Handling spelling variations
        'hoon': 'hu',  # Shortening the word
        'hain': 'hai',  # Plural to singular form
        'bhi': 'bi',  # Common abbreviation
        'main': 'me',  # Normalizing pronouns
        'raha': 'reh',  # Shortening verbs
        'rahi': 'reh',
        'rahe': 'reh',
        'kya': 'ky',  # Common casual abbreviation
        'nahi': 'na',  # Common shortening
        'acha': 'achha',  # Normalizing informal spelling variations
        'bahut': 'bhot',  # Normalizing informal abbreviations
        'mein': 'me',  # Pronoun normalization
        'matlab': 'mltb',  # Common short form
        'ho': 'h',  # Verb normalization
        'koi': 'koy',  # Casual spellings
        'sab': 'sb',  # Short form
        'haan': 'ha',  # Casual speech
        'chalo': 'chl',  # Shortened verbs
        'ab': 'abhi',  # Time reference standardization
        'zyada': 'zyaada',  # Variations of more
        'tumhe': 'tuje',  # Pronoun normalization
        'kuch': 'kch',  # Common abbreviations
        'jaisa': 'jaise',  # Variant forms
        'kitna': 'kitne',  # Plural form adjustment
        'pichle': 'pichli',  # Gender adjustment
        'yeh': 'ye',  # Casual abbreviation
        'voh': 'vo',  # Casual abbreviation
        'sabse': 'sbse',  # Common short form
        'shukriya': 'thanks',  # Translation
        'zindagi': 'life',  # Translation
        'kya': 'ky',  # Common abbreviation
        'theek': 'thik',  # Normalizing spellings
    }

    # Clean the text
    def clean_text(self, text):
        # Check if the input is a string before applying regex
        if isinstance(text, str):
            text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)
            text = re.sub(r'\@\w+|\#', '', text)
            text = re.sub(r'[^\w\s]', '', text)
            text = re.sub(r'\d+', '', text)
            text = emoji.demojize(text)
            text = text.lower()
            return text
        else:
          # Handle non-string values (e.g., NaN) by returning an empty string
          return ''

    # Tokenization
    def tokenize_text(self, text):
        return word_tokenize(text)

    # Stopword Removal
    def remove_stopwords(self, tokens):
        combined_stopwords = self.stop_words.union(self.hinglish_stopwords)
        return [word for word in tokens if word not in combined_stopwords]

    # Normalization
    def normalize_text(self, tokens):
        return [self.normalization_dict.get(token, token) for token in tokens]

    # Fit method (no-op for this transformer, needed for the pipeline compatibility)
    def fit(self, X, y=None):
        return self

    # Transform method: applies preprocessing to each text element
    def transform(self, X, y=None):
        processed_texts = []
        for text in X:
            cleaned = self.clean_text(text)
            tokens = self.tokenize_text(cleaned)
            tokens = self.remove_stopwords(tokens)
            tokens = self.normalize_text(tokens)
            processed_texts.append(" ".join(tokens))  # Join tokens back into a single string
        return processed_texts


app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(comments_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
