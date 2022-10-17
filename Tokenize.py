"""
    Tokenize: using the Professor's code as the skeleton, this code here tokenizes words that come in as a text file using regex.
    The return of the fucntion is a list of tokenized sentences. It uses nltk to divide the text into sentences, which then is used
    as words to tokenize and then appended together at the end as a list. It also does some post processing for
"""

import ply.lex as lex
import re
import nltk

nltk.download('punkt')

# List of token names, always needed
tokens = (
    'LABEL',
    'APOS',
    'HYPH',
    'NUM',
    'PUNC',
    'WORD',
    'DELIM',
    'ERROR'
)


def t_LABEL(t): r"\$DOC\b | \$TITLE\b | \$TEXT\b"; return t


def t_APOS(t): r"(?!'*')(\S*[\w']*)(\w'+\w*)+"; return t


def t_HYPH(t): r"((?:\w+-)+\w+)(?!\S*['])([\w'-]+)"; return t


def t_NUM(t): r"(-?\.*[0-9])(([0-9]*)|([+-]?[0-9]*\.[0-9]*))"; return t


def t_WORD(t): r"[a-zA-Z]\w*[a-zA-Z]|[a-zA-Z]"; return t


def t_PUNC(t): r"""[,'.\/;=\\%*+{@!}\#&`~$(?):\_\-"]+"""; return t


def t_DELIM(t): r"[\s\n\t]+"; return t


# Error handling
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexers
lexer = lex.lex()


def scan(data):
    total_hyphens = []
    count_doc_list = []

    # open file, and split into sentences using nltk
    with open(data, "r") as f:
        text = f.read()
    sentences = nltk.tokenize.sent_tokenize(text)
    sentence_list = []
    list_tokens = []
    list_tokens_whole = []
    list_doc = []

    # loop through each sentence, tokenize each word
    for sentence in sentences:
        lexer.input(sentence)
        total_sentences = ''
        count_tokens = 0
        count_tokens_whole = 0
        count_doc = 0

        while True:
            tok = lexer.token()
            if not tok:
                break
            if tok.type == 'HYPH':
                count = 0
                # count the number of hyphens
                for idx, val in enumerate(tok.value):
                    if val == '-':
                        count += 1
                # post-processing - hyphens
                if (count == 2 and (1 <= len(tok.value.rsplit('-')[1]) <= 2)) or count == 1:
                    tok.value = tok.value
                    # print(tok.value)
                else:
                    tok.value = re.sub(r"(\w)([-])", r"\1 \2 ", tok.value)
                total_hyphens.append(count)

            # post-processing - apostrophes
            if tok.type == 'APOS':
                count = 0
                for idx, val in enumerate(tok.value):
                    if val == "'":
                        count += 1
                if count == 1 and ((len(tok.value.rsplit("'")[0]) == 1 and (len(tok.value.rsplit("'")[1]) > 2)) or (
                        (tok.value.rsplit("'")[1]) == 's') or ((tok.value.rsplit("'")[1]) == 'S')):
                    tok.value = tok.value
                    count_hy = 0
                    for i in tok.value.rsplit("'")[0]:
                        if i == '-':
                            count_hy += 1
                    if count_hy > 2:
                        tok.value = re.sub(r"([-'])", r" \1 ", tok.value)
                elif count == 1 and ((1 <= len(tok.value.rsplit("'")[1]) <= 2) and (
                        ((tok.value.rsplit("'")[1]) != 's') or ((tok.value.rsplit("'")[1]) != 'S'))):
                    tok.value = re.sub(r"(['])", r" \1", tok.value)
                elif count == 2 and ((len(tok.value.rsplit("'")[0]) == 1) and tok.value.rsplit("'")[2] == 's'):
                    tok.value = tok.value
                else:
                    tok.value = re.sub(r"(\w)(['])", r"\1 \2 ", tok.value)
            if tok.type == 'PUNC':
                tok.value = re.sub(r"""((?<!\s)(?=[,'./;=%*+{@!}\#&`~$?:\_\"]))""", r" \1", tok.value)
                tok.value = re.sub(r"""([\w/(')\s-]|[^\w/(')\s-])\s*""", r"\1 ", tok.value)

            # count number of tokens for each sentence in document
            if tok.type != 'LABEL' and not re.findall(r'(\$DOC.*)', tok.value) and not re.findall(r'(\w*-\d.*)', tok.value):
                count_tokens += 1

            # count number of tokens for each sentence for entire data
            if tok.type is not None:
                count_tokens_whole += 1

            total_sentences += tok.value
        sentence_list.append(total_sentences)
        list_tokens.append(count_tokens)
        list_tokens_whole.append(count_tokens_whole)
        # over write file
        with open('articles.tokenized', 'w') as f:
            for item in sentence_list:
                f.write("%s\n" % item)
    return list_tokens, list_tokens_whole

if __name__ == '__main__':
    import sys
    scan(sys.argv[1])


