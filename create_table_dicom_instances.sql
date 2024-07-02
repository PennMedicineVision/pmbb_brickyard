-- Databricks notebook source
USE CATALOG biobank_analytics;

-- To clear/reset the table
-- DROP TABLE IF EXISTS imaging.dicom_instances;

-- table name is schema.table_name
CREATE TABLE IF NOT EXISTS imaging.dicom_instances
(
   PatientID STRING,
   StudyInstanceUID STRING,
   SeriesInstanceUID STRING,
   SOPInstanceUID STRING,
   AccessionNumber STRING,
   Modality STRING,
   InstitutionName STRING,
   StudyDescription STRING,
   SeriesNumber INT,
   SeriesDescription STRING,
   ImageType0 STRING,
   ImageType1 STRING,
   ImageType2 STRING,
   ImageType3 STRING,
   ImageType4 STRING,
   SliceThickness FLOAT,
   SpacingBetweenSlices FLOAT,
   PixelSpacing0 FLOAT,
   PixelSpacing1 FLOAT,
   ImageRows INT,
   ImageColumns INT,
   SliceLocation FLOAT
);



