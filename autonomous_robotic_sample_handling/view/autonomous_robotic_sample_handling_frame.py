# Standard Imports
import tkinter as tk
from tkinter import ttk
import logging
from pathlib import Path

from autonomous_robotic_sample_handling.view.frames.multiposition_frame import MultiPositionTab, MultipositionButtons
from autonomous_robotic_sample_handling.view.frames.in_house_tools import InHouseTools
from navigate.view.custom_widgets.validation import ValidatedSpinbox, ValidatedCombobox

class AutonomousRoboticSampleHandlingFrame(ttk.Frame):
    """Plugin Frame: Just an example

    This frame contains the widgets for the plugin.
    """

    def __init__(self, root, *args, **kwargs):
        """Initialization of the  Frame

        Parameters
        ----------
        root : tkinter.ttk.Frame
            The frame that this frame will be placed in.
        *args
            Variable length argument list.
        **kwargs
            Arbitrary keyword arguments.
        """
        ttk.Frame.__init__(self, root, *args, **kwargs)

        # Formatting
        tk.Grid.columnconfigure(self, "all", weight=1)
        tk.Grid.rowconfigure(self, "all", weight=1)

        # Dictionary for widgets and buttons
        #: dict: Dictionary of the widgets in the frame
        self.inputs = {}
        self.buttons = {}
        self.variables = {}

        # #################################
        # ######## Example Widgets ########
        # ##### add your widgets here #####
        # #################################

        tk.Grid.columnconfigure(self, "all", weight=1)
        tk.Grid.rowconfigure(self, "all", weight=1)

        # Robot Initialization Buttons
        self.robot_init = RobotInitialization(self)
        self.robot_init.grid(
            row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10
        )
        self.buttons.update(RobotInitialization.get_buttons(self.robot_init))

        # Quick Command Buttons
        self.move_sequence = MoveSequence(self)
        self.move_sequence.grid(
            row=5, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10
        )
        self.buttons.update(MoveSequence.get_buttons(self.move_sequence))

        # Pause and Play Buttons
        self.pause_play = PausePlay(self)
        self.pause_play.grid(
            row=0, column=3, columnspan=2, sticky=tk.NSEW, padx=10, pady=10
        )
        self.buttons.update(PausePlay.get_buttons(self.pause_play))

        self.multiposition = MultiPositionTab(self)
        self.multiposition.grid(
            row=15, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10
        )
        # multiposition table Buttons
        self.MultipositionButtons = MultipositionButtons(self)
        self.MultipositionButtons.grid(
            row=10, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10
        )

        # In-House Tools
        self.InHouseTools = InHouseTools(self)
        self.InHouseTools.grid(
            row=7, column=0, columnspan=2, sticky=tk.NSEW, padx=10, pady=10
        )
        self.buttons.update(InHouseTools.get_buttons(self.InHouseTools))

    # Getters
    def get_variables(self):
        """Returns a dictionary of the variables for the widgets in this frame.

        The key is the widget name, value is the variable associated.

        Returns
        -------
        variables : dict
            Dictionary of the variables for the widgets in this frame.
        """
        return self.variables

    def get_widgets(self):
        """Returns a dictionary of the widgets in this frame.

        The key is the widget name, value is the LabelInput class that has all the data.

        Returns
        -------
        self.inputs : dict
            Dictionary of the widgets in this frame.
        """
        return self.inputs

