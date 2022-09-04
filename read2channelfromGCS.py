from google.cloud import storage
import time
import matplotlib.animation as animation
import matplotlib.pyplot as plt

import numpy as np
from google.oauth2 import service_account

project = 'ueegproject'
credentials = service_account.Credentials.from_service_account_file(
    'ueegproject-c9b668074a47.json')

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)
#x is sample number
#y is value

bucket_name = "ueegbucket"
temp_file_name = "tempfile" #name of file you wnat to read
temp_file_name2 = "tempfile2" 
update_interval = 1000

storage_client = storage.Client(project=project,credentials=credentials)
bucket = storage_client.bucket(bucket_name)
from collections import deque  
x_data = deque('',33000)
y_data = deque('',33000)
x_data2 = deque('',33000)
y_data2 = deque('',33000)
global updates 
updates = 0
global updates2
updates2 = 0

def blob_plot(i):
    """Prints out a blob's metadata."""
    global updates
    global updates2
    blob = bucket.get_blob(temp_file_name)
    if updates != blob.updated:
        updates = blob.updated
        contents = blob.download_as_string()
        newdata = np.fromstring(contents, dtype='single')
        # newdata = contents.split(b'\r\n')
        y_data.extend(map(float, newdata))
        x_data = range(len(y_data))
        ax1.clear()
        ax1.plot(x_data,y_data)
    blob = bucket.get_blob(temp_file_name2)
    if updates2 != blob.updated:
        updates2 = blob.updated
        contents = blob.download_as_string()
        newdata = np.fromstring(contents, dtype='single')
        # newdata = contents.split(b'\r\n')
        y_data2.extend(map(float, newdata))
        x_data2 = range(len(y_data2))
        ax2.clear()
        ax2.plot(x_data2,y_data2)


ani = animation.FuncAnimation(fig, blob_plot, interval=update_interval)
plt.show()
