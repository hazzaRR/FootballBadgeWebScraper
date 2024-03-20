from azure.storage.blob import ContainerClient, BlobClient
from credentials import azure_connection_string, azure_container_name
import os

container = ContainerClient.from_connection_string(conn_str=azure_connection_string, container_name=azure_container_name)

CURRENT_PATH = os.getcwd()

images = os.path.join(CURRENT_PATH, "badges")

for filename in os.listdir(images):
    print(filename)
    try:
        with open(os.path.join(images, filename), "rb") as image:
            f = image.read()
            b = bytearray(f)
            container.upload_blob(filename, b)
    except:
        print(f"Skipping upload of image: {filename}")
