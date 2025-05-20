from typing import List, Dict
from fastapi import HTTPException
import os


def get_files_from_directory(directory: str) -> List[Dict[str, str]]:
    """
    Retrieves a list of files from the specified directory.

    Args:
        directory (str): The path to the directory.

    Returns:
        List[str]: A list of file names in the directory. Returns empty list on error.
    """
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return [{"name": f, "type": get_file_type(f)} for f in files]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Directory not found: {directory}")
    except Exception as e:
        print(f"Error reading directory: {e}") 
        return []  


def get_file_type(filename: str) -> str:
    """
    Determines the type of a file based on its extension.

    Args:
        filename (str): The name of the file.

    Returns:
        str: The file type (e.g., "text", "image", "other").
    """
    if "." not in filename:
        return "other"
    extension = filename.split(".")[-1].lower()
    if extension in ["txt", "md", "py", "js", "html", "css"]:
        return "text"
    elif extension in ["jpg", "jpeg", "png", "gif", "svg"]:
        return "image"
    elif extension in ["pdf"]:
        return "pdf"
    else:
        return "other"
