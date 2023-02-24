import io
from dataclasses import dataclass

import streamlit as st
from dotenv import load_dotenv
from google.cloud import storage
from google.oauth2 import service_account
from PIL import Image

load_dotenv()
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
storage_client = storage.Client(credentials=credentials)


@dataclass
class ImageUri:
    uri: str

    def load(self):
        bucket, path = self.uri.replace("gs://", "").split("/", 1)
        bucket = storage_client.bucket(bucket)
        blob = bucket.blob(path)
        return Image.open(io.BytesIO(blob.download_as_bytes()))
