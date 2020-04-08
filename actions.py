# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


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
#from rasa_core.actions import Action
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa.core.actions.action import Action
from rasa.core.events import SlotSet, AllSlotsReset, Restarted
import json
import rasa.core
import sys
'''import warning
sys.modules["rasa_core"] = rasa.core
warnings.warn(
    "The 'rasa_core' package has been renamed. You should change "
    "your imports to use 'rasa.core' instead.",
    UserWarning,
)'''

class ActionOrderPizza(Action):
	def name(self):
		return 'utter_action_order_pizza'
	def run(self):
		print('Ordering Pizza is completed! It should be with you soon')
		pass

class ActionOrderPizzaConfirm(Action):
	def name(self):
		return 'utter_order_pizza_confirm'
	def run(self):
		print('order pizza confirm! thank you for ordering pizza')
		pass

class ActionOrderPizzaGreetings(Action):
	def name(self):
		return 'utter_order_pizza_ask_help'
	def run(self):
		print('see you')
		pass

class ActionOrderPizzaGreetingsBye(Action):
	def name(self):
		return 'utteraction_order_pizza_greetings_bye'
	def run(self):
		print('okey see you later')
		pass

class ActionOrderPizzaAddress(Action):
	def name(self):
		return 'utter_order_pizza_ask_address'
	def run(self):
		print('123 Evergreen Terrace, Springfield')
		pass
class ActionOrderPizzaTopping(Action):
	def name(self):
		return'utter_action_order_pizza_topping'
	def run(self):
		print('onion')
		pass

class ActionOrderPizzaProvideAll(Action):
	def name(self):
		return ' utter_order_pizza_provide_all'
	def run(self):
		print('I want to order large size pizza with olives')
		pass

class ActionOrderPizzaProvideNone(Action):
	def name(self):
		return ' utter_order_pizza_provide_none'
	def run(self):
		print('I want order pizza ')
		pass

class ActionOrderPizzaProvideSize(Action):
	def name(self):
		return ' utter_order_pizza_ask_size'
	def run(self):
		print(' I want to large size pizza')
		pass
class ActionOrderPizzaProvideType(Action):
	def name(self):
		return 'utter_order_pizza_provide_type'
	def run(self):
		print('please select pizza types')
		return[]










