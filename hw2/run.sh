set -x
HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar


yarn jar $HADOOP_STREAMING_JAR \
        -file mapper.py \
        -file reducer.py \
        -mapper "./mapper.py" \
        -reducer "./reducer.py" \
        -numReduceTasks 2 \
        -input "$1" \
        -output "$2"

hdfs dfs -cat "$2"/part-00000 | head -50
