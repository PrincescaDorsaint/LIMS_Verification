#!/usr/bin/env nextflow

// check parameters
if (!new File(params.apitoken).exists()) {
    exit 1, "The API Token does not exist: "+params.apitoken+"\n"
}

if (!new File(params.configurationFile).exists()) {
    exit 1, "The Config File does not exist: "+params.configurationFile+"\n"
}

if (!new File(params.resultDir).exists()) {
    println ("The Nextflow results folder does not exist: "+params.resultDir+"\nCreating one...")
    file(params.resultDir).mkdir()
    if( new File(params.resultDir).exists() ) println("...done") else exit 1, "Cannot create results directory"
}

if (!params.LIMS_URL) {
    exit 1, "LIMS URL parameter is missing."
}

if (!params.source) {
    exit 1, "LIMS source filter parameter is missing."
}

process QueryBioInfo {

    publishDir params.resultDir, mode: 'copy', overwrite: true 
   
    // other configuration
    errorStrategy 'retry'
    maxRetries 3

    input:
    path(apitoken) from params.apitoken
    val(LIMS_URL) from params.LIMS_URL
    val(source) from params.source

    output:
    path('*.csv') into bioinfoFiles_ch

    script:
    """ 
    python queryBioInfo.py ${apitoken} "${LIMS_URL}${source}"
    """
}

process LIMSUpdate {

    // other configuration
    errorStrategy 'retry'
    maxRetries 3

    input:
    path(apitoken) from params.apitoken
    path(configurationFile) from params.configurationFile
    val(LIMS_URL) from params.LIMS_URL
    path(queriedFile) from bioinfoFiles_ch

    script:
    """ 
    python LIMS_Update.py ${apitoken} ${configurationFile} $queriedFile ${LIMS_URL}
    """
}
