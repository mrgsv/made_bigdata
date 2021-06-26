import re
import itertools

from pyspark import SparkContext


WORD = "narodnaya"
sc = SparkContext()

wiki_rdd = sc.textFile("hdfs:///data/wiki/en_articles_part")
words_rdd = (
    wiki_rdd
    .map(lambda x: x.split('\t', 1))
    .map(lambda content: re.findall(r"\w+", content[1]))
    .map(lambda words: list(map(lambda word: word.lower(), words)))
)

def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)

bigrams_rdd = (
    words_rdd
    .flatMap(lambda x: list(pairwise(x)))
    .filter(lambda pair: pair[0] == WORD)
    .map(lambda pair: ("_".join(pair), 1))
    .reduceByKey(lambda x, y: x + y)
    .sortByKey(ascending=True)
    .map(lambda pair: pair[0] + "\t" + str(pair[1]))
)

for bigram in bigrams_rdd.collect():
    print(bigram)
