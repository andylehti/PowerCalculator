import streamlit as st
import mpmath
import re
import math

# Function to map operation from string to integer value
def map_operation(operation_str):
    operations = ['Add', 'Subtract', 'Multiply', 'Divide']
    return operations.index(operation_str)

# Function to map output format from string to integer value
def map_output_format(output_format_str):
    output_formats = ['Full Rounded Down', 'Scientific Notation', 'Full Rounded Up', 'Full Result', 'Truncated']
    return output_formats.index(output_format_str)

def calculate_result(v, number, operation, precision, output_option):
    mpmath.mp.dps = 1500 + precision

    lines = v.split('\n')

    array = []
    for line in lines:
        values = re.findall(r'\d+', line)
        if values:
            array.extend(map(int, values))

    if array:
        total_result = mpmath.mpf(array.pop(0))
    else:
        raise ValueError("No elements in the array.")

    result_strings = []  # To store the equations of each iteration

    for i, value in enumerate(array):
        last_result = total_result

        if operation == 0:
            total_result += value
            operation_symbol = '+'
        elif operation == 1:
            total_result -= value
            operation_symbol = '-'
        elif operation == 2:
            total_result *= value
            operation_symbol = '⋅'
        elif operation == 3:
            if value == 0:
                total_result = float('inf')  # Return infinite symbol for division by zero
                operation_symbol = '/'
            else:
                total_result /= value
                operation_symbol = '/'
        else:
            raise ValueError("Invalid operation. Please choose 0 for 'Add', 1 for 'Subtract', 2 for 'Multiply', or 3 for 'Divide'.")

        # Decoding output_option from string to integer value
        output_format = map_output_format(output_option[0])

        if output_format == 0:
            output_result = f"{mpmath.floor(total_result)}"
        elif output_format == 1:
            output_result = f"{mpmath.nstr(total_result, 10, min_fixed=0, max_fixed=0)}"
        elif output_format == 2:
            output_result = f"{math.ceil(total_result)}"
        elif output_format == 3:
            output_result = f"{total_result}"
        elif output_format == 4:
            output_result = f"{str(total_result)[:101]}"

        if output_option[3]:  # show_equation is True
            result_string = f"{last_result} {operation_symbol} {value} = {output_result}"
        else:
            result_string = f"{output_result}"

        result_strings.append(result_string)

        if output_option[2]:  # print_iterations is True
            st.write(result_string)

    # Final output result
    if output_format == 0:
        final_output = f"The full rounded down result is: {mpmath.floor(total_result)}"
    elif output_format == 1:
        final_output = f"The result in scientific notation is: {mpmath.nstr(total_result, 10, min_fixed=0, max_fixed=0)}"
    elif output_format == 2:
        final_output = f"The full rounded up result is: {math.ceil(total_result)}"
    elif output_format == 3:
        final_output = f"The full result is: {total_result}"
    elif output_format == 4:
        final_output = f"The truncated result is: {str(total_result)[:101]}"

    st.write(final_output)

    if output_option[1]:  # save final result to file
        with open("calcd.txt", 'w') as f:
            f.write(final_output)
        st.write("")

    if output_option[2]:  # save all outputs to file
        with open("calcd_all.txt", 'w') as f:
            f.write('\n'.join(result_strings))
            f.write('\n' + final_output)
        st.write("")

def main():
    st.sidebar.header('Options') 
    v = st.sidebar.text_area('Enter your data here', value='...')
    number = st.sidebar.number_input('Number', value=0)
    operation_str = st.sidebar.selectbox('Operation', ['Add', 'Subtract', 'Multiply', 'Divide'])
    precision = st.sidebar.slider('Precision', min_value=500, max_value=10000, value=500)
    output_format_str = st.sidebar.selectbox('Output Format', ['Full Rounded Down', 'Scientific Notation', 'Full Rounded Up', 'Full Result', 'Truncate'])
    save_to_file = 1
    print_iterations = st.sidebar.checkbox('Print Iterations')
    show_equation = st.sidebar.checkbox('Show Equations')
    output_option = (output_format_str, save_to_file, print_iterations, show_equation)

    if st.button('Calculate'):
        try:
            # Mapping operation from string to integer value
            operation = map_operation(operation_str)
            calculate_result(v, number, operation, precision, output_option)
        except ValueError as e:
            st.error(str(e))

st.title('Power Calculator')
st.subheader('Autosum, Automultiply, Autodivide, Autosubtract all pasted values')

st.markdown(
    """
    <div style='position:fixed; bottom:0; left:8; width:100%; text-align:center;'>
    <a href='https://github.com/andylehti'>Public Resource License | Andrew Lehti</a>
    </div>
    """,
    unsafe_allow_html=True,
)

if __name__ == '__main__':
    main()
