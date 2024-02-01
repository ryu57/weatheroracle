import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import *
from actmng import AccountManager
import forecast


class MainUI(QtWidgets.QMainWindow):
    """
    Holds all ui sections
    """

    def __init__(self):
        """
        Initializes all nested UI elements
        """
        super().__init__()

        # Set window size and title
        self.setWindowTitle('Weather Oracle')
        self.setGeometry(300, 300, 300, 600)
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.setup_ui()

    def setup_ui(self):
        # Set layout
        self.layout = QtWidgets.QVBoxLayout()
        self.setStyleSheet("background-color: lightblue;")

        # Initialize the 2 main UI elements
        self.forecast_ui = ForecastUI()
        self.location_select_ui = LocationSelectUI(self.forecast_ui)

        # Add widgets to layout
        self.layout.addWidget(self.location_select_ui)
        self.layout.addWidget(self.forecast_ui)

        self.central_widget.setLayout(self.layout)

    def run(self):
        """
        Start the MainWindow
        """
        self.show()
        return QtWidgets.QApplication.instance().exec_()


class ForecastUI(QtWidgets.QWidget):
    """
    Holds forecast widgets
    """
    def __init__(self):
        super().__init__()
        self.forecast = forecast.Forecast()

        self.setup_ui()
    def setup_ui(self):
        """
        Create the UI elements holding information for each day
        :return:
        """
        self.layout = QtWidgets.QHBoxLayout()

        # Create an instance of DayUI for each day
        self.day_list = []
        for i in range(7):
            current = DayUI()
            self.layout.addWidget(current)
            self.day_list.append(current)

        # Set layout
        self.setLayout(self.layout)

        # Update the displayed information
        self.update_forecast_ui()


    def update_forecast_ui(self, location="Toronto"):
        """
        Update the on-screen forecast with the new specified location
        :param location: a location string, e.g. Toronto, Ottawa, Montreal, etc.
        """
        self.forecast.update_data(location=location)
        dates, temp = self.forecast.get_days_and_temp()
        for i in range(7):
            self.day_list[i].set_label_top(str(dates[i]))
            self.day_list[i].set_label_bottom(str(temp[i]))

class DayUI(QtWidgets.QWidget):
    """
    Individual Forecast Widget
    """
    def __init__(self):
        super().__init__()

        self.setFixedSize(250, 600)
        self.day_layout = QtWidgets.QVBoxLayout()

        # Set Font
        self.font = QtGui.QFont("Calibri", 30)

        # Creating labels
        self.label_top = QtWidgets.QLabel("Default Top Text")
        self.label_bottom = QtWidgets.QLabel("Default Bottom Text")

        # Adding labels to the layout
        self.day_layout.addWidget(self.label_top)
        self.day_layout.addWidget(self.label_bottom)

        # Set text formating
        self.label_top.setAlignment(QtCore.Qt.AlignCenter)
        self.label_bottom.setAlignment(QtCore.Qt.AlignCenter)
        self.label_top.setFont(self.font)
        self.label_bottom.setFont(self.font)

        # Setting the layout for the widget
        self.setLayout(self.day_layout)
        self.day_layout.setSpacing(0)

        # Setting the background color for the entire widget
        self.setStyleSheet("background-color: white;")
        self.opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self.opacity_effect.setOpacity(0.5)
        self.setGraphicsEffect((self.opacity_effect))

    def set_label_top(self, text):
        """
        Sets the text of the date label
        :param text: String that should indicate the date
        """
        self.label_top.setText(text)

    def set_label_bottom(self, text):
        """
        Sets the text of the temperature label
        :param text: String that should indicate temperature
        """
        self.label_bottom.setText(text)

