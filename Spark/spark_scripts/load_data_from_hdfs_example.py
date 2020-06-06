# Execution with: $SPARK_HOME/bin/spark-submit ~/spark_scrips/load_data_from_hdfs.py
from pyspark.sql import Row, SparkSession
from pyspark import SparkContext

sc = SparkContext()
spark = SparkSession.builder\
        .getOrCreate()
# .master("local[2]") \
df2 = spark.read.parquet("hdfs://192.168.0.10/user/hadoop/mqtt_data/191217_mqtt_data.parquet")
#df2 = spark.read.load("hdfs://192.168.0.10/user/hadoop/books/example.parquet")
# df2 = spark.read.csv("hdfs://192.168.0.10/user/hadoop/books/example.csv")
# df = spark.read.load("examples/src/main/resources/users.parquet")
df2.show()


