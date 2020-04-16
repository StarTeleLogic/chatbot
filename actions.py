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
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet

#from joblib import load
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

class ElicitationForm(FormAction):
    """Example of a custom form action"""

	def name(self) -> Text:
        """Unique identifier of the form"""

		return "elicitation_form"

	@staticmethod
	def required_slot(tracker: Tracker) -> List[Text]:

		return["pizza_del_address", "pizza_size", "pizza_toppings", "pizza_type"]

	def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""
	return{
		"pizza_del_address":[self.from_entity(
                entity="pizza_del_address", 
                intent="inform"),
                self.from_text()],
		"pizza_size":[self.from_entity(
                entity="pizza_size", 
                intent="inform"),
                self.from_text()],
		"pizza_toppings":[self.from_entity(
                entity="pizza_toppings", 
                intent="inform"),
                self.from_text()],
		"pizza_type":[self.from_entity(
                entity="pizza_type", 
                intent="inform"),
                self.from_text()]
	}


	@staticmethod
	def answers_db() -> Dict[str, List]:
        """Database of supported cuisines"""

		return {'pizza_del_address': ['my address is 123 Evergreen Terrace, Springfield',
			'sector 62, noida', 'noida'],
			'pizza_size': ['I want large pizza_size', 
					'I want to order large pizza_size', 
					'I like to order large pizza_size',
					'I would like to order large pizza_size',
					'take order for large pizza_size', 
					'provide large pizza_size',
					'large pizza_size  will be good',
					'large pizza_size is good',
					'large pizza_size is good to go',
					'ok write down large pizza_size',
					'ok give me large pizza_size',
					'ok deliver large pizza_size',
					'deliver large pizza'],
			'pizza_toppings':['I want onion pizza_toppings',
					'I want to order onion pizza_toppings',
					'I like to order onion pizza_toppings',
					'I would like to order onion pizza_toppings',
					'take order for onion pizza_toppings',
					'provide onion pizza_toppings']
			'pizza_type': ['Margherita pizza_type',
					'I want Margherita pizza_type',
					'I want to order Margherita pizza_type',
					'I like to order Margherita pizza_type',
					'ok give me Margherita pizza_type',
					'ok deliver Margherita pizza_type',
					'deliver Margherita pizza_type',
					'Veg Extravaganza pizza_type',
					'Veg Extravaganza pizza_type:veg extravaganza',
					'veg extravaganza pizza_type', 'other']}
	def validate_cuisine(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if value.lower() in self.cuisine_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"cuisine": value}
        else:
            dispatcher.utter_message(template="utter_wrong_cuisine")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"cuisine": None}

	def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(template="utter_submit")

	return []

	
	class DetectDialect(Action):
		def name(self) -> Text:
        """Unique identifier of the form"""

        return "detect_dialect"

	def run(self, dispatcher, tracker, domain):
        """place holder method for guessing dialect """
        # let user know the analysis is running
        dispatcher.utter_message(template="utter_working_on_it")

        # get information from the form (maybe)
        pizza_address = tracker.get_slot("pizza_del_address")
        print(pizza_address)

        # classify test case
        
        training_data, d_classes, meta_data, test_case = OrderPizzaGreeting.load_data()
        test_case_encoded = OrderPizzaGreeting.encode_data(test_case, training_data)
        dialects = OrderPizzaGreeting.OrderPizzaGreetingsBye(test_case_encoded, meta_data, training_data)

        # always guess us for now
        return [SlotSet("dialect", dialects)]

	class OrderPizzaGreeting():

		def name(self) -> Text:
			
			return "utter_order_pizza_greetings"
		def load_data():
			''' Load in the pretrained model & label encoders'''
			traning_data = load('/home/startele/Project_chatbot/models/nlu/Chatbot/training_data.json')
			d_class = load('/home/startele/Project_chatbot/models/dialogue/domain.yml')
			meta_data = load('/home/startele/Project_chatbot/models/nlu/Chatbot/meta_data.json')
			test_case = load('/home/startele/Project_chatbot/training_data.json') 

			# remove target class from test data
        	del test_case["class_target"]

       		 # update the classes for each of our label encoders
        	for key,item in training_data.items():
            		training_data[key]._classes = d_classes[key]

        		return training_data, d_classes, meta_data, test_case

		def encode_data(input_data, training_data):
        ''' Encode our input data with pre-trained label encoders.'''
                
      			test_case_encoded = input_data

        		for i, row in input_data.items():
            			test_case_encoded[i] = training_data[i].transform([input_data[i]])

       	 			test_case_encoded = test_case_encoded.apply(lambda x:x[0])

        		return test_case_encoded

		def OrderPizzaGreetingsBye (test_case_encoded, meta_data, training_data):
        ''' Take in encoded data & return top most order pizzza '''
        
        	# convert input data to DMatrix format
        		test_case_encoded_d = xgb.DMatrix(test_case_encoded)
        		test_case_encoded_d.feature_names =  test_case_encoded.index.tolist()

        	# classify using our pre-trained model
        		predictions = meta_data.predict(test_case_encoded_d)

       		 # return the top 3 classes
        		top_3 = np.argsort(predictions, axis=1)[ : ,-3 : ]

        		pizza_order = training_data["class_target"].inverse_transform(top_3[0].tolist())

        		return 'pizza_order'




	
			

		
		

	









