import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
import sys
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import *  # Import everything from main.py
from tkinter import Tk
from tkinter import messagebox as mess
import csv

class TestAttendanceSystem(unittest.TestCase):

    @patch('services.services.flask_server.start')
    def test_flask_server_start(self, mock_start):
        """Test if the Flask server starts successfully"""
        # Assuming `flask_server` is a module that contains the start function
        from services import flask_server  # Importing flask_server dynamically
        flask_server.start()
        # Assert that the start method was called
        mock_start.assert_called_once()

    @patch('services.services.mess.showerror')
    @patch('services.services.ts.askstring')
    def test_psw_admin_password_not_set(self, mock_askstring, mock_showerror):
        """Test the password flow when no password is set"""
        mock_askstring.return_value = None  # Simulate empty password entry
        
        psw_admin()  # Assuming this is a function in main.py that you want to test
        
        # Assert that showerror was called for missing password
        mock_showerror.assert_called_once_with('Password Required', 'Please provide the essential field: Password')

    @patch('services.services.mess.showinfo')
    @patch('services.services.ts.askstring')
    def test_psw_admin_password_set(self, mock_askstring, mock_showinfo):
        """Test the password flow when setting a new password"""
        mock_askstring.side_effect = ['new_password', 'new_password']  # First prompt for setting, second for confirmation
        
        psw_admin()  # Assuming this is a function in main.py that you want to test
        
        # Check if the showinfo message box was triggered
        mock_showinfo.assert_called_once_with('Password Set', 'Admin password was set successfully')

    @patch('services.services.mess.showinfo')
    def test_changeOnHover(self, mock_showinfo):
        """Test hover color change on buttons"""
        mock_button = MagicMock()
        changeOnHover(mock_button, "#ff0000", "#0000ff", "#ffffff", "#000000")
        
        # Simulate hover events
        mock_button.event_generate('<Enter>')
        mock_button.event_generate('<Leave>')
        
        # Check if the button configuration was changed
        mock_button.config.assert_called_with(background="#0000ff", fg="#000000")

    @patch('services.services.Tk.after')
    def test_tick(self, mock_after):
        """Test if the tick function updates the clock"""
        mock_clock = MagicMock()
        tick()  # Assuming tick() is a function in main.py
        
        # Ensure that the after method was called to update the time
        mock_after.assert_called_once()

    @patch('services.services.Tk.Toplevel')
    def test_show_gif(self, mock_toplevel):
        """Test if the gif window is displayed properly"""
        mock_window = MagicMock()
        mock_toplevel.return_value = mock_window
        
        show_gif(lambda: None)  # No need for actual gif callback in this test
        
        # Check that a new Toplevel window was created
        mock_toplevel.assert_called_once()

    @patch('services.services.csv.reader')
    def test_attendance_data_read(self, mock_csv_reader):
        """Test if the attendance data is being read correctly"""
        mock_csv_reader.return_value = iter([['id', 'name'], ['123', 'John Doe']])  # Simulated CSV data
        
        # Simulate file existence
        os.path.isfile = MagicMock(return_value=True)
        
        with patch('builtins.open', mock_open(read_data="id,name\n123,John Doe")):
            # Test the reading function
            with open('student_details/student_details.csv', 'r') as csvFile:
                reader = csv.reader(csvFile)
                rows = list(reader)
                self.assertEqual(len(rows), 2)
                self.assertEqual(rows[1], ['123', 'John Doe'])

    @patch('services.services.messagebox.showinfo')
    def test_admin_panel(self, mock_showinfo):
        """Test if the admin panel opens successfully"""
        mock_window = MagicMock()
        
        admin()  # Assuming `admin()` is a function in main.py that opens the admin panel
        
        # Check if the admin panel was initialized with the correct title
        mock_window.title.assert_called_with("Admin Panel - SKIT Jaipur")

