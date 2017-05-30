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

clusters_filtered = sqlContext.sql("SELECT cid, count(uid) as uid_count FROM clusters group by cid having uid_count > 4 order by uid_count desc")
clusters_filtered.show(100)

print clusters_filtered
print "==========finished clusters_filtered.show()=============="


# Output
clusters_out = clusters_filtered.rdd.map(lambda x: "cid: {}, uid_count {}".format(x.cid, x.uid_count))
for c_out in clusters_out.collect():
  print c_out

sc.stop()
