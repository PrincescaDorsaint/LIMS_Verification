# LIMS Verification

Nextflow pipeline to verify file paths in LIMS and update the FileSize parameter of each existing file in LIMS.

This pipeine queries the LIMS api by passing parameters to LIMS url. Proper configuration file set up is needed to access designated server via ssh & s3.

## Docker:

You can build a Docker with all necessary components with the Dockerfile in the Docker folder. To build the docker image, execute the following statement from the base folder of LIMS_Verification 'docker build -t lims_verification:latest Docker/.' This will build a Docker image named lims_verification:latest, which can then be used in combination with nextflow.

## Running the pipeline:

To run this pipeline set up the proper config file.
nextflow run  main.nf -c nextflow.config