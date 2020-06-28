import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes 

s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
build_bucket = s3.Bucket('portfoliobuild.bksoftaws.com')

portfolio_zip = StringIO.StringIO()
build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)
portfolio_bucket_list = s3.Bucket('bksoftaws.com')

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket_list.upload_fileobj(obj, nm,
        ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        portfolio_bucket_list.Object(nm).Acl().put(ACL='public-read')