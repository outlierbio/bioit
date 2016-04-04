import os
from os.path import join
from subprocess import check_output

import click

CGHUB_PUBLIC_KEY = 'https://cghub.ucsc.edu/software/downloads/cghub_public.key'
DEFAULT_NUM_THREADS = 8
TMP_DIR = '/scratch'


def upload_s3(src, dst):
    cmd = 'aws s3 cp {src} {dst}'.format(src, dst)
    out = check_output(src, dst)

@click.command()
@click.argument('analysis_id', help='CGHub analysis ID')
@click.argument('s3path', help='S3 root path to upload the analysis')
@click.option('-k', '--cghub-key', help='Path to CGHub key', default=CGHUB_PUBLIC_KEY)
@click.option('-t', '--tmp-dir', help='Temporary local directory to download data', default=TMP_DIR)
@click.option('-n', '--num-threads', help='Number of download threads', default=DEFAULT_NUM_THREADS)
def gtdownload(analysis_id, s3path, cghub_key, tmp_dir, n_threads):
    """Download ANALYSIS_ID from CGHub and upload to S3PATH.

    Requires GeneTorrent. Download client `gtdownload` must be on PATH. Use
    public key if none provided. Returns analysis subdirectory.
    """
    cmd = 'gtdownload -c {keypath} -p {prefix} --max-children {n_threads} -v {analysis_id}'
    check_output(cmd.format(keypath=cghub_key, prefix=tmp_dir, n_threads=n_threads,
                            analysis_id=analysis_id),
                 shell=True)

    analysis_dir = os.path.join(tmp_dir, analysis_id)
    for fname in os.listdir(analysis_dir):
        local_fpath = join(analysis_dir, fname)
        key_path = join(s3path, analysis_id, fname)
        upload_s3(local_fpath, key_path)

if __name__ == '__main__':
    gtdownload()
