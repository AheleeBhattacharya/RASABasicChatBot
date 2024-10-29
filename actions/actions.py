# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import datetime

class ActionCheckDeviceStatus(Action):
    def name(self) -> Text:
        return "action_check_device_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        device = tracker.get_slot("device")
        if not device:
            dispatcher.utter_message(text="Could you specify which device you're having issues with?")
            return []

        # Simulate checking device status
        device_status = self.get_device_status(device)
        if device_status["status"] == "operational":
            message = f"The {device} appears to be working normally. Are you experiencing specific issues with it?"
        else:
            message = f"I've detected an issue with the {device}. {device_status['message']}"
        
        dispatcher.utter_message(text=message)
        return [SlotSet("device", device)]

    def get_device_status(self, device: Text) -> Dict[str, str]:
        # This would typically make an API call to your device monitoring system
        # Mock implementation for demonstration
        return {
            "status": "operational",
            "message": "All systems functioning normally."
        }

class ActionCreateSupportTicket(Action):
    def name(self) -> Text:
        return "action_create_support_ticket"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        issue_type = tracker.get_slot("issue_type")
        device = tracker.get_slot("device")
        software = tracker.get_slot("software")
        
        # Create ticket details
        ticket_details = {
            "timestamp": datetime.datetime.now().isoformat(),
            "issue_type": issue_type,
            "device": device,
            "software": software,
            "conversation_id": tracker.sender_id
        }
        
        # Simulate ticket creation
        ticket_number = self.create_ticket(ticket_details)
        
        message = f"I've created support ticket #{ticket_number} for your issue. An IT support specialist will review it shortly."
        dispatcher.utter_message(text=message)
        
        return []

    def create_ticket(self, details: Dict[str, Any]) -> str:
        # This would typically make an API call to your ticketing system
        # Mock implementation for demonstration
        return "INC" + datetime.datetime.now().strftime("%Y%m%d%H%M")

class ActionCheckSoftwareCompatibility(Action):
    def name(self) -> Text:
        return "action_check_software_compatibility"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        software = tracker.get_slot("software")
        if not software:
            dispatcher.utter_message(text="Which software are you trying to install?")
            return []
        
        # Check compatibility
        compatibility = self.check_compatibility(software)
        if compatibility["compatible"]:
            message = f"{software} is compatible with your system. Would you like installation instructions?"
        else:
            message = f"There might be compatibility issues with {software}. {compatibility['message']}"
        
        dispatcher.utter_message(text=message)
        return [SlotSet("software", software)]

    def check_compatibility(self, software: Text) -> Dict[str, Any]:
        # This would typically check against a system requirements database
        # Mock implementation for demonstration
        return {
            "compatible": True,
            "message": "System meets all requirements."
        }

class ActionCheckNetworkStatus(Action):
    def name(self) -> Text:
        return "action_check_network_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Simulate checking network status
        network_status = self.get_network_status()
        
        if network_status["status"] == "operational":
            message = "All network systems are currently operational. Are you experiencing specific connectivity issues?"
        else:
            message = f"We're experiencing some network issues: {network_status['message']}"
        
        dispatcher.utter_message(text=message)
        return []

    def get_network_status(self) -> Dict[str, str]:
        # This would typically make an API call to your network monitoring system
        # Mock implementation for demonstration
        return {
            "status": "operational",
            "message": "All networks functioning normally."
        }

# from typing import Any, Text, Dict, List, Optional
# from rasa_sdk import Action, Tracker, FormValidationAction
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet, EventType
# from rasa_sdk.types import DomainDict
# import requests
# import datetime
# import re

# class ValidateUserIdentificationForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_user_identification_form"

#     def validate_employee_id(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         """Validate employee_id value."""
#         if not re.match(r"^EMP\d{3}$", slot_value):
#             dispatcher.utter_message(text="Please enter a valid employee ID in the format 'EMPxxx'")
#             return {"employee_id": None}
#         return {"employee_id": slot_value}

# class ActionVerifyUser(Action):
#     def name(self) -> Text:
#         return "action_verify_user"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         name = tracker.get_slot("name")
#         employee_id = tracker.get_slot("employee_id")
        
#         # Verify user against employee database
#         if self.verify_employee(name, employee_id):
#             return [SlotSet("verified", True)]
        
#         dispatcher.utter_message(template="utter_verification_failed")
#         return [SlotSet("verified", False)]

#     def verify_employee(self, name: Text, employee_id: Text) -> bool:
#         # Mock implementation - would typically check against employee database
#         # Return True for demonstration purposes
#         return True

# class ActionHandlePasswordReset(Action):
#     def name(self) -> Text:
#         return "action_handle_password_reset"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         if not tracker.get_slot("verified"):
#             dispatcher.utter_message(text="Please verify your identity first.")
#             return []

#         employee_id = tracker.get_slot("employee_id")
#         reset_link = self.generate_reset_link(employee_id)
        
#         message = (f"I've generated a password reset link for your account.\n"
#                   f"Please check your company email for the reset instructions.\n"
#                   f"Reference number: {reset_link}")
        
#         dispatcher.utter_message(text=message)
#         return []

#     def generate_reset_link(self, employee_id: Text) -> Text:
#         # Mock implementation - would typically integrate with password reset system
#         return f"RESET-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"

# class ActionCheckDeviceStatus(Action):
#     def name(self) -> Text:
#         return "action_check_device_status"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         if not tracker.get_slot("verified"):
#             dispatcher.utter_message(text="Please verify your identity first.")
#             return []

#         device = tracker.get_slot("device")
#         employee_id = tracker.get_slot("employee_id")
        
#         if not device:
#             dispatcher.utter_message(text="Could you specify which device you're having issues with?")
#             return []

#         # Check device status for specific employee
#         device_status = self.get_device_status(device, employee_id)
        
#         if device_status["status"] == "operational":
#             message = f"The {device} assigned to you appears to be working normally. Are you experiencing specific issues with it?"
#         else:
#             message = f"I've detected an issue with your {device}. {device_status['message']}"
        
#         dispatcher.utter_message(text=message)
#         return []

#     def get_device_status(self, device: Text, employee_id: Text) -> Dict[str, str]:
#         # Mock implementation
#         return {
#             "status": "operational",
#             "message": "All systems functioning normally."
#         }

# class ActionCheckSoftwareCompatibility(Action):
#     def name(self) -> Text:
#         return "action_check_software_compatibility"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         if not tracker.get_slot("verified"):
#             dispatcher.utter_message(text="Please verify your identity first.")
#             return []

#         software = tracker.get_slot("software")
#         employee_id = tracker.get_slot("employee_id")
        
#         if not software:
#             dispatcher.utter_message(text="Which software are you trying to install?")
#             return []
        
#         # Check software compatibility for user's machine
#         compatibility = self.check_compatibility(software, employee_id)
        
#         if compatibility["compatible"]:
#             message = f"{software} is compatible with your system. Would you like installation instructions?"
#         else:
#             message = f"There might be compatibility issues with {software}. {compatibility['message']}"
        
#         dispatcher.utter_message(text=message)
#         return []

#     def check_compatibility(self, software: Text, employee_id: Text) -> Dict[str, Any]:
#         # Mock implementation
#         return {
#             "compatible": True,
#             "message": "System meets all requirements."
#         }

# class ActionCreateSupportTicket(Action):
#     def name(self) -> Text:
#         return "action_create_support_ticket"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         if not tracker.get_slot("verified"):
#             dispatcher.utter_message(text="Please verify your identity first.")
#             return []
