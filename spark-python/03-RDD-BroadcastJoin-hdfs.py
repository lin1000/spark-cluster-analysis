import sys
import datetime
from pyspark import SparkContext, SparkConf

def  doJoin(key, value, bc):
    try:
        return (key, value, bc.value[key])
    except:
        #return ""
        return (key, value, "no")

def doJoinP(iterator, bc):
    for element in iterator:
        try:
            yield (element[0], element[1], bc.value[element[0]])
        except:
            yield (element[0], element[1], "no")
print datetime.datetime.now().time()

conf = SparkConf().setAppName("RDD Broadcast Join app test")
sc = SparkContext(conf=conf)

#read sfis file and TTT file need to process
#sfisFile = "hdfs:///usidata/windows-Panasonic/sfis\ data/r06\ -\ 1279500.txt"
sfisFile = "hdfs:///usidata/windows-Panasonic/sfis\ data/*"
sfisRDD = sc.textFile(sfisFile).map(lambda line: line.split(",")).map(lambda line: ((line[0].replace("\"","")+"+"+line[1]).replace("\"",""),line))

#print sfisRDD.take(2)

#ttt_file_path = "hdfs:///usidata/windows-Siemens/S75/Processed/S75_KIT001017U272950142_20171121014502869.ttt"
ttt_file_path = "hdfs:///usidata/windows-Siemens/S75/Processed/*20171121*"
tttRDD = sc.textFile(ttt_file_path).map(lambda line: line.split("\t")).map(lambda line: ((line[0]+"+"+line[1].split("/")[2]),line))

#print tttRDD.take(2)

### init broadcast 
ttt_bc = sc.broadcast(tttRDD.collectAsMap())

### ttt map join sfis
ttt_sfis_join = sfisRDD.map(lambda (key,value): doJoin(key, value, ttt_bc)).filter(lambda (key, sfis_value, ttt_value): ttt_value!="no")#.saveAsTextFile("hdfs:///test/")
#print ttt_sfis_join.take(1)

### read pvs file
pvsFile = "hdfs:///usidata/windows-Panasonic/pvs-1206334-nochinese.txt"
pvsRDD = sc.textFile(pvsFile).map(lambda line: line.split(",")).map(lambda line: ((line[2]+"+"+line[7]+"+"+line[6]+"+"+line[8]),line))
#print pvsRDD.take(1)

### re generate combine key
ttt_sfis_join_rekey = ttt_sfis_join.map(lambda (key, sfisdata, tttdata): ((tttdata[2]+"+"+tttdata[4]+"+"+tttdata[11]+"+"+tttdata[7]),(sfisdata,tttdata)))
#print ttt_sfis_join_rekey.take(1)

### init broadcast 2
ttt_sfis_bc = sc.broadcast(ttt_sfis_join_rekey.collectAsMap())

### ttt sfis pvs join
ttt_sfis_pvs_join = pvsRDD.map(lambda (key,value): doJoin(key, value, ttt_sfis_bc)).filter(lambda (key, ttt_sfis_value, pvs_value): pvs_value!="no").saveAsTextFile("hdfs:///test")
#print ttt_sfis_pvs_join.take(6)
print datetime.datetime.now().time()
