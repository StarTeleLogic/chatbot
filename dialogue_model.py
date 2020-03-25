
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import warnings
import ruamel.yaml
warnings.simplefilter('ignore', ruamel.yaml.error.UnsafeLoaderWarning)

from rasa_core.agent import Agent
from rasa_core.policies import FallbackPolicy, KerasPolicy, MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
#from rasa_core.train import interactive
from rasa_core.utils import EndpointConfig

logger = logging.getLogger(__name__)

fallback = FallbackPolicy(fallback_action_name="utter_unclear",
                          core_threshold=0.2,
                          nlu_threshold=0.1)

def train_dialogue(interpreter,domain_file = 'domain.yml',
                   model_path = './models/dialogue',
                   training_data_file = './data/stories.md'):

    agent = Agent(domain_file, policies=[MemoizationPolicy(), KerasPolicy(), fallback])
    training_data = agent.load_data('./data/stories.md')

    agent.train(
            training_data)

    agent.persist('models/dialogue')
    return agent




def run_pizza_bot(serve_forever=True):
    nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/Chatbot')
    action_endpoint = EndpointConfig(url="http://localhost:5002/api/stories")
    agent = Agent.load('./models/dialogue', interpreter=nlu_interpreter, action_endpoint=action_endpoint)
    
    return agent

if __name__ == '__main__':
    train_dialogue(interpreter=RasaNLUInterpreter)
    run_pizza_bot()
