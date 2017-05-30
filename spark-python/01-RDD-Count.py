import sys
from pyspark import SparkContext, SparkConf

dataFile =  "/home/spark/spark-cluster-analysis/sampledata/memberFile"

conf = SparkConf().setAppName("Read Weak Member Test001 app")
sc = SparkContext(conf=conf)

dataRDD = sc.textFile(dataFile).cache()

numA = dataRDD.filter(lambda s: 'tony' in s).count()
numB = dataRDD.filter(lambda s: 'mary' in s).count()

print "Lines with tony : %s , lines with mary: %s" % (numA,numB)

sc.stop()
