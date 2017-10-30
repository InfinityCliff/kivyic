from __future__ import print_function

from kivy.uix.screenmanager import Screen

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors

from kivy.properties import ListProperty

from apiclient.http import MediaFileUpload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class GoogleLinkScreen(Screen):
    pass


class GoogleLink(object):
    # https://developers.google.com/drive/v3/web/quickstart/python

    _API_KEY = ''
    _CLIENT_SECRET_FILE = './rsc/client_secrets.json'
    APPLICATION_NAME = ''
    LOCAL_STORAGE_PATH = ''
    _CREDENTIAL_PATH = '.credentials/'
    SCOPE = ''
    settings = {}
    service = None

#    def __init__(self, **kwargs):
#        super(GoogleLink, self).__init__(**kwargs)

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        # Authorize server-to-server interactions from Google Compute Engine.

        credential_dir = self.LOCAL_STORAGE_PATH + self._CREDENTIAL_PATH

        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       self.APPLICATION_NAME + '.json')

        store = Storage(credential_path)
        credentials = False
        try:
            credentials = store.get()
        except UserWarning:
            pass

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self._CLIENT_SECRET_FILE, self.SCOPE)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def _settings(self, settings):
        self.LOCAL_STORAGE_PATH = settings.get('LOCAL_STORAGE_PATH', '')
        self.SCOPE = settings.get('SCOPE', '')
        self.APPLICATION_NAME = settings.get('APPLICATION_NAME', '')
        self._API_KEY = settings.get('API_KEY', '')

    def _open_service(self):
        # OAuth 2.0 for Mobile & Desktop Apps
        # https://developers.google.com/identity/protocols/OAuth2InstalledApp

        # Try Sign-In for iOS
        # https://developers.google.com/identity/sign-in/ios/start?configured=true

        # Enable Google Services for your App
        # https://developers.google.com/mobile/add?platform=ios&cntapi=signin&cntapp=Default%20Demo%20App&cntpkg=com.google.samples.quickstart.SignInExample&cnturl=https:%2F%2Fdevelopers.google.com%2Fidentity%2Fsign-in%2Fios%2Fstart%3Fconfigured%3Dtrue&cntlbl=Continue%20with%20Try%20Sign-In

        # Add Google Sign-In to Your iOS App
        # https://developers.google.com/identity/sign-in/ios/


        #https://stackoverflow.com/questions/46717454/which-library-i-should-use-to-obtain-access-token



        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())

        self.service = discovery.build('drive', 'v3', http=http)
        #self.service = discovery.build('drive', 'v3', developerKey=self._API_KEY)
        return self.service

    def open_service(self, settings):
        self._settings(settings)

        if any([setting == '' for setting in settings]):
            raise ValueError('Incorrect Google Link Settings')
        else:
            return self._open_service()

    def add_file(self, filename, application='json'):
        file_metadata = {'name': filename,
                         'parents': ['appDataFolder']}
        file = os.path.join(self.LOCAL_STORAGE_PATH, filename)

        media = MediaFileUpload(file,
                                mimetype='application/' + application,
                                resumable=True)
        return self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()

    def delete_file(self, file_id):
        """Permanently delete a file, skipping the trash.

        Args:
          service: Drive API service instance.
          file_id: ID of the file to delete.
        """
        try:
            self.service.files().delete(fileId=file_id).execute()
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def server_folder_list(self):
        for file in self.get_folder_list():
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))

    def get_folder_list(self):
        response = self.service.files().list(spaces='appDataFolder',
                                             fields='nextPageToken, files(id, name)',
                                             pageSize=10).execute()
        return response.get('files', [])

    def update_file(self, file_id, new_filename):
        new_filename = self.LOCAL_STORAGE_PATH + new_filename
        try:
            # First retrieve the file from the API.
            file = self.service.files().get(fileId=file_id).execute()
            # File's new content.
            media_body = MediaFileUpload(
                    new_filename, resumable=True)

            # Send the request to the API.
            updated_file = self.service.files().update_panel_display(
                    fileId=file_id,
                    body=file,
                    media_body=media_body).execute()
            return updated_file
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return None


    def update_file(self, file_id, new_title, new_description, new_mime_type,
                    new_filename, new_revision):
        """Update an existing file's metadata and content.

        Args:
          service: Drive API service instance.
          file_id: ID of the file to update.
          new_title: New title for the file.
          new_description: New description for the file.
          new_mime_type: New MIME type for the file.
          new_filename: Filename of the new content to upload.
          new_revision: Whether or not to create a new revision for this file.
        Returns:
          Updated file metadata if successful, None otherwise.
        """
        try:
            # First retrieve the file from the API.
            file = self.service.files().get(fileId=file_id).execute()

            # File's new metadata.
            file['title'] = new_title
            file['description'] = new_description
            file['mimeType'] = new_mime_type

            # File's new content.
            media_body = MediaFileUpload(
                    new_filename, mimetype=new_mime_type, resumable=True)

            # Send the request to the API.
            updated_file = self.service.files().update_panel_display(
                    fileId=file_id,
                    body=file,
                    newRevision=new_revision,
                    media_body=media_body).execute()
            return updated_file
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return None

if __name__ == '__main__':
    gc = GoogleLink()
    set = {'LOCAL_STORAGE_PATH': '.local_storage/',
           'SCOPE': "https://www.googleapis.com/auth/drive.appdata",
           'APPLICATION_NAME': 'Task Manager',
           'API_KEY': 'AIzaSyDjQ_pg_ICdC_RenDu2DGmT54XtoYGXQSo'}
    gc.open_service(set)
    gc.server_folder_list()
