# Model

'''
https://docs.python.org/3/howto/regex.html
https://www.nltk.org/book/ch00.html
https://course.spacy.io/en/
'''

class QueryObject:

    def __init__(self, query):
        self.query = query               # original query string (preserved) 
        self.__operations_string = query # duplicate string for trimming and analyzing

        self.remove_stopwords()
        self.identify_intent()
        self.identify_company()

    def remove_stopwords(self):
        pass

    def identify_intent(self):
        pass

    def identify_company(self):
        '''
        https://pypi.org/project/python-Levenshtein/
        '''
        pass
