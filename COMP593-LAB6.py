import requests
import hashlib
import subprocess
import os

FILE_URL = "https://get.videolan.org/vlc/3.0.18/win64/vlc-3.0.18-win64.exe"
HASH_URL = "http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe.sha256"
installer_path = 'C:\\temp\\vlc-3.0.18-win64.exe'

def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):
        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():

# Send GET message to download the file
    resp_msg = requests.get(FILE_URL)

# Check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:

# Extract binary file content from response message body
        file_content = resp_msg.content

# Calculate SHA-256 hash value
        image_hash = hashlib.sha256(file_content).hexdigest()
    return image_hash

def download_installer():

# Send GET message to download the file
    resp_msg = requests.get(FILE_URL)

# Check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:

        # Extract and return the binary file content from response message
        return resp_msg.content

def installer_ok(installer_data, expected_sha256):

    installer_data = get_expected_sha256()

# Send GET message to download the file
    resp_msg = requests.get(HASH_URL)

# Check whether the download was successful
    if resp_msg.status_code == requests.codes.ok:
        
# Extract text hash from the file content from response message
        expected_sha256 = resp_msg.text.split()[0]

        # Determine whether the hash files match
        if expected_sha256 == installer_data:
            return True
        else: 
            return False

def save_installer(installer_data):

    installer_data = download_installer()

    with open(r'C:\temp\vlc-3.0.18-win64.exe', 'wb') as file:
        file.write(installer_data)

    return

def run_installer(installer_path):

    subprocess.run([installer_path, '/L=1033', '/S'])

    return
    
def delete_installer(installer_path):

    os.remove(installer_path)

    return

if __name__ == '__main__':
    main()