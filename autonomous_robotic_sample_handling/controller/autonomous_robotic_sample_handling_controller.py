
# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports
from navigate.tools.file_functions import load_yaml_file
from navigate.config.config import get_navigate_path
from autonomous_robotic_sample_handling.controller.sub_controllers.robot_arm_controller import (
    RobotArmController
)
from autonomous_robotic_sample_handling.controller.sub_controllers.multiposition_controller import (
    MultipositionController
)
from autonomous_robotic_sample_handling.controller.sub_controllers.motor_controller import (
    MotorController
)
from autonomous_robotic_sample_handling.controller.sub_controllers.automation_controller import (
    AutomationController
)
from autonomous_robotic_sample_handling.controller.sub_controllers.inhouse_tools_controller import (
    InHouseToolsPopupController
)
from autonomous_robotic_sample_handling.view.popups.inhouse_tools_popup import InHouseToolsPopup


class AutonomousRoboticSampleHandlingController:
    """AutonomousRoboticSampleHandlingController"""
    def __init__(self, view, parent_controller=None):
        """
        Initialize the AutonomousRoboticSampleHandlingController

        Parameters
        ----------
        view : object
            The view object
        parent_controller : object
            The parent controller object
        """
        #: object: The view object
        self.view = view

        #: object: The parent controller object
        self.parent_controller = parent_controller

        #: dict: The variables from the view
        self.variables = self.view.get_variables()

        #: dict: The buttons from the view
        self.buttons = self.view.buttons

        # Configure traces
        self.buttons['automation_sequence'].configure(
            command=self.automated_sample_handling)
        self.buttons['process_sample'].configure(
            command=self.sample_iteration)
        self.buttons['offline_program'].configure(
            command=self.start_offline_program)
        self.buttons['in_house'].configure(
            command=self.launch_inhouse_tools)

        #: dict: The data from the configuration file
        self.data = self.load_config_data()
        self.prepare_config_data(self.data)

        # Initialize sub-controllers
        #: RobotArmController: The robot arm controller
        self.robot_arm_controller = RobotArmController(
            self.view, self.parent_controller
        )

        #: MultipositionController: The multiposition controller
        self.multiposition_controller = MultipositionController(
            self.view, self.parent_controller
        )

        #: MotorController: The motor controller
        self.motor_controller = MotorController(
            self.view, self.parent_controller
        )

        #: AutomationController: The automation controller
        self.automation_controller = AutomationController(
            self.view.move_sequence, self.parent_controller
        )

        #: InHouseToolsPopupController: The in house tools popup controller
        self.inhouse_tools_popup_controller = None

        #: dict: The key positions
        self.key_positions = None

    def launch_inhouse_tools(self):
        """Launches inhouse tools popup.

        Will only launch when button in GUI is pressed, and will not duplicate.
        Pressing button again brings popup to the front.
        """

        if hasattr(self, "inhouse_tools_popup_controller"):
            self.inhouse_tools_popup_controller.showup()
            return
        inhouse_tools = InHouseToolsPopup(self.view)
        self.inhouse_tools_popup_controller = InHouseToolsPopupController(inhouse_tools, self)

    def load_config_data(self):
        """ Load the configuration data

        Returns
        -------

        """
        plugins_config_path = os.path.join(
            get_navigate_path(), "config", "plugins_config.yml"
        )
        plugins_config = load_yaml_file(plugins_config_path)
        plugin_path = plugins_config["Autonomous Robotic Sample Handling"]
        local_config_path = os.path.join(plugin_path, "config", "configuration.yaml")
        data = load_yaml_file(local_config_path)
        return data

    def start_offline_program(self, program_name="Vertical_Oscillation"):
        """ Start the offline program

        Parameters
        ----------
        program_name: str
            The name of the program to start
        """
        self.parent_controller.execute(
            "start_program", program_name
        )

    def get_microscope_position(self, data):
        """ Get the microscope position

        Parameters
        ----------
        data : dict
            The data from the configuration

        Returns
        -------
        list
            The list of the positions
        """
        x = data["environment"]["microscope"]["x"]
        y = data["environment"]["microscope"]["y"]
        z = data["environment"]["microscope"]["z"]
        theta_x = data["environment"]["microscope"]["R1"]
        theta_y = data["environment"]["microscope"]["R2"]
        theta_z = data["environment"]["microscope"]["R3"]
        return [x, y, z, theta_x, theta_y, theta_z]

    def get_loading_zone_position(self, data):
        """ Get the loading zone position

        Parameters
        ----------
        data : dict
            The data from the configuration

        Returns
        -------
        list
            The list of the positions
        """
        x = data["environment"]["loading_zone"]["pose"]["x"]
        y = data["environment"]["loading_zone"]["pose"]["y"]
        z = data["environment"]["loading_zone"]["pose"]["z"]
        theta_x = data["environment"]["loading_zone"]["pose"]["Rx"]
        theta_y = data["environment"]["loading_zone"]["pose"]["Ry"]
        theta_z = data["environment"]["loading_zone"]["pose"]["Rz"]
        flag = data["environment"]["loading_zone"]["flag"]
        return [x, y, z, theta_x, theta_y, theta_z] if flag else None

    def prepare_config_data(self, data):
        """ Prepare the configuration data

        Parameters
        ----------
        data : dict
            The data from the configuration file.
        """
        motor_position = data["environment"]["motor"]["units"]
        motor_to_robot_mm = motor_position * 25.4
        # for standard TRF, z is forwards, x is down
        data_points = {
            "robot_base": data["environment"]["robot"]["robot_base_plate_height"],
            "vial_height": data["environment"]["components"]["vial_height_from_carousel"],
            "carousel_height": data["environment"]["components"]["carousel_height_from_table"],
            "vial_attack": data["environment"]["components"]["vial_attack_distance_from_carousel"],
            "wrf_to_trf": data["environment"]["components"]["trf_from_wrf_cartesian"],
            "trf_gripper_edge": data["environment"]["components"]["trf_to_gripper_edge"],
            "trf_gripper_bottom": data["environment"]["components"]["trf_to_gripper_bottom"],
            "MEPG_thickness": data["environment"]["components"]["MEPG_thickness"],
            "sample_height": data["environment"]['components']['sample_height'],
            "shear_distance": data["environment"]['components']['shear_distance'],
            "tolerance_up": data["environment"]["components"]["tolerance_up"],
            "tolerance_forward": data["environment"]["components"]["tolerance_forward"],
        }
        motor_position_x = data_points["robot_base"] + data_points[
            "wrf_to_trf"][2] - data_points["carousel_height"] - data_points[
            "vial_height"] - data_points['trf_gripper_bottom'] + data_points[
            'tolerance_up']

        motor_position_z = motor_to_robot_mm - data_points["vial_attack"] - data_points["wrf_to_trf"][0] - data_points[
            'tolerance_forward'] - data_points["MEPG_thickness"]

        loading_zone_x = motor_to_robot_mm - data_points['vial_attack'] - data_points['tolerance_forward'] - \
                         data_points['MEPG_thickness']

        loading_zone_z = data_points['carousel_height'] + data_points['vial_height'] + data_points[
            'trf_gripper_bottom'] - data_points['robot_base'] + data_points["tolerance_up"]

        self.key_positions = {
            "motor_position": [motor_position_x, 0, motor_position_z, 0, 0, 0],
            "loading_zone": [loading_zone_x, 0, loading_zone_z, 0, 90, 0],
            "engage_header_distance": data_points['trf_gripper_edge'] - data_points['MEPG_thickness'],
            "shear_distance": data_points['shear_distance'],
            "sample_height": data_points['sample_height'],
            "microscope": self.get_microscope_position(data),
            "loading_zone_manual": self.get_loading_zone_position(data),
        }

    def move_robot_arm_to_loading_zone(self):
        """ Move the robot arm to the loading zone"""
        loading_zone_manual = self.key_positions['loading_zone_manual']
        engage_header_distance = self.key_positions['engage_header_distance']
        if loading_zone_manual is None:
            loading_zone = self.key_positions['loading_zone']
            x, y, z, Rx, Ry, Rz = loading_zone
            self.robot_arm_controller.move_lin(
                x - engage_header_distance, y, z, Rx, Ry, Rz)
        else:
            x, y, z, Rx, Ry, Rz = loading_zone_manual
            self.robot_arm_controller.move_lin(
                x - engage_header_distance, y, z, Rx, Ry, Rz)
        self.engage_header()
        self.remove_header_from_stage()

    def engage_header(self):
        """ Engage the header. """
        self.robot_arm_controller.open_gripper()
        engage_header_distance = self.key_positions["engage_header_distance"]
        self.robot_arm_controller.move_lin_rel_trf(0, 0, engage_header_distance, 0, 0, 0)
        self.robot_arm_controller.delay(1)
        self.robot_arm_controller.close_gripper()

    def remove_header_from_stage(self):
        """ Remove the header from the stage. """
        sample_height = - self.key_positions['sample_height']
        self.robot_arm_controller.move_lin_rel_trf(
            sample_height, 0, 0, 0, 0, 0)
        self.start_offline_program("Vertical_Oscillation")
        self.robot_arm_controller.zero_joints()

    def move_to_microscope(self):
        """ Move to the microscope. """
        microscope = self.key_positions['microscope']
        x, y, z, Rx, Ry, Rz = microscope
        microscope_tolerance = 10
        engage_header_distance = self.key_positions['engage_header_distance']
        self.robot_arm_controller.move_lin(x, y + engage_header_distance, z - microscope_tolerance, Rx, Ry, Rz)
        self.engage_microscope(microscope_tolerance=microscope_tolerance, engage_header_distance=engage_header_distance)
        self.disengage_microscope(engage_header_distance=engage_header_distance)
        self.remove_header_from_microscope(engage_header_distance=engage_header_distance)

    def engage_microscope(self, microscope_tolerance, engage_header_distance):
        """ Engage the microscope

        Parameters
        ----------
        microscope_tolerance : float
            The tolerance for the microscope
        engage_header_distance : float
            The distance to engage the header

        """
        self.robot_arm_controller.move_lin_rel_trf(
            0, 0, engage_header_distance, 0, 0, 0)
        self.robot_arm_controller.move_lin_rel_trf(
            -microscope_tolerance, 0, 0, 0, 0, 0)
        self.robot_arm_controller.open_gripper()

    def disengage_microscope(self, engage_header_distance):
        """ Disengage the microscope

        Parameters
        ----------
        engage_header_distance : float
            The distance to engage the header

        """
        self.robot_arm_controller.move_lin_rel_trf(
            0, 0, -engage_header_distance * 2, 0, 0, 0)

    def remove_header_from_microscope(self, engage_header_distance):
        """ Remove the header from the microscope

        Parameters
        ----------
        engage_header_distance : float
            The distance to engage the header
        """
        shear_distance = self.key_positions['shear_distance']
        z_tolerance = 50
        self.robot_arm_controller.move_lin_rel_trf(0, 0, engage_header_distance * 2, 0, 0, 0)
        self.robot_arm_controller.close_gripper()
        self.robot_arm_controller.delay(1)
        self.robot_arm_controller.move_lin_rel_trf(0, -shear_distance * 0.75, 0, 0, 0, 0)
        self.robot_arm_controller.move_lin_rel_trf(0, 0, -z_tolerance, 0, 0, 0)
        self.robot_arm_controller.zero_joints()

    def return_header_to_carousel(self):
        """ Return the header to the carousel. """

        loading_zone_manual = self.key_positions['loading_zone_manual']
        sample_height = self.key_positions['sample_height']
        engage_header_distance = self.key_positions['engage_header_distance']
        if loading_zone_manual is None:
            loading_zone = self.key_positions['loading_zone']
            x, y, z, Rx, Ry, Rz = loading_zone
            self.robot_arm_controller.move_lin(x, y, z + sample_height, Rx, Ry, Rz)
        else:
            x, y, z, Rx, Ry, Rz = loading_zone_manual
            self.robot_arm_controller.move_lin(x, y, z + sample_height, Rx, Ry, Rz)

        # Move sample above loading zone
        # self.robot_arm_controller.move_lin(x, y, z + sample_height, Rx, Ry, Rz)
        self.robot_arm_controller.delay(1)

        # Place sample within vial
        self.robot_arm_controller.move_lin_rel_trf(sample_height, 0, 0, 0, 0, 0)
        self.robot_arm_controller.open_gripper()
        self.robot_arm_controller.delay(1)

        # Disengage robot arm from loading zone
        self.robot_arm_controller.move_lin_rel_trf(0, 0, -engage_header_distance, 0, 0, 0)

    def sample_iteration(self):
        """ Sample iteration. """

        self.move_robot_arm_to_loading_zone()
        self.move_to_microscope()
        self.return_header_to_carousel()

    def automated_sample_handling(self):
        """ Automated sample handling. """

        self.automation_controller.reset_automation_variables()
        num_samples = self.automation_controller.get_num_samples()
        og_position = 9.15
        dtheta = 15
        for i in range(1, num_samples + 1):
            self.motor_controller.MoveTo(og_position)
            self.sample_iteration()
            print(f"Finished processing sample {i}")
            og_position = og_position + dtheta
            self.automation_controller.update_progress_bar(i)
