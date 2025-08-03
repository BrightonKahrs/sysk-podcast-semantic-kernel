# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "b07d162e-8950-4f65-a962-233be2b91e5e",
# META       "default_lakehouse_name": "sysk_bronze_lh",
# META       "default_lakehouse_workspace_id": "204602e2-2a8e-4879-b594-01681dad044d",
# META       "known_lakehouses": [
# META         {
# META           "id": "b07d162e-8950-4f65-a962-233be2b91e5e"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Bronze to Silver Notebook
# 
# Build out the silver layer for the podcast data

# CELL ********************

import notebookutils
import json

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Bronze lakehouse
bronze_lh = notebookutils.lakehouse.get('sysk_bronze_lh')
bronze_lh = bronze_lh.properties['abfsPath']
#print(f'Bronze lakehouse path: {bronze_lh}')

# Silver lakehouse
silver_lh = notebookutils.lakehouse.get('sysk_silver_lh')
silver_lh = silver_lh.properties['abfsPath']
#print(f'Silver lakehouse mount path: {silver_lh}')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

json_folder_path = f'{bronze_lh}/Files/raw_episode_json'

df = spark.read.json(json_folder_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.createOrReplaceTempView('df')

df_transformed = spark.sql("""
    SELECT
        guid,
        title,
        TO_DATE(publish_date) AS publish_date,
        description,
        TO_TIMESTAMP(datalake_load_date) AS bronze_load_date,
        CURRENT_TIMESTAMP() AS silver_load_date
    FROM df
""")

# display(df_transformed)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_transformed.write.mode('overwrite').option('overwriteSchema','true').format('delta').save(f'{silver_lh}/Tables/dbo/episodes')

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
