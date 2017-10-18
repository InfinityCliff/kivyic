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
    APP_DATA_FILE_ID = ''
    CONFIG_FILE_IDS = []
    CLIENT_SECRET_FILE = ''
    APPLICATION_NAME = ''
    LOCAL_STORAGE_PATH = ''
    # TODO set to user directory or a application path after testing
    #HOME_DIR = '' # os.path.expanduser('~')
    SCOPE = ''
    settings = {}
    service = None

    def __init__(self, scope, application_name, **kwargs):
        super(GoogleLink, self).__init__(**kwargs)
        #self.SCOPE = scope
        #self.APPLICATION_NAME = application_name
        #self.service = self.open_service()

    def get_credentials(self, scope):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        # Authorize server-to-server interactions from Google Compute Engine.

        credential_dir = os.path.join(self.LOCAL_STORAGE_PATH, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'drive-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, scope)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def _settings(self, settings):
        self.CLIENT_SECRET_FILE = settings.get('CLIENT_SECRET_FILE', '')
        self.LOCAL_STORAGE_PATH = settings.get('LOCAL_STORAGE_PATH', '')
        self.SCOPE = settings.get('SCOPE', '')
        self.APPLICATION_NAME = settings.get('APPLICATION_NAME', '')

    def open_service(self, settings):
        self._settings(settings)

        if any([setting == '' for setting in settings]):
            raise ValueError('Incorrect Google Link Settings')
        else:
            credentials = self.get_credentials(self.SCOPE)
            http = credentials.authorize(httplib2.Http())

            return discovery.build('drive', 'v3', http=http)

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

    def folder_list(self):
        for file in self.get_folder_list():
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))

    def get_folder_list(self):
        response = self.service.files().list(spaces='appDataFolder',
                                             fields='nextPageToken, files(id, name)',
                                             pageSize=10).execute()
        return response.get('files', [])

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
            updated_file = self.service.files().update(
                    fileId=file_id,
                    body=file,
                    newRevision=new_revision,
                    media_body=media_body).execute()
            return updated_file
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return None

if __name__ == '__main__':
    gc = GoogleLink('https://www.googleapis.com/auth/drive.appdata', 'Task Manager')
    gc.LOCAL_FILE_PATH = './'
    gc.folder_list()
