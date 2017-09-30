#!/bin/bash

############# Spark procedure (TODO) #################
# <take user_id/data_name>
# mkdir /home/hadoop/Raw/<user_id>;
# cp <data_name> /home/hadoop/Raw/<user_id>/;

# mkdir /var/www/perseus/app/data/uploaded/<user_id>/
# mkdir /var/www/perseus/app/data/uploaded/<user_id>/<raw>
# mv <data_name> /var/www/perseus/app/data/uploaded/<user_id>/<raw> #Not exist: uploaded

# mkdir /var/www/perseus/app/data/uploaded/<user_id>/<processed>

# hdfs dfs -put <filename>

# cd /home/hadoop/project/PERSEUS_Spark/src;

# spark-submit --master yarn --files ClusteringCoefficient.py,Utility.py,Degrees.py,PageRank.py,SVD.py --py-files linalg.zip --executor-memory 1g Driver.py /tmp2_ID_processed.tsv /ii

# hdfs dfs -get <filename> /var/www/perseus/app/data/uploaded/<user_id>/<processed>/

############## Redis callback #####################

