import sys
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext, Row

dataFile =  "/home/spark/spark-cluster-analysis/sampledata/memberFile"

conf = SparkConf().setAppName("Read Weak Member Test002 app")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)


dataRDD = sc.textFile(dataFile).cache()


rowRDD = dataRDD.map(lambda line: line.split(",")).map(lambda x: Row(cid=x[0],uid=x[1]))

clusters = sqlContext.createDataFrame(rowRDD)
clusters.registerTempTable("clusters")

clusters_filtered = sqlContext.sql("SELECT cid, count(uid) FROM clusters group by cid order by count(uid) desc")
clusters_filtered.show(100)

print clusters_filtered
print "==========finished clusters_filtered.show()=============="

sc.stop()
