# Databricks notebook source
! ls /Volumes/biobank_analytics/uploads/ct-studies/Dicom_Order16/

# COMMAND ----------

# Without databricks.pixels, we need to install pydicom
!pip install pydicom

# COMMAND ----------

## ModuleNotFoundError: No module named 'databricks.pixels'

#from databricks.pixels import Catalog
#from dbx.pixels import Catalog

#from databricks.pixels.dicom import *

# Sample dataset of dicom images
path="/Volumes/biobank_analytics/uploads/ct-studies/Dicom_Order16/"

#catalog = Catalog(spark)
#catalog_df = catalog.catalog(path)
#print(catalog_df)

import glob
import os
import pydicom

# get all study directories
study_dirs = [ os.path.join(path,i) for i in os.listdir(path) if os.path.isdir(os.path.join(path,i)) ]

# fields to pull out
fields = ('PatientID','StudyInstanceUID','SeriesInstanceUID','SOPInstanceUID','AccessionNumber',
          'Modality','InstitutionName','StudyDescription','SeriesNumber','SeriesDescription','ImageType')

# Abbreviate the list for testing
for study_dir in study_dirs[0:4]:

    # Here we have .dcm files but sometimes they are "extension-less"
    study_files = glob.glob(os.path.join(study_dir,"*.dcm"))

    # Abbreviate the list for testing
    for f in study_files[0:4]:

        dat = pydicom.dcmread(f)
        row={k: dat.get(k, None) for k in fields}
        print(row)





# COMMAND ----------