class LocationSelectUI(QtWidgets.QWidget):
    """
    Holds all UI related to selecting profile and location
    """
    def __init__(self, forecast_ui):
        super().__init__()

        self.forecast_ui = forecast_ui
        self.account_mng = AccountManager()
        self.init_ui()
    def init_ui(self):
        # Set font
        self.font = QtGui.QFont("Calibri", 16)

        # Label presenting profile select combobox
        self.profile_label = QtWidgets.QLabel("Current Profile: ")
        self.profile_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.profile_label.setFont(self.font)

        # Profile select combobox
        self.profile_dropdown = self.init_profile_combo_box()
        self.profile_dropdown.setStyleSheet("background-color: white;")
        self.profile_dropdown.setFont(self.font)

        # Button that initiates profile management ui
        self.manage_profile_button = QtWidgets.QPushButton("Manage Profiles")
        self.manage_profile_button.setFont(self.font)
        self.manage_profile_button.setStyleSheet("background-color: white;")
        self.manage_profile_button.clicked.connect(self.on_profile_manage_button_click)

        # Widget spacer
        self.spacer = QSpacerItem(100,5)

        # Button for applying changes to location combobox
        self.button = QtWidgets.QPushButton('Apply and Refresh Location Data', self)
        self.button.setStyleSheet("background-color: white;")
        self.button.clicked.connect(self.on_button_click)
        self.button.setFont(self.font)

        # Location select combobox
        self.dropdown_selector = self.init_location_combo_box()
        self.dropdown_selector.setStyleSheet("background-color: white;")
        self.dropdown_selector.setFont(self.font)

        # Label presenting location select combobox
        self.dropdown_label = QtWidgets.QLabel("Change Location:", self)
        self.dropdown_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.dropdown_label.setFont(self.font)

        # Label displaying currently selected location
        self.current_label = QtWidgets.QLabel("Current Location: " + self.selected_location, self)
        self.current_label.setStyleSheet("border: 5px solid blue; padding: 5px;")
        self.current_label.setAlignment( QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.current_label.setFont(self.font)

        # Set layout and add widgets
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.profile_label)
        layout.addWidget(self.profile_dropdown)
        layout.addWidget(self.manage_profile_button)
        layout.addItem(self.spacer)
        layout.addWidget(self.current_label)
        layout.addWidget(self.dropdown_label)
        layout.addWidget(self.dropdown_selector)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def init_profile_combo_box(self):
        """
        Initialize the profile select combo box
        :return: Initialized combo box
        """
        # Create and add profiles to combobox list
        dropdown_selector = QtWidgets.QComboBox(self)
        for profile in self.account_mng.get_profiles():
            dropdown_selector.addItem(profile)

        # Set the current combobox selection to the last selected option from
        # the last session
        self.selected_profile = self.account_mng.get_current_profile()
        dropdown_selector.setCurrentText(self.selected_profile)

        # Connect the signal function when selection is changed
        dropdown_selector.currentIndexChanged.connect(self.on_profile_dropdown_change)

        return dropdown_selector

    def init_location_combo_box(self):
        """
        Initialize the location select combo box
        :return: Initialized combobox
        """
        # Create and add items to combobox
        dropdown_selector = QtWidgets.QComboBox(self)
        dropdown_selector.addItem("Toronto")
        dropdown_selector.addItem("Ottawa")
        dropdown_selector.addItem("Quebec")
        dropdown_selector.addItem("Montreal")
        dropdown_selector.addItem("Vancouver")
        dropdown_selector.addItem("Calgary")
        dropdown_selector.addItem("Edmonton")
        dropdown_selector.addItem("Regina")
        dropdown_selector.addItem("Winnipeg")

        # Set the current location to the last selected location
        self.selected_location = self.account_mng.accounts["accounts"][self.selected_profile].location

        # Update the displayed forecast
        self.forecast_ui.update_forecast_ui(self.selected_location)
        dropdown_selector.setCurrentText(self.selected_location)

        # Connect selection change signal to response function
        dropdown_selector.currentIndexChanged.connect(self.on_location_dropdown_change)

        return dropdown_selector


    def on_profile_manage_button_click(self):
        """
        Launch the profile manager UI
        """
        # Create UI object and pass self
        profile_manage_ui = ProfileManagerUI(self.selected_location, self.account_mng, self)
        profile_manage_ui.location_select_ui = self

        # Set modality of the sub-UI and display it
        profile_manage_ui.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        profile_manage_ui.show()


    def on_button_click(self):
        """
        Update the displayed forecast when the location change button is pressed.
        """
        self.forecast_ui.update_forecast_ui(location=self.selected_location)
        self.current_label.setText("Current Location: " + self.selected_location)
        self.account_mng.write_to_file()


    def on_location_dropdown_change(self):
        """
        Change the saved location of the current profile to the selected profile
        """
        self.selected_location = self.dropdown_selector.currentText()
        self.account_mng.accounts["accounts"][self.selected_profile].change_location(self.selected_location)

    def on_profile_dropdown_change(self):
        """
        Update the UI to the preferences of the selected profile
        """
        # Changed the saved last profile to currently selected profile
        self.account_mng.set_current_profile(self.profile_dropdown.currentText())
        self.selected_profile = self.profile_dropdown.currentText()

        # Get the location preference of the currently selected profile
        self.selected_location = self.account_mng.accounts["accounts"][self.selected_profile].location

        # Update the UI to match the profile
        self.forecast_ui.update_forecast_ui(location=self.selected_location)
        self.current_label.setText(
            "Current Location: " + self.selected_location)
        self.dropdown_selector.setCurrentText(self.selected_location)
        self.account_mng.write_to_file()

