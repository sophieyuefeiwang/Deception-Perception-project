import boto3

client = boto3.client(
    's3',
    aws_access_key_id='AKIAW4LB2YT6GQH7ZF4I',
    aws_secret_access_key='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',
)


def download_from_s3(client, bucket: str, file_download: str,  save_directory: str) -> None:
    """
    Download a file from S3
    """
    client.download_file(bucket, file_download, save_directory + file_download)


def download_model_s3(save_directory: str) -> None:
    """
    Downloads all the model files from S3
    """
    bucket = 'deceptionperception'
    files = ['config.json', 'pytorch_model.bin', 'training_args.bin']

    for file in files:
        download_from_s3(client, bucket, file, save_directory)