from rasa_nlu.training_data import load_data
#from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Metadata, Interpreter

def train_nlu(data, configuration, model_dir):
	training_data = load_data(data)
	trainer = Trainer(config.load(configuration))
	trainer.train(training_data)
	model_directory = trainer.persist(model_dir, fixed_model_name = 'Chatbot')
	return model_directory

def run_nlu(model_directory):
	interpreter = Interpreter.load('./models/nlu/default/Chatbot')
	print(interpreter.parse(u"I want to order pizza with paneer"))

# define function to ask question
def ask_question(text):
    print(interpreter.parse(text))

# asking question
    ask_question("I want to order pizza with paneer")
    ask_question("What price")

if __name__ == '__main__':
	model_directory = train_nlu('./data/nlu.md', 'config.json', './models/nlu')
	run_nlu('./models/nlu/default/Chatbot')
