from utils import get_data
import pandas as pd
from typing import Any
import plotly.express as px
import streamlit as st


def get_info_from_data(code_str: str) -> Any:
    """
    DataFrame is available as 'df' in the global scope.
    Execute a block of pandas code and return the result.
    The code_str should not contain print functions. instead to should set the data to the 'result' variable
    
    Params:
    code_str (str): The plain string of pandas code to execute.
    
    Returns:
    The result of the executed code.
    """
    df = get_data()
    df = df.drop(["enc", "IMG"], axis=1)
    print(code_str)
    try:
        namespace = {"df": df, "result": None}
        exec(code_str, namespace)
        result = namespace.get('result')

        if result is None:
            result = eval(code_str, namespace)

        if isinstance(result, pd.DataFrame):
            result = result.map(str).to_dict(orient='records')
        elif isinstance(result, pd.Series):
            result = result.map(str).tolist()
        elif isinstance(result, (int, float, str)):
            result = str(result)
        elif result is None:
            result = ""
        elif not isinstance(result, str):
            result = str(result)
            
        print(result)
        return {"result": result}

    except Exception as e:
        print(f"Error executing code: {e}")
        return {"Error": str(e)}



def generate_plotly_chart(code_str: str) -> Any:
    """
    DataFrame is available as 'df' in the global scope.
    Execute a block of plotly code.
    The code_str should generate a plotly figure object and assign it to the 'fig' variable. Don't show it.
    The code_str should not contain fig.show()
    
    Params:
    code_str (str): The plain string of plotly code to execute.
    
    Returns:
    A dictionary containing the path to the saved HTML chart file, or an error message.
    """
    df = get_data()
    df = df.drop(["enc", "IMG"], axis=1)
    print(f"Executing Plotly code: {code_str}")
    try:
        # Prepare the namespace for execution
        namespace = {"df": df, "px": px, "fig": None}
        exec(code_str, namespace)
        fig = namespace.get('fig')

        if fig is None:
            # Attempt to evaluate if exec didn't assign to 'fig' directly
            # This might happen if the code_str is just an expression like px.scatter(...)
            try:
                fig = eval(code_str, namespace)
            except Exception:
                return {"error": "Code did not produce a figure object assigned to 'fig' or return a figure."}


        # Check if the result is a Plotly figure
        if fig is not None:
            st.session_state.messages.append({"role": "assistant", "content": "", "chart": fig})
            return {"created": True}
        else:
            print("Executed code did not result in a Plotly Figure object.")
            return {"error": "Code did not produce a valid Plotly Figure object."}

    except Exception as e:
        print(f"Error executing Plotly code: {e}")
        return {"error": f"Error executing code: {str(e)}"}