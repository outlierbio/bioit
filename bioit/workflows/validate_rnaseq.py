import subprocess

import pandas as pd
import vcf
import luigi
import luigi.s3

CGHUB_PUBLIC_KEY = 'https://cghub.ucsc.edu/software/downloads/cghub_public.key'

maf = pd.read_csv('/path/to/maf')


class GTDownload(luigi.Task):

    analysis_id = luigi.Parameter()

    def run(self):
        cmd = '''docker run --rm -v /mnt/scratch:/scratch outlierbio/gtdownload \
                   "gtdownload -c {keypath} -p /scratch --max-children 8 -v {analysis_id} && \
                    aws s3 cp {src} {dst} --recursive"
              '''.format(keypath=CGHUB_PUBLIC_KEY, analysis_id=self.analysis_id,
                         src='/scratch/' + self.analysis_id, dst=self.output().path)
        out = subprocess.check_output(cmd, shell=True)

    def output(self):
        s3_path = 's3://outlierbio-data-raw/tcga/{analysis_id}/{analysis_id}.bam'.format(
            analysis_id=self.analysis_id)
        return luigi.s3.S3Target(s3_path)


class ExtractRegion(luigi.Task):

    analysis_id = luigi.Parameter()
    region = luigi.Parameter()

    def requires(self):
        return GTDownload(analysis_id=self.analysis_id)

    def run(self):
        cmd = '''docker run --rm -v /mnt/scratch:/scratch outlierbio/samtools \
                   "aws s3 cp {src} {local} && \
                    samtools view -bh {local} {region} > {out} && \
                    aws s3 cp {out} {dst}"
              '''.format(src=self.input().path, local='/scratch/tmp.bam', region=self.region,
                         out='/scratch/out.bam', dst=self.output().path)
        out = subprocess.check_output(cmd, shell=True)

    def output(self):
        s3_path = 's3://outlierbio-data/tcga/{analysis_id}/{region}.bam'.format(
            analysis_id=self.analysis_id, region=self.region.replace(':', '_'))
        return luigi.s3.S3Target(s3_path)


class Mutect(luigi.Task)

    analysis_id = luigi.Parameter()
    region = luigi.Parameter()

    def requires(self):
        return ExtractRegion(analysis_id=self.analysis_id, region=self.region)

    def run(self):
        pass

    def output(self):
        return luigi.s3.S3Target(self.input().path.replace('.bam', '.vcf'))


class RunSample(luigi.WrapperTask):

    sample_id = luigi.Parameter()

    def requires(self):
        for row in maf.iterrows():
            analysis_id = get_analysis_id(self.sample_id)
            region = row['Chromosome', 'Start']
            yield Mutect(analysis_id=analysis_id, region=region)

    def run(self):
        with self.input().open() as f:
            variants = list(vcf.VCFReader(f))

        maf['rna_af'] = maf['genome_change'].map(lambda gc: get_af(gc, variants))

        with self.output().open('w') as f:
            maf.to_csv(f, index=False)

    def output(self):
        return luigi.s3.S3Target(self.input().path.replace('.maf', 'rna_af.maf'))
