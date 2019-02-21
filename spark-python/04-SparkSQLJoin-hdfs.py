import sys
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row
from pyspark.sql.functions import broadcast

dataFile =  "/data/spark/sampledata/memberFile"
dataFile2 = "/data/spark/sampledata/clusterFile"

conf = SparkConf().setAppName("Spark SQL join test app")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)


dataRDD = sc.textFile(dataFile).map(lambda line: line.split(",")).map(lambda x: Row(x[0],x[1]))
dataRDD2 = sc.textFile(dataFile2).map(lambda key: (key , "test"))

member = sqlContext.createDataFrame(dataRDD,['number','name'])
cluster = sqlContext.createDataFrame(dataRDD2, ['number', 'data'])

cluster.join(broadcast(member), ["number"]).show(10)#.write.format("csv").save("hdfs:///test")
sc.stop()
