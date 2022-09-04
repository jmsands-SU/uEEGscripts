from operator import truediv
from google.cloud import storage
import time
from google.oauth2 import service_account
import datetime

#changeprojectname
project = 'ueegproject'
credentials = service_account.Credentials.from_service_account_file(
    'ueegproject-c9b668074a47.json')
bucket_name = 'ueegbucket'

now = datetime.datetime.now()
local_file_name = "..\quals\ssvep_ch1_0414_15Hz.bin"
remote_file_name = now.strftime("%m_%d_%Y")+"_ch1.bin"
temp_file_name = "tempfile"
chunk_time = 5

local_file_name2 = "..\quals\ssvep_ch2_0414_15Hz.bin"
remote_file_name2 = now.strftime("%m_%d_%Y")+"_ch2.bin"
temp_file_name2 = "tempfile2"


def upload_blob_from_stream(bucket, file_obj, destination_blob_name,temp_file):
    """Uploads bytes from a stream or other file-like object to a blob."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The stream or file (file-like object) from which to read
    # import io
    # file_obj = io.StringIO()
    # file_obj.write("This is test data.")

    # The desired name of the uploaded GCS object (blob)
    # destination_blob_name = "storage-object-name"

    # Construct a client-side representation of the blob.
    blob = bucket.blob(destination_blob_name)

    # Rewind the stream to the beginning. This step can be omitted if the input
    # stream will always be at a correct position.
    # file_obj.seek(0)

    # Upload data from the stream to your bucket.
    blob.upload_from_string(file_obj.read())

    #Copy to temp file so that the first one isn't missing from the live update
    temp_blob = bucket.blob(temp_file)
    sources = [blob]
    temp_blob.compose(sources)
    # blob.upload_from_file(file_obj)

    print(
        f"Stream data uploaded to {destination_blob_name}."
    )

def append_blob_from_stream(bucket, file_obj, destination_blob_name,temp_file):
    blob = bucket.blob(destination_blob_name)
    temp_blob = bucket.blob(temp_file)
    temp_blob.upload_from_string(file_obj.read())

    sources = [bucket.get_blob(destination_blob_name), temp_blob]
    blob.compose(sources)
    print(
        f"Append data uploaded to {destination_blob_name}."
    )



def keepSync(fileobj,fileobj2,bucket_name,blobName,blobName2):
    i = 0
    storage_client = storage.Client(project=project,credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    upload_blob_from_stream(bucket,fileobj,blobName,temp_file_name)
    upload_blob_from_stream(bucket,fileobj2,blobName2,temp_file_name2)
    while True:
        time.sleep(chunk_time)
        append_blob_from_stream(bucket,fileobj,blobName,temp_file_name)
        append_blob_from_stream(bucket,fileobj2,blobName2,temp_file_name2)

f = open(local_file_name,"rb")
f2 = open(local_file_name2,"rb")
# f = open("synctestdata.txt", "rb")
keepSync(f,f2,bucket_name,remote_file_name, remote_file_name2)
# upload_blob("ueegbucket", "synctestdata.txt", "test_file.txt")