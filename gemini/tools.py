from utils import get_data
import pandas as pd
from typing import Any


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
            result = result.tolist()
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
        return "Error"
