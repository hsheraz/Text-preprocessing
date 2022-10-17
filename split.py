from nltk import sent_tokenize

def split(infile, outfile):
    lines = infile.readlines()
    buffer = ' '.join(line[:-1] for line in lines)
    sents = sent_tokenize(buffer)
    for sent in sents:
      outfile.write(sent + '\n')

input = open('test.txt', 'r')
output = open('test.splitted', 'w')
split(input, output)
input.close()
output.close()