class ProfileManagerUI(QDialog):
    """
    UI that handles creating and deleting users
    """
    def __init__(self, location, account_mng, parent=None):
        """
        Initialize UI object
        :param location: The currently selected location
        :param account_mng: AccountManager object of parent
        :param parent: The parent UI, should be LocationSelectUI
        """
        super().__init__(parent)

        self.initUI()
        self.parent = parent
        self.account_mng = account_mng
        self.selected_location = location
        self.location_select_ui = None

    def initUI(self):
        layout = QtWidgets.QHBoxLayout()

        # Set font
        self.font = QtGui.QFont("Calibri", 16)

        # Button that launches add profile UI
        self.add_profile_button = QtWidgets.QPushButton("Create a Profile")
        self.add_profile_button.setStyleSheet("background-color: white;")
        self.add_profile_button.setFont(self.font)
        self.add_profile_button.clicked.connect(
            self.on_profile_add_button_click)

        # Button that launches delete profile UI
        self.delete_profile_button = QtWidgets.QPushButton("Delete a Profile")
        self.delete_profile_button.setStyleSheet("background-color: white;")
        self.delete_profile_button.setFont(self.font)
        self.delete_profile_button.clicked.connect(
            self.on_profile_delete_button_click)

        # Add buttons to layout
        layout.addWidget(self.add_profile_button)
        layout.addWidget(self.delete_profile_button)

        self.setLayout(layout)
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowTitle('Profile Manager')

    def on_profile_add_button_click(self):
        """
        Launch add user UI after clicking the respective button.
        """
        inputDialog = InputDialog(self)
        inputDialog.account_mng = self.account_mng
        inputDialog.textEntered.connect(self.handleTextEntered)

        # Show the dialog
        inputDialog.exec_()

    def on_profile_delete_button_click(self):
        """
        Launch add user UI after clicking the respective button.
        """
        inputDialog = DeleteDialog(self.account_mng, self)
        inputDialog.textEntered.connect(self.handleDelete)

        # Show the dialog
        inputDialog.exec_()

    def handleTextEntered(self, text):
        """
        Function that adds a profile with the passed string as the profile name
        :param text: The name of the new profile
        """
        # Add a new account object to the AccountManager
        self.account_mng.add_account(text, self.selected_location)
        self.account_mng.set_current_profile(text)

        # Access the LocationSelectUI instance and update the profile combo box
        self.location_select_ui.profile_dropdown.addItem(text)
        self.location_select_ui.selected_profile = self.account_mng.get_current_profile()

        # Save changes
        self.account_mng.write_to_file()


    def handleDelete(self, text):
        """
        Function that deletes a profile with the passed string as the profile name
        :param text: The name of the profile being deleted
        """
        # Delete the profile from AccountManager
        success = self.account_mng.remove_account(text)

        # Check if delete was successful, then update the profile select combobox
        if success:
            for i in range(self.location_select_ui.profile_dropdown.count()):
                if text == self.location_select_ui.profile_dropdown.itemText(i):
                    self.location_select_ui.profile_dropdown.removeItem(i)
                    break

        # Update the displayed forecast based on the remaining profiles
        self.location_select_ui.selected_profile = self.account_mng.get_current_profile()
        self.location_select_ui.profile_dropdown.setCurrentText(
            self.account_mng.get_current_profile())
        self.selected_location = self.account_mng.accounts["accounts"][self.location_select_ui.selected_profile]

        # Save changes
        self.account_mng.write_to_file()




