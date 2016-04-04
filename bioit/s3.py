from urlparse import urlsplit
import boto3

client = boto3.client('s3', 'us-east-1')
xfer = boto3.s3.transfer.S3Transfer(client)


def _path_to_bucket_and_key(s3_path):
    '''Split S3 path like s3://bucket/key/path to (bucket, key/path)'''
    (scheme, netloc, path, query, fragment) = urlsplit(s3_path)
    if scheme != 's3':
        raise ValueError('path must begin with "s3"')
    path_without_initial_slash = path.lstrip('/')
    return netloc, path_without_initial_slash


def upload_s3(local_path, s3_path):
    '''Upload local file to S3'''
    dst_bucket, dst_key = _path_to_bucket_and_key(s3_path)
    xfer.upload_file(local_path, dst_bucket, dst_key)


def download_s3(s3_path, local_path):
    '''Download S3 object to local filepath'''
    src_bucket, src_key = _path_to_bucket_and_key(s3_path)
    xfer.download_file(src_bucket, src_key, local_path)
