import torch
import copy
import pandas as pd

BIG_M = 1000000

# The Simplex class
# is used for solving
# linear programming
# problems using the
# simplex method.

class Simplex:
    def __init__(self, json_data):
        """
        The function initializes various variables and data structures used in a mathematical
        optimization problem.
        
        @param json_data The `json_data` parameter is a JSON object that contains the data needed for
        the initialization of the class. It is used to store and pass data between different methods and
        functions within the class. The specific structure and content of the `json_data` object would
        depend on the requirements and design of the
        """
        self.json_data = json_data
        self.cost_function_variables = None
        self.equation_matrix_variables = None
        self.selected_symbols = None
        self.equation_results = None
        self.number_of_variables = None
        self.number_of_constraints = None
        self.type_min_max = None
        self.preprocessed_matrix = None
        self.matrixResult = None;
        self.response = []
        self.tables = []
        self.pivots = []
        self.RCPair = []
        self.addedVariables = []
        
    def json_list(self):
        """
        The function extracts various variables and data from a JSON object and performs some data
        manipulation.
        """
        # Cost function variables
        self.cost_function_variables = self.json_data.get("functionVariables")
        # Equations of constraint matrix
        self.equation_matrix_variables = self.json_data.get("equationVariables")
        # Selected symbol 1: = 2: < 3: >
        self.selected_symbols = self.json_data.get("selectedSymbols")
        self.equation_results = self.json_data.get("equationEqual")
        # Number of variables
        self.number_of_variables = self.json_data.get("variables")
        # Number of contraints
        self.number_of_constraints = self.json_data.get("constraints")
        # Type of simplex min or max
        self.type_min_max = self.json_data.get("type")
        # Replace None values in variables with 0 and convert python list to pytorch tensors
        self.cost_function_variables = torch.tensor(list(map(lambda x: 0 if x is None else x, self.cost_function_variables)), dtype=torch.float64)
        self.equation_matrix_variables = torch.tensor(list(map(lambda row: list(map(lambda element: 0 if element is None else element, row)), self.equation_matrix_variables)), dtype=torch.float64)
        self.equation_results = torch.tensor(list(map(lambda x: 0 if x is None else x, self.equation_results)), dtype=torch.float64)
        self.selected_symbols = self.selected_symbols[:self.number_of_constraints]


    
    
    def create_table(self):
        """
        The function "create_table" takes a set of symbols and creates a matrix representation of a
        linear programming problem.
        """
        # Get sublist of symbols
        
        number_of_variable_lower_bound = self.selected_symbols.count(3)
        number_of_slack_variables = self.selected_symbols.count(2) + self.selected_symbols.count(3)
        number_of_artifical_variables_introduced = 0
        number_of_slack_variables_introduced = 0 

        zeros_matrix = torch.zeros(self.number_of_constraints, self.number_of_constraints + number_of_variable_lower_bound)

        for index, element in enumerate(self.selected_symbols):
            if(element == 1): # element: =
                # Put 1 in artificial constranits
                zeros_matrix[index][(number_of_slack_variables + number_of_artifical_variables_introduced)] = 1
                number_of_artifical_variables_introduced+=1
            elif(element == 2): # element: <
                # Put 1 in slack constraints
                zeros_matrix[index][number_of_slack_variables_introduced] = 1
                number_of_slack_variables_introduced += 1
            elif(element == 3): # element: >
                # Put -1 in slack constraint
                zeros_matrix[index][number_of_slack_variables_introduced] = -1
                number_of_slack_variables_introduced += 1
                # Put 1 in artifical constraints
                zeros_matrix[index][(number_of_slack_variables + number_of_artifical_variables_introduced)] = 1
                number_of_artifical_variables_introduced+=1

        self.addedVariables.append(number_of_artifical_variables_introduced)
        self.addedVariables.append(number_of_slack_variables_introduced)


        # Create header row with zeros
        slack_zeros = torch.zeros(number_of_slack_variables)

        # Define M value in artificial Rows
        artificial_variables_value = None
        if(self.type_min_max == 'Max'):
            artificial_variables_value = torch.full((number_of_artifical_variables_introduced,), -1*BIG_M)
        else:
            artificial_variables_value = torch.full((number_of_artifical_variables_introduced,), BIG_M)

        constraints_header = torch.cat((slack_zeros, artificial_variables_value, torch.tensor([0])), dim=0)

        # Add a constraint header to the cost function and multiply it by -1 using element-wise multiplication.
        self.cost_function_variables = torch.cat((self.cost_function_variables, constraints_header))
        if(self.type_min_max == "Max"):
            self.cost_function_variables = self.cost_function_variables * -1

        # Convert results tensor to column tensor
        self.equation_results = self.equation_results.unsqueeze(1)

        # Concatenate the matrix with the constraint matrix
        self.preprocessed_matrix = torch.cat((self.equation_matrix_variables, zeros_matrix), dim=1)
        
        # Concatenate the column vector with the solutions of the equations with the constraint matrix
        self.preprocessed_matrix = torch.cat((self.preprocessed_matrix, self.equation_results), dim=1)
        
        # Concatenate cost function and constraint matrix
        self.cost_function_variables = self.cost_function_variables.unsqueeze(0)
        self.preprocessed_matrix = torch.cat((self.cost_function_variables, self.preprocessed_matrix), dim=0)

        


    def fix_table_simlpex(self):
        """
        The function fixes a table simplex by selecting specific tensors that meet certain criteria and
        performing calculations on them.
        """
        # Target value to search
        target = 1
        slack_variables = self.selected_symbols.count(2)
        z = self.preprocessed_matrix[0].unsqueeze(0)

        # Specific range of positions within the tensor (for example, from position 1 to 2). In this case, the range pertains to columns with an M value in the header.
        min_posicion = self.number_of_variables + slack_variables + self.selected_symbols.count(3)
        max_posicion = self.preprocessed_matrix[0].shape[0] -2

        print("min_posicion: ", min_posicion, "max position: ", max_posicion)

        # Create a boolean mask that identifies the tensors that meet the criteria.
        mask = ((self.preprocessed_matrix == target) & (torch.arange(self.preprocessed_matrix.size(1)) >= min_posicion) & (torch.arange(self.preprocessed_matrix.size(1)) <= max_posicion)).any(dim=1)

        # Select the tensors that satisfy the boolean mask
        selected_tensors = torch.clone(self.preprocessed_matrix[mask])
        print("selected: ", selected_tensors)
        # Multiply selected tensors by -1.
        selected_tensors = selected_tensors * (-1 * BIG_M)
        # Concatenate the tensors with row z.
        selected_tensors = torch.cat((z, selected_tensors), dim=0)
        # Sum all tensor
        selected_tensors = selected_tensors.sum(dim=0)
        # Replace first row with the new z row 
        self.preprocessed_matrix[0] = selected_tensors




    def start_simplex(self):
        """
        The function "start_simplex" performs the simplex algorithm on a given matrix until the objective
        function coefficients are all non-negative.
        """
        # Transform json data to tensors 
        self.json_list()
        # Create the table with information provide by front-end
        self.create_table()
        # Verify if it is an 'M' case or a simple case with only upper bounds.
        if(self.selected_symbols.count(1) > 0 or self.selected_symbols.count(2) > 0):
            self.fix_table_simlpex()
        # Define matrix as preprocessed matrix
        matrix = self.preprocessed_matrix
        # Select z row 
        z = matrix[0, : -1]
        counter = 0
        # This loop is used to check the status of the simplex algorithm, it runs as long as there are negative numbers in the row z
        while (z.min() < 0):
            self.tables.append(copy.deepcopy(matrix).tolist())
            self.iterate(matrix)
            counter += 1
        matrix[0] = abs(matrix[0])
        self.matrixResult = matrix[0]
        self.tables.append(copy.deepcopy(matrix).tolist())


    def iterate(self, matrix):
        """
        The function performs matrix iteration and updates the matrix based on certain calculations.
        
        @param matrix The `matrix` parameter is a tensor representing a matrix. It is used in the
        `iterate` method to perform calculations and update the matrix.
        """
        # Reshape data
        num_of_cols = matrix.size()[0]-1

        # Indexes and incoming vector
        z = matrix[0,]
        incoming_index = matrix[0, : -1].argmin().item()
        solution_index = z.size(dim=0)-1
        
        solution_column = matrix[:, solution_index]
        incoming_column = matrix[:, incoming_index]

        # Outcoming vector
        div = (solution_column / incoming_column)[1:]
        n = torch.clone(div)
        n[n<0] = torch.inf
        outcoming_index = (n[n >= 0].argmin()+1).item()
        outcoming_row = matrix[outcoming_index, :]

        print("outcoming: ", outcoming_row)

        #Add RCP
        self.RCPair.append([copy.deepcopy(outcoming_index),copy.deepcopy(incoming_index)])

        # New pivot row
        pivot = incoming_column[outcoming_index]
        self.pivots.append(copy.deepcopy(pivot).tolist())
        new_pivot_row = outcoming_row / pivot

        # Calculating the remaining rows
        calculees = torch.cat((
            incoming_column[: outcoming_index],
            incoming_column[outcoming_index + 1:]
        ))

        rows = torch.cat((
            matrix[:outcoming_index],
            matrix[outcoming_index + 1:]
        ))

        rows = rows - (calculees.reshape(num_of_cols, 1) * new_pivot_row)

        # Matrix update
        matrix[:outcoming_index,] = rows[:outcoming_index,]
        matrix[outcoming_index, :] = new_pivot_row
        matrix[outcoming_index+1:,] = rows[outcoming_index:,]


    def print_data(self):
        """
        The function "print_data" prints various variables and information related to a cost function and
        equation matrix.
        """
        print("Cost Function Variables:", self.cost_function_variables)
        print("Equation Matrix Variables:", self.equation_matrix_variables)
        print("Selected Symbols:", self.selected_symbols)
        print("Equation Results:", self.equation_results)
        print("Number of Variables:", self.number_of_variables)
        print("Number of Constraints:", self.number_of_constraints)
        print("Type (Min/Max):", self.type_min_max)

    def getInfo(self):
        """
        The function `getInfo` returns a dictionary containing information about tables, RCPair,
        variables, constraints, addedVariables, and type_min_max, and also generates a CSV file.
        
        @return a dictionary called `response_data`.
        """
        self.RCPair.append([-1, -1])
        response_data = {
            "tables": self.tables,
            "RCPair": self.RCPair,
            "variables": self.number_of_variables,
            "constraints": self.number_of_constraints,
            "addedVariables": self.addedVariables,
            "type": self.type_min_max 
        }      
        self.generatesCSV()
        return response_data  


    
        
    def generatesCSV(self):
        """
        The function generates a CSV file from a nested list of data and saves it as 'tabla.csv'.
        """
        flat_data = [item for sublist in self.tables for item in sublist]
        df = pd.DataFrame(flat_data)
        df.to_csv('tabla.csv', index=False, header=False)
    


