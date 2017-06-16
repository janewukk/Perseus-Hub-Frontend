import pandas as pd
import sys
import time

def create_edges_sql(edges_input_filename, edges_sql_filename):
    data = pd.read_csv(edges_input_filename, sep='\t', skipinitialspace=True, escapechar="\\", header=None)

    edges_sql = open(edges_sql_filename, 'w')

    for (fromNode, toNode, weight) in zip(data[0], data[1], data[2]):
        insert_string = "INSERT INTO app_edge (fromNode, toNode, weight) VALUES (" + str(fromNode) + "," + str(toNode) + "," + str(weight) + ");\n"
        edges_sql.write(insert_string)
    edges_sql.close()

def create_data_sql(data_input_filename, data_sql_filename):
    data = pd.read_csv(data_input_filename, sep=',', skipinitialspace=True, escapechar="\\", header=None, dtype=str)

    data_sql = open(data_sql_filename, 'w')
    arr = []*29
    for arr in zip(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7],
                data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15],
                data[16], data[17], data[18], data[19],data[20], data[21], data[22], data[23],
                data[24], data[25], data[26], data[27], data[28]):
        columnNames = """(nodeid, degree, count, pagerank, pagerank_t, pagerank_t_count, clustering_coefficient,
                        clustering_coefficient_t, clustering_coefficient_t_count, v_1, v_2, v_3, v_4, v_5, v_6,
                        v_7, v_8, v_9, v_10, v_1_t, v_2_t, v_3_t, v_4_t, v_5_t, v_6_t, v_7_t, v_8_t, v_9_t,
                        v_10_t, dataset_id)"""
        vals = "("
        for i in range(len(arr)):
            vals += arr[i] + ", "
        # Add the value for dataset_id
        vals += "1);\n"
        insert_string = "INSERT INTO app_node " + columnNames + " VALUES " + vals
        data_sql.write(insert_string)
    data_sql.close()

def main():
    edges_input_filename = "data/edges.txt"
    data_input_filename = "data/full_data_set3.csv"
    edges_sql_filename = "edges_set1.sql"
    data_sql_filename = "data_set3.sql"
    # create_edges_sql(edges_input_filename, edges_sql_filename)
    create_data_sql(data_input_filename, data_sql_filename)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print "Done, total running time was:", (time.time()-start_time), "seconds"