from math import inf
from collections import deque, defaultdict

from pyspark import SparkContext
from pyspark.sql.session import SparkSession
import pyspark.sql.functions as F

sc = SparkContext()
spark = SparkSession(sc)


edges_df = spark.read.text("hdfs:///data/twitter/twitter.txt")

edges_list = (edges_df.withColumn("from", F.split(F.col("value"), "\t").getItem(1))
                      .withColumn("to", F.split(F.col("value"), "\t").getItem(0))
                      .drop("value"))

graph_df = (edges_list.groupBy("from").agg(F.collect_list("to").alias("to_nodes")))


unique_nodes = (edges_list
                .select(F.col("from").alias("node"))
                .union(edges_list
                       .select(F.col("to").alias("node")))
                .distinct())


unique_nodes_list = list(map(lambda row: row["node"], unique_nodes.collect()))


graph = defaultdict(list)
for row in graph_df.collect():
    graph[row["from"]].extend(row["to_nodes"])


d = defaultdict(int)
used = defaultdict(bool)

for node in unique_nodes_list:
    d[node] = inf
    used[node] = False


def bfs(s):
    d[s] = 0
    deq = deque()
    deq.append(s)
    used[s] = True
    while len(deq) != 0:
        v = deq.popleft()
        for u in graph[v]:
            if not used[u]:
                used[u] = True
                deq.append(u)
                d[u] = d[v] + 1


bfs("12")

print(d["34"])

spark.stop()
              
