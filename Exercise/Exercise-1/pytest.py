import unittest
from unittest.mock import patch, MagicMock, mock_open, call ,AsyncMock
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from aiohttp import ClientSession
from asyncioCode_ThreadExecutor import creating_folder, extract_and_remove_zip, downloading_files, main , urls, save_path # Update with the correct import

class TestDownloadScript(unittest.IsolatedAsyncioTestCase):

    save_path = 'C:\\Users\\Vasanth\\Downloads\\pythonDownload\\combined'
    @patch("os.path.exists", return_value=False)
    @patch("os.makedirs")
    @patch("builtins.print")
    def test_creating_folder_creates_directory(self, mock_print, mock_makedirs, mock_exists):
        creating_folder()
        mock_makedirs.assert_called_once_with(save_path)
        mock_print.assert_called_once_with(f"The new directory {save_path} is created!")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.print")
    def test_creating_folder_already_exists(self, mock_print, mock_exists):
        creating_folder()
        mock_print.assert_called_once_with(f"The directory {save_path} already exists")

    @patch("zipfile.ZipFile.extractall")
    @patch("os.remove")
    @patch("zipfile.ZipFile.__enter__")
    @patch("zipfile.ZipFile.__exit__")
    @patch("builtins.print")
    def test_extract_and_remove_zip_success(self, mock_print, mock_exit, mock_enter, mock_remove, mock_extractall):
        # mock_zipfile = MagicMock()
        # mock_enter.return_value = mock_zipfile
        
        # Call the function under test
        extract_and_remove_zip("C:\\Users\\Vasanth\\Downloads\\pythonDownload\\combined\\unitTestZipFiles\\Divvy_Trips_2019_Q3.zip")
        
        # Assert that the extraction was called correctly
        mock_extractall.assert_called_once_with(path="C:\\Users\\Vasanth\\Downloads\\pythonDownload\\combined")
        
        # Assert that os.remove was called with the correct file path
        mock_remove.assert_called_once_with("C:\\Users\\Vasanth\\Downloads\\pythonDownload\\combined\\unitTestZipFiles\\Divvy_Trips_2019_Q3.zip")
        
        # Assert that the correct print message was printed
        mock_print.assert_called_once_with("Extracted and removed C:\\Users\\Vasanth\\Downloads\\pythonDownload\\combined\\unitTestZipFiles\\Divvy_Trips_2019_Q3.zip")

    @patch("builtins.print")
    def test_extract_and_remove_zip_failure(self, mock_print):
        with patch("zipfile.ZipFile", side_effect=Exception("Test Error")):
            extract_and_remove_zip("Divvy_Trips_2018_Q4.zip")
            mock_print.assert_called_once_with("Error extracting or removing Divvy_Trips_2018_Q4.zip: [Errno 2] No such file or directory: 'Divvy_Trips_2018_Q4.zip'")

    @patch("builtins.open", new_callable=mock_open)
    @patch("aiohttp.ClientSession.get")
    @patch("builtins.print")
    async def test_downloading_files_success(self, mock_print, mock_get, mock_open):
        # Mock response for aiohttp
        mock_response = MagicMock()
        mock_response.status = 200
        # Set up read method as an asynchronous method using AsyncMock
        mock_response.read = AsyncMock(return_value=b"file content")
        mock_get.return_value.__aenter__.return_value = mock_response

        # Use ThreadPoolExecutor in the test to match the function's implementation
        executor = ThreadPoolExecutor(max_workers=1)
        async with ClientSession() as session:
            await downloading_files(session, "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip", executor)

        # Verify that the file was opened in write-binary mode
        mock_open.assert_called_with(os.path.join(save_path, "Divvy_Trips_2018_Q4.zip"), 'rb')

        # Check print outputs for correct download and write operations
        mock_print.assert_any_call("Downloading https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip")
        mock_print.assert_any_call(os.path.join(save_path, "Divvy_Trips_2018_Q4.zip"), "was written")

    @patch("builtins.print")
    @patch("aiohttp.ClientSession.get")
    async def test_downloading_files_failure(self, mock_get, mock_print):
        mock_response = MagicMock()
        mock_response.status = 404
        mock_get.return_value.__aenter__.return_value = mock_response

        executor = ThreadPoolExecutor(max_workers=1)
        async with ClientSession() as session:
            await downloading_files(session, "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip", executor)

        mock_print.assert_called_with("Invalid URL: https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip, skipping to next file")

    @patch("asyncioCode_ThreadExecutor.downloading_files")  # Replace `your_module` with the actual module name
    @patch("asyncioCode_ThreadExecutor.creating_folder")
    async def test_main(self, mock_creating_folder, mock_downloading_files):
        mock_downloading_files.return_value = asyncio.Future()
        mock_downloading_files.return_value.set_result(None)

        await main()

        mock_creating_folder.assert_called_once()
        self.assertEqual(mock_downloading_files.call_count, len(urls))

if __name__ == '__main__':
    unittest.main()