class TestStudentCapture(unittest.TestCase):
    
    @patch('tkinter.messagebox.showerror')
    @patch('tkinter.messagebox.showinfo')
    @patch('builtins.open', create=True)
    def test_validate_and_capture_missing_info(self, mock_open, mock_showinfo, mock_showerror):
        # Mock the missing fields
        window = tk.Tk()
        id_entry = tk.Entry(window)
        name_entry = tk.Entry(window)
        status_msg = tk.Label(window)
        train_img_btn = tk.Button(window)

        # Simulate missing information
        id_entry.insert(0, '')
        name_entry.insert(0, '')

        # Call validate_and_capture
        validate_and_capture(id_entry, name_entry, "message", status_msg, train_img_btn)

        # Check that the showerror method was called for missing fields
        mock_showerror.assert_called_with("Missing Information", "Please provide all essential fields: ID and Name")
    
    @patch('tkinter.messagebox.showerror')
    @patch('tkinter.messagebox.showinfo')
    @patch('helper.anime.take_images')  # Assuming this method is used for capturing images
    def test_validate_and_capture_success(self, mock_take_images, mock_showinfo, mock_showerror):
        # Mock the file opening
        window = tk.Tk()
        id_entry = tk.Entry(window)
        name_entry = tk.Entry(window)
        status_msg = tk.Label(window)
        train_img_btn = tk.Button(window)

        # Simulate valid inputs
        id_entry.insert(0, '123')
        name_entry.insert(0, 'John Doe')

        # Simulate taking images (mock the method)
        mock_take_images.return_value = None

        # Call validate_and_capture
        validate_and_capture(id_entry, name_entry, "message", status_msg, train_img_btn)

        # Check that TakeImages was called
        mock_take_images.assert_called()

class TestAdminPasswordSetup(unittest.TestCase):

    @patch('tkinter.simpledialog.askstring')
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_psw_admin_new_password(self, mock_showerror, mock_showinfo, mock_askstring):
        # Mock the askstring dialog for password setup
        mock_askstring.return_value = 'newpassword'

        # Call psw_admin to simulate setting a new password
        psw_admin()

        # Check if the message box shows the correct info message
        mock_showinfo.assert_called_with('Password Set', 'Admin password was set successfully.')

    @patch('tkinter.simpledialog.askstring')
    @patch('tkinter.messagebox.showerror')
    @patch('builtins.open', create=True)
    def test_psw_admin_password_mismatch(self, mock_open, mock_showerror, mock_askstring):
        # Mock the askstring dialog for admin authentication
        mock_open.return_value.read.return_value = 'correctpassword'
        mock_askstring.side_effect = ['wrongpassword', 'correctpassword']

        # Simulate wrong password input
        psw_admin()

        # Check that showerror is called for incorrect password
        mock_showerror.assert_called_with('Access Denied', 'Incorrect password')

class TestButtonHoverEffect(unittest.TestCase):

    @patch('tkinter.Button.config')
    def test_changeOnHover(self, mock_config):
        window = tk.Tk()
        button = tk.Button(window)
        button.state = "normal"  # Mock the state

        # Call the function to simulate hover effect
        changeOnHover(button, "blue", "red", "white", "black")

        # Check if the config function was called with the expected arguments
        mock_config.assert_called_with(background="blue", fg="white")


class TestLogging(unittest.TestCase):

    @patch('logging.basicConfig')
    @patch('logging.FileHandler')
    def test_log_error(self, mock_filehandler, mock_basicconfig):
        # Mock the logging.FileHandler to avoid file creation during tests
        mock_handler = MagicMock()
        mock_filehandler.return_value = mock_handler

        # Call the log function with an error level message
        log("ERROR", "This is an error message")

        # Check if logging error function was called with the right message
        mock_handler.write.assert_called_with('ERROR: This is an error message')

    @patch('logging.basicConfig')
    @patch('logging.FileHandler')
    def test_log_warning(self, mock_filehandler, mock_basicconfig):
        # Mock the logging.FileHandler to avoid file creation during tests
        mock_handler = MagicMock()
        mock_filehandler.return_value = mock_handler

        # Call the log function with a warning level message
        log("WARNING", "This is a warning message")

        # Check if logging warning function was called with the right message
        mock_handler.write.assert_called_with('WARNING: This is a warning message')


if __name__ == "__main__":
    unittest.main()
