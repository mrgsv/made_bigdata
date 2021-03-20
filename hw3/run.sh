#!/usr/bin/env bash
set -x

HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar
NUM_REDUCERS=8

hdfs dfs -rm -r -skipTrash "$2"*

# stackexchange
(yarn jar $HADOOP_STREAMING_JAR \
    -D stream.num.map.output.key.fields=2 \
    -D stream.num.reduce.output.key.fields=2 \
    -D mapreduce.partition.keypartitioner.options=-k1.1,1.4 \
    -files mapper.py,reducer.py \
    -mapper "python3 ./mapper.py" \
    -reducer "python3 ./reducer.py" \
    -combiner "python3 ./reducer.py" \
    -numReduceTasks $NUM_REDUCERS \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -input "$1" \
    -output "$2"_tmp &&

# Global sorting as we use only 1 reducer
yarn jar $HADOOP_STREAMING_JAR \
    -D stream.num.map.output.key.fields=3 \
    -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
    -D mapreduce.partition.keycomparator.options="-k1,1n -k3,3nr" \
    -file reducer_top10_by_year.py \
    -mapper cat \
    -reducer "python3 ./reducer_top10_by_year.py" \
    -numReduceTasks 1 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -input "$2"_tmp \
    -output "$2"
) || echo "Error happens"

hdfs dfs -rm -r -skipTrash "$2"_tmp

hdfs dfs -cat "$2"/* | head -20