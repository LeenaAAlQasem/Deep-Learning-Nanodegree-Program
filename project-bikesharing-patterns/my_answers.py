import numpy as np


class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize weights
        self.weights_input_to_hidden = np.random.normal(0.0, self.input_nodes**-0.5, 
                                       (self.input_nodes, self.hidden_nodes))

        self.weights_hidden_to_output = np.random.normal(0.0, self.hidden_nodes**-0.5, 
                                       (self.hidden_nodes, self.output_nodes))
        self.lr = learning_rate
        
        
        ## I used "math.exp," but eventually, it causes an error so, I replace it with "np.exp" ##
        
        self.activation_function = lambda x : 1 / (1 + np.exp(-x))
        
        # def sigmoid(x):
        #  return 1 / (1 + np.exp(-x))  
        # self.activation_function = sigmoid

    def train(self, features, targets):

        n_records = features.shape[0]
        delta_weights_i_h = np.zeros(self.weights_input_to_hidden.shape)
        delta_weights_h_o = np.zeros(self.weights_hidden_to_output.shape)
        for X, y in zip(features, targets):
            
            final_outputs, hidden_outputs = self.forward_pass_train(X)  
            
            delta_weights_i_h, delta_weights_h_o = self.backpropagation(final_outputs, hidden_outputs, X, y, 
                                                                        delta_weights_i_h, delta_weights_h_o)
        self.update_weights(delta_weights_i_h, delta_weights_h_o, n_records)


    def forward_pass_train(self, X):


        ### Forward pass ###
        hidden_inputs = np.dot(X, self.weights_input_to_hidden) 
        hidden_outputs = self.activation_function(hidden_inputs) 

        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output) 
        final_outputs = final_inputs 
        
        return final_outputs, hidden_outputs
    
   
    def backpropagation(self, final_outputs, hidden_outputs, X, y, delta_weights_i_h, delta_weights_h_o):

        
        ### Backward pass ###
        error = y - final_outputs 
        hidden_error = np.dot(self.weights_hidden_to_output , error)
        
        output_error_term = error
        hidden_error_term = hidden_error * hidden_outputs * (1 - hidden_outputs)
        
        ## I tried np.dot(X[None, :], hidden_error_term[None, :]) but it didn't work..
        delta_weights_i_h += hidden_error_term * X[:,None] 
        delta_weights_h_o += output_error_term * hidden_outputs[:,None]
        
        return delta_weights_i_h, delta_weights_h_o

    
    def update_weights(self, delta_weights_i_h, delta_weights_h_o, n_records):
  
        self.weights_hidden_to_output += (self.lr * delta_weights_h_o) / n_records 
        self.weights_input_to_hidden += (self.lr * delta_weights_i_h) / n_records 

        
    def run(self, features):

     
        hidden_inputs = np.dot(features, self.weights_input_to_hidden) 
        hidden_outputs = self.activation_function(hidden_inputs)
        

        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output) 
        final_outputs = final_inputs
        
        return final_outputs



# Set hyperparameters here

iterations = 10000
learning_rate = 0.3
hidden_nodes = 15
output_nodes = 1