class RobotInitialization(tk.Frame):
    """RobotInitialization

    RobotInitialization is a frame that contains the widgets for initializing
    robot movement.

    Parameters
    ----------
    settings_tab : tk.Frame
        The frame that contains the settings tab.
    *args : tuple
        Variable length argument list.
    **kwargs : dict
        Arbitrary keyword arguments.

    Attributes
    ----------
    buttons : dict
        A dictionary of all the buttons that are tied to each widget name.
        The key is the widget name, value is the button associated.

    Methods
    -------
    """
    def __init__(self, settings_tab, *args, **kwargs):
        text_label = 'Robot Initialization'
        ttk.Labelframe.__init__(self, settings_tab, text=text_label, *args, **kwargs)

        # Formatting
        tk.Grid.columnconfigure(self, "all", weight=1)
        tk.Grid.rowconfigure(self, "all", weight=1)

        # Initializing Button
        self.buttons = {
            "import": ttk.Button(self, text="Load Positions from Disk"),
            "connect": ttk.Button(self, text="Connect Robot"),
            "disconnect": ttk.Button(self, text="Disconnect Robot"),
            "move": ttk.Button(self,text='Move Robot'),
            "zero": ttk.Button(self, text="Zero Joints"),
            "opengripper": ttk.Button(self, text="Open Gripper"),
            "closegripper": ttk.Button(self,text="Close Gripper"),
            "movetoloadingzone": ttk.Button(self,text="Move Stage to Initial Loading Zone")
        }
        counter = 0
        for key, button in self.buttons.items():
            if counter == 0:
                row, column = 0, 0
            elif counter == 1:
                row, column = 0, 1
            elif counter == 2:
                row, column = 0, 2
                row, column = 1, 0
            elif counter == 3:
                row, column = 1,1
            elif counter == 4:
                row, column = 2, 0
            elif counter == 5:
                row, column = 2, 1
            elif counter == 6:
                row, column = 3, 0
            elif counter == 7:
                row, column = 3, 1

            button.grid(
                row=row, column=column, sticky=tk.NSEW, padx=(4, 1), pady=(4, 6)
            )
            counter += 1

    def get_buttons(self):
        return self.buttons

class MoveSequence(tk.Frame):
    """MoveSequence

    MoveSequence is a frame that contains the widgets for initializing
    robot movement.

    Parameters
    ----------
    settings_tab : tk.Frame
        The frame that contains the settings tab.
    *args : tuple
        Variable length argument list.
    **kwargs : dict
        Arbitrary keyword arguments.

    Attributes
    ----------
    buttons : dict
        A dictionary of all the buttons that are tied to each widget name.
        The key is the widget name, value is the button associated.

    Methods
    -------
    """
    def __init__(self, settings_tab, *args, **kwargs):
        text_label = 'Move Sequence'
        ttk.Labelframe.__init__(self, settings_tab, text=text_label, *args, **kwargs)

        # Formatting
        tk.Grid.columnconfigure(self, "all", weight=1)
        tk.Grid.rowconfigure(self, "all", weight=1)

        # Initializing Button
        self.buttons = {
            "stop": ttk.Button(self, text="STOP"),
            "sample_carousel": ttk.Button(self, text="Sample to carousel"),
            "sample_microscope": ttk.Button(self, text="Sample to microscope"),
        }
        counter = 0
        for key, button in self.buttons.items():
            if counter == 0:
                row, column = 0, 0
            elif counter == 1:
                row, column = 0, 1
            elif counter == 2:
                row, column = 0, 2

            button.grid(
                row=row, column=column, sticky=tk.NSEW, padx=(4, 1), pady=(4, 6)
            )
            counter += 1

    def get_buttons(self):
        return self.buttons

class PausePlay(tk.Frame):
    """PausePlay

    PausePlay is a frame that contains the widgets for pausing and resuming
    robot actions.

    Parameters
    ----------
    settings_tab : tk.Frame
        The frame that contains the settings tab.
    *args : tuple
        Variable length argument list.
    **kwargs : dict
        Arbitrary keyword arguments.

    Attributes
    ----------
    buttons : dict
        A dictionary of all the buttons that are tied to each widget name.
        The key is the widget name, value is the button associated.

    Methods
    -------
    """
    def __init__(self, settings_tab, *args, **kwargs):
        ttk.Labelframe.__init__(self, settings_tab, *args, **kwargs)

        # Formatting
        tk.Grid.columnconfigure(self, "all", weight=1)
        tk.Grid.rowconfigure(self, "all", weight=1)

        #Path to pause and play buttons
        image_directory = Path(__file__).resolve().parent
        self.pause_image = tk.PhotoImage(
            file=image_directory.joinpath("images", "pause.png")
        ).subsample(32,32)
        self.play_image = tk.PhotoImage(
            file=image_directory.joinpath("images", "play.png")
        ).subsample(32,32)

        self.buttons = {
            "pause": tk.Button(self, image=self.pause_image, borderwidth=0),
            "play": tk.Button(self, image=self.play_image, borderwidth=0),
        }

        # Gridding out Buttons
        self.buttons['play'].grid(
            row=0, column=0, rowspan=1, columnspan=1, padx=2, pady=2
        )
        self.buttons['pause'].grid(
            row=0, column=2, rowspan=1, columnspan=1, padx=2, pady=2
        )

    def get_buttons(self):
        return self.buttons


