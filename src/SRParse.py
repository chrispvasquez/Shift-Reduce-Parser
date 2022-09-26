from Tables import Tables
from Helper_Functions import *

def SRParse(myExpression):

    if myExpression == "":
        print(4)
        return None, None, None, None, None, None, 4

    # Instantiate a stack starting its first index value with 0
    stack = ['0']
    my_actions = []
    my_expressions = []
    my_R_states = []

    my_coords = []

    expression = myExpression.replace(" ", "")

    if expression[len(expression)-1] != "$":
        expression += "$"
        
    my_tables = Tables()

    # Read input string character by character
    while True:
        current_symbol = getCurrentSymbol(expression, my_tables)

        # Determine if the current symbol is valid
        if current_symbol in my_tables.symbols:

            current_stack_value = stack[-1]
            my_expressions.append(expression)

            # Determine State Number
            state_num = getStateNum(current_stack_value)

            # Check if the Y, X for the the action table results in a value or not
            if (state_num, current_symbol) in my_tables.action:

                my_coords.append((state_num, current_symbol))

                # Get the proper action from the table
                current_action = my_tables.action[(state_num, current_symbol)]
                my_actions.append(current_action)

                if current_action[0] == 'S':

                    stack.append(current_stack_value + current_symbol + current_action[1:])
                    expression = expression.lstrip(current_symbol)


                elif current_action[0] == 'R':

                    # Get the proper rule according to the action table R#
                    current_protocol = my_tables.prodRules[current_action]

                    # Store the right hand side of the protocol
                    protocol_left = current_protocol[0]
                    protocol_right = current_protocol[1]
                    protocol_right_index = len(protocol_right) - 1

                    # Iterate over the current stack value until we find all characters within the right
                    # hand side of the protocol, then break
                    for c in reversed(current_stack_value):

                        if c == protocol_right[protocol_right_index]:
                            protocol_right = protocol_right.rstrip(protocol_right[-1])
                            protocol_right_index -= 1

                        current_stack_value = current_stack_value.rstrip(c)

                        if not protocol_right:
                            break


                    # Determine State Number before appending left hand side
                    state_num = getStateNum(current_stack_value)

                    # With the string properly trimed, we can append the left hand side of the protocol
                    current_stack_value += protocol_left

                    # Add the proper value from the GoTo table to the stack value
                    current_stack_value += my_tables.goto[(state_num, protocol_left)]

                    my_R_states.append(my_tables.goto[(state_num, protocol_left)])

                    my_coords.append((state_num, protocol_left))

                    stack.append(current_stack_value)

                elif current_action == 'accept':

                    used_prod_rules = []
                    terminal_output = []
                    r_counter = 0

                    for i in my_actions:
                        if i[0] == 'R':
                            expr = my_tables.prodRules[i]
                            L = expr[0]
                            R = expr[1]
                            if expr[1] == "E+T" or expr[1] == "T*F":
                                R = expr[1].replace("", " ")[1: -1]
                            used_prod_rules.append(L + " -> " + R)


                        if i[0] == "S":
                            terminal_output.append("Shift Input. Go to State " + i[1:])

                        elif i[0] == "R":
                            terminal_output.append("Reduce using Production Rule " + i[1:] + ". Go to state " + my_R_states[r_counter])
                            r_counter += 1
                        elif i == "accept":
                            terminal_output.append("Finished!")


                    return stack, my_actions, my_expressions, used_prod_rules, terminal_output, my_coords, 0

                else:
                    # Throw error because it results in an unknown action
                    print(1)
                    return None, None, None, None, None, None, 1

            else:
                # Throw error because it results in a space in the table
                print(1)
                return None, None, None, None, None, None, 2

        else:
            # Throw error because no known symbols were found
            print(1)
            return None, None, None, None, None, None, 3