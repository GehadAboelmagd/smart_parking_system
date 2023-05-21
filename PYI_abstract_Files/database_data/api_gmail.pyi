from .enm import enm as enm
from _typeshed import Incomplete
from email.mime.image import MIMEImage as MIMEImage
from google.oauth2 import service_account as service_account

mime_types: Incomplete
SCOPES: Incomplete

def refresh_credentials(creds) -> None: ...

client_secret_path: str
token_path: str

def gmail_setup(): ...
def get_sys_pass(is_auto: bool = ...): ...

sys_key_path: str

def main_gmail(_to_email: str, _from_email: str = ..., _msg_title: str = ..., _msg_content: str = ..., attach_file: bool = ..., file_path: str = ...) -> enm: ...
