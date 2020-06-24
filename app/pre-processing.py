from time import time
from csv import DictReader, DictWriter
from bs4 import BeautifulSoup

from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

# from nltk import download
# download('wordnet')
# download('averaged_perceptron_tagger')

from nltk import WordNetLemmatizer, pos_tag
from nltk.corpus import wordnet

print('Preprocessing started')
start_time = time()

# Create function that get part of speech
def getPOS(token):
    tag = pos_tag([token])[0][1][0].upper()
    tag_dict = {
      "J": wordnet.ADJ,
      "N": wordnet.NOUN,
      "V": wordnet.VERB,
      "R": wordnet.ADV
    }
    return tag_dict.get(tag, wordnet.NOUN)

# Settings
path = '../data/'
source_file = 'posts>=0.csv'
results_file = 'preprocessedd-'+source_file
columns = ['id', 'date', 'author', 'body']
word_net = WordNetLemmatizer()

# Create CSV
with open(path+results_file, 'w', errors='surrogatepass') as result_file:
    writer = DictWriter(result_file, fieldnames=columns) 
    writer.writeheader()

# Read posts
with open(path+source_file, "r") as csv_file:
    for post in DictReader(csv_file):
        # Remove HTML tags
        soup = BeautifulSoup(post['body'], 'lxml')
        for tag in soup.find_all('code'):
            tag.decompose()
        post['body'] = soup.get_text().replace('\n', ' ').replace('\r', '')
        # Tokenize, remove stopwords and lemmatize
        post['body'] = [ word_net.lemmatize(token, pos=getPOS(token)) for token in simple_preprocess(post['body'], deacc=True) if token not in STOPWORDS ]
        post['body'] = ' '.join(post['body'])
        # Write in CSV
        with open(path+results_file, 'a', errors='surrogatepass') as result_file:
            writer = DictWriter(result_file, fieldnames=post.keys()) 
            writer.writerow(post)

print('Done in {:0.4f} seconds'.format(time() - start_time))