# Databricks notebook source
! ls /Volumes/biobank_analytics/uploads/ct-studies/Dicom_Order16/

# COMMAND ----------

# Without databricks.pixels, we need to install pydicom
!pip install pydicom tqdm

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG biobank_analytics;
# MAGIC
# MAGIC -- To clear/reset the table for dev/testing
# MAGIC DROP TABLE IF EXISTS imaging.dicom_instances;
# MAGIC
# MAGIC -- table name is schema.table_name
# MAGIC CREATE TABLE IF NOT EXISTS imaging.dicom_instances
# MAGIC (
# MAGIC    PatientID STRING,
# MAGIC    StudyInstanceUID STRING,
# MAGIC    SeriesInstanceUID STRING,
# MAGIC    SOPInstanceUID STRING,
# MAGIC    AccessionNumber STRING,
# MAGIC    Modality STRING,
# MAGIC    InstitutionName STRING,
# MAGIC    StudyDescription STRING,
# MAGIC    SeriesNumber INT,
# MAGIC    SeriesDescription STRING,
# MAGIC    ImageType0 STRING,
# MAGIC    ImageType1 STRING,
# MAGIC    ImageType2 STRING,
# MAGIC    ImageType3 STRING,
# MAGIC    ImageType4 STRING,
# MAGIC    SliceThickness FLOAT,
# MAGIC    SpacingBetweenSlices FLOAT,
# MAGIC    PixelSpacing0 FLOAT,
# MAGIC    PixelSpacing1 FLOAT,
# MAGIC    ImageRows INT,
# MAGIC    ImageColumns INT,
# MAGIC    SliceLocation FLOAT
# MAGIC );
# MAGIC

# COMMAND ----------

## ModuleNotFoundError: No module named 'databricks.pixels'

#from databricks.pixels import Catalog
#from dbx.pixels import Catalog

#from databricks.pixels.dicom import *

catalog = "biobank_analytics"
schema = "imaging"

# Sample dataset of dicom images
path="/Volumes/biobank_analytics/uploads/ct-studies/Dicom_Order16/"

#catalog = Catalog(spark)
#catalog_df = catalog.catalog(path)
#print(catalog_df)

import glob
import os
import pydicom
import tqdm


def row_value(row, key, index=0, default='NA'):
    if key in row:
        val=row[key]
        if isinstance(val, list):
            return val[index]
        else:
            return val
    else:
        return default

def row_to_list(row):
    dat = [row_value(row, 'PatientID')]
    dat.append(row_value(row, 'StudyInstanceUID'))
    dat.append(row_value(row, 'SeriesInstanceUID'))
    dat.append(row_value(row, 'SOPInstanceUID'))
    dat.append(row_value(row, 'AccessionNumber'))
    dat.append(row_value(row, 'Modality'))
    dat.append(row_value(row, 'InstitutionName'))
    dat.append(row_value(row, 'StudyDescription'))
    dat.append(int(row_value(row, 'SeriesNumber')))
    dat.append(row_value(row, 'SeriesDescription'))
    dat.append(row_value(row, 'ImageType0'))
    dat.append(row_value(row, 'ImageType1'))
    dat.append(row_value(row, 'ImageType2'))
    dat.append(row_value(row, 'ImageType3'))
    dat.append(row_value(row, 'ImageType4'))
    dat.append(float(row_value(row, 'SliceThickness', default=0)))
    dat.append(float(row_value(row, 'SpacingBetweenSlices', default=0)))
    dat.append(float(row_value(row, 'PixelSpacing0', default=0)))
    dat.append(float(row_value(row, 'PixelSpacing1', default=0)))
    dat.append(int(row_value(row, 'ImageRows', default=0)))
    dat.append(int(row_value(row, 'ImageColumns',default=0)))
    dat.append(float(row_value(row, 'SliceLocation',default=0)))
    return(dat)

schema_string="PatientID STRING,StudyInstanceUID STRING,SeriesInstanceUID STRING,SOPInstanceUID STRING,AccessionNumber STRING,Modality STRING,InstitutionName STRING,StudyDescription STRING,SeriesNumber int,SeriesDescription STRING,ImageType0 STRING,ImageType1 STRING,ImageType2 STRING,ImageType3 STRING,ImageType4 STRING,SliceThickness float,SpacingBetweenSlices float,PixelSpacing0 float,PixelSpacing1 FLOAT,ImageRows int,ImageColumns int,SliceLocation float"


# get all study directories
study_dirs = [ os.path.join(path,i) for i in os.listdir(path) if os.path.isdir(os.path.join(path,i)) ]

# fields to pull out
fields = ('PatientID','StudyInstanceUID','SeriesInstanceUID','SOPInstanceUID','AccessionNumber', 'Modality','InstitutionName','StudyDescription','SeriesNumber','SeriesDescription','ImageType','SliceThickness','SpacingBetweenSlices','PixelSpacing','Rows','Columns','SliceLocation')


# Abbreviate the list for testing
dat_dicts=[]

study_dirs=study_dirs[0:10]

#for i in tqdm.tqdm(range(0,4)):
for i in tqdm.tqdm(range(0,len(study_dirs))):

    # Here we have .dcm files but sometimes they are "extension-less"
    study_files = glob.glob(os.path.join(study_dirs[i],"*.dcm"))

    # Abbreviate the list for testing
    for f in study_files:

        dat = pydicom.dcmread(f, stop_before_pixels=True)
        row = {k: dat.get(k, None) for k in fields}

        # type casting
        if row['SeriesNumber'] is not None:
            row['SeriesNumber'] = int(row['SeriesNumber'])
        else:
            row['SeriesNumber'] = int(0)

        row['ImageRows'] = int(row['Rows'])
        row['ImageColumns'] = int(row['Columns'])

        if row['SliceThickness'] is not None:
            row['SliceThickness'] = float(row['SliceThickness'])
        else:
            row['SliceThickness'] = float(0)

        if row['SliceLocation'] is not None:
            row['SliceLocation'] = float(row['SliceLocation'])
        else:
            row['SliceThickness'] = float(0)

        if row['SpacingBetweenSlices'] is not None:
            row['SpacingBetweenSlices'] = float(row['SpacingBetweenSlices'])
        else:
            row['SpacingBetweenSlices'] = float(0)

        row['StudyInstanceUID'] = str(row['StudyInstanceUID'])
        row['SeriesInstanceUID'] = str(row['SeriesInstanceUID'])
        row['SOPInstanceUID'] = str(row['SOPInstanceUID'])

        # stretch out vectors
        for j in range(0,5):
            if j < len(row['ImageType']):
                row['ImageType'+str(j)] = row['ImageType'][j]
            else:
                row['ImageType'+str(j)]="NA"
        del row['ImageType']

        if row['PixelSpacing'] is not None:
            row['PixelSpacing0'] = float(row['PixelSpacing'][0])
            row['PixelSpacing1'] = float(row['PixelSpacing'][1])
        else:
            row['PixelSpacing0'] = 0
            row['PixelSpacing1'] = 0
        del row['PixelSpacing']

        dat_dicts.append(row)

df = spark.createDataFrame(dat_dicts, schema=schema_string)

print(df)
display(df)

df.write.mode("overwrite").saveAsTable("biobank_analytics.imaging.dicom_instances")

print("Done")





# COMMAND ----------


