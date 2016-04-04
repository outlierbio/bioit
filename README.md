# Bio-IT example: RNA-seq validation pipeline

This codebase is a **partially implemented** framework for implementing the toy example described in my talk at Bio-IT. Please note the "partially implemented" part. It is completely untested and only meant to illustrate the concepts. However, with a modest amount of effort it could be upgraded to a completely functional, cloud-enabled workflow, which I may do eventually. Pull requests accepted, if anyone is interested in this actual application.

## Workflow overview
As described in the talk, the goal of this workflow is to automatically use RNA-seq alignments to confirm somatic mutation calls from DNA whole-exome data.

<img src="rnaseq_workflow.png" height="300" width="500">

Luigi Tasks (green rectangles) are created for downloading BAM files from CGHub, extracting RNA-seq reads using `samtools`, calling mutations with `MuTect`, and merging the RNA mutation allele frequencies for each DNA variant back into the original MAF file. The output Luigi Targets for each task are immutable S3 objects

## Architecture
The code is made up of independent, containerized modules (apps), tied together by Luigi workflows. In this example there is only one workflow but once the framework is complete, extensions or completely new workflows can be easily added.

Each app has its own Dockerfile that can optionally inherit from the base Dockerfile in the top-level directory. Credentials (including keys for Amazon S3) are added from the `secrets` folder to the base Docker image for shared use among the apps. (The `secrets` folder is not checked into version control!)

## Building the Docker images
The app-level images inherit from the top-level Dockerfile. Therefore, you have to first `cd` into the top folder of the repo and build the base image:

	$ docker build -t <yourname>/bioit .
	
swapping <yourname> with username for your Docker registry (e.g., DockerHub). Then, adjust the app-level Dockerfiles and build them in the same way (using whatever image names you choose). Finally, adjust the `run` methods in the Luigi Tasks to match the Docker image names you've just built.

## Running the workflow
See the [Luigi docs](https://luigi.readthedocs.org) for details on running Luigi Tasks from the command line. Since any Task can be run, this workflow can be built from the sample or cohort level. To run a sample workflow on a single TCGA sample (for example, TCGA-AB-2929-01), run 

	$ luigi --module bioit.validate_rnaseq RunSample --sample-id=TCGA-AB-2929-01

For the entire TCGA cohort (lung adenocarcinoma, for example), use

	$ luigi --module bioit.validate_rnaseq RunCohort --disease=LUAD
	
