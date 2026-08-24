import pandas as pd
import io

def parse_excel(file_bytes: bytes) -> str:
    df = pd.read_excel(io.BytesIO(file_bytes), sheet_name=None)
    text = ""
    for sheet_name, data in df.items():
        text += f"Sheet: {sheet_name}\n"
        text += data.to_string(index=False) + "\n\n"
    return text