class InputDialog(QDialog):
    """
    UI for adding a user
    """
    textEntered = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.account_mng = None
        self.initUI()

    def initUI(self):
        # Initialize layout
        layout = QVBoxLayout()

        # Set font
        self.font = QtGui.QFont("Calibri", 16)

        # Text input widget
        self.inputLineEdit = QLineEdit(self)
        self.inputLineEdit.setStyleSheet("background-color: white;")
        self.inputLineEdit.setFont(self.font)
        layout.addWidget(self.inputLineEdit)

        # Input completed button
        self.okButton = QPushButton("OK", self)
        self.okButton.clicked.connect(self.emitTextEntered)
        self.okButton.setStyleSheet("background-color: white;")
        self.okButton.setFont(self.font)
        layout.addWidget(self.okButton)

        # Finalize window
        self.setLayout(layout)
        self.setWindowTitle('Create Profile')
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

    def emitTextEntered(self):
        """
        Send text signal of the input
        """
        # Check if profile already exists, display a popup if it does
        if self.inputLineEdit.text() in self.account_mng.accounts["accounts"]:
            popup = PopupUI("Profile ID already exists")
            popup.exec_()
        else:
            self.textEntered.emit(self.inputLineEdit.text())
            self.accept()

class DeleteDialog(QDialog):
    """
    UI for deleting profiles
    """
    textEntered = QtCore.pyqtSignal(str)
    def __init__(self, account_mng=None, parent=None):
        super().__init__(parent)
        self.account_mng = account_mng
        self.initUI()

    def initUI(self):
        # Set layout
        layout = QVBoxLayout()

        # Set font
        self.font = QtGui.QFont("Calibri", 16)

        # Profile list combobox
        self.dropdown = self.init_profile_combo_box()
        self.dropdown.setStyleSheet("background-color: white;")
        self.dropdown.setFont(self.font)

        # Delete selected profile button
        self.okButton = QPushButton("Delete Profile", self)
        self.okButton.setStyleSheet("background-color: white;")
        self.okButton.setFont(self.font)
        self.okButton.clicked.connect(self.emitTextEntered)

        # Add widgets to layout
        layout.addWidget(self.dropdown)
        layout.addWidget(self.okButton)

        # Finalize window
        self.setLayout(layout)
        self.setWindowTitle('Delete Profile')
        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

    def init_profile_combo_box(self):
        """
        Function for initializing the profile select combobox
        :return: Initialized combobox
        """
        dropdown_selector = QtWidgets.QComboBox(self)
        # Add the profiles listed by AccountManager
        for profile in self.account_mng.get_profiles():
            dropdown_selector.addItem(profile)
        return dropdown_selector

    def emitTextEntered(self):
        """
        Emit text signal for selected profile
        :return:
        """
        # Check if the selected profile isn't default, if it is, display a popup
        if self.dropdown.currentText() != "default":
            self.textEntered.emit(self.dropdown.currentText())
            # Close the dialog
            self.accept()
        else:
            popup = PopupUI("Cannot delete default profile.")
            popup.exec_()



class PopupUI(QMessageBox):
    """
    General Popup UI
    """
    def __init__(self, text):
        super().__init__()

        # Set font
        self.font = QtGui.QFont("Calibri", 16)

        # Set the window title and text
        self.setWindowTitle("Warning")
        self.setText(text)
        self.setFont(self.font)

        # Popup Button
        self.addButton(QMessageBox.Ok)

        # Set Icon
        self.setIcon(QMessageBox.Information)













