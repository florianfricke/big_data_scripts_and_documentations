# Execution with: $SPARK_HOME/bin/spark-submit --packages org.apache.bahir:spark-streaming-mqtt_2.11:2.3.2 ~/spark_scripts/spark_streaming_mqtt_data_to_hdfs.py
# Note: you can also use the notebook spark_streaming_mqtt_data_to_hdfs.ipynb 

from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, StringType, DoubleType, BooleanType, TimestampType, StructField, StructType

from mqtt import MQTTUtils
from datetime import date

def getSparkSessionInstance(sparkConf):
    if ('sparkSessionSingletonInstance' not in globals()):
        globals()['sparkSessionSingletonInstance'] = SparkSession\
            .builder\
            .config(conf=sparkConf)\
            .getOrCreate()
        # globals()['sparkSessionSingletonInstance'] = SparkSession\
        #     .builder\
        #     .master("local[2]") \
        #     .config(conf=sparkConf)\
        #     .getOrCreate()
    return globals()['sparkSessionSingletonInstance']

def getSchema():
  return StructType([
    StructField("_id", StringType(), True),
    StructField("_rev", StringType(), True),
    StructField("subpart0", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("modul", StringType(), True),
    StructField("value", StringType(), True),
    StructField("topic", StringType(), True),
    StructField("Sensor", StringType(), True)
  ])


if __name__ == "__main__":
    sc = SparkContext(appName="mqttToHdfs")
    ssc = StreamingContext(sc, 1)

    brokerUrl = "tcp://test.mosquitto.org:1883"
    topic = "flfr/#"
    lines = MQTTUtils.createStream(ssc, brokerUrl, topic, None, None)

    # Convert RDDs of the words DStream to DataFrame and run SQL query
    def process(time, rdd):
       # print("========= %s =========" % str(time))
        try:
            # Get the singleton instance of SparkSession
            spark = getSparkSessionInstance(rdd.context.getConf())
            df = spark.read.json(rdd, schema=getSchema())
#            df.printSchema()
#            df.show()
            date_today = date.today().strftime("%y%m%d")
#            df.write.save("hdfs://192.168.0.10:9000/user/hadoop/mqtt_data/example.parquet", format="parquet", mode="append")
            df.write.save("hdfs://192.168.0.10:9000/user/hadoop/mqtt_data/{}_mqtt_data.parquet".format(date_today), format="parquet", mode="append")
            # df.write.save(path='csv', format='csv', mode='append', sep='\t')
        except:
            pass

    lines.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()


