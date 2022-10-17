from nltk import pos_tag

def tag(infile, outfile):
    lines = infile.readlines()
    for line in lines:
       tokens = line.split()
       tagged = pos_tag(tokens)
       paired = [word + '/' + tag for (word, tag) in tagged]
       outfile.write(' '.join(paired) + '\n')

input = open('test.splitted', 'r')
output = open('test.tagged', 'w')
tag(input, output)
input.close()
output.close()
