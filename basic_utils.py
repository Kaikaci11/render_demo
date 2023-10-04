import json
import mimetypes


def read_file(path:str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
            return text
    except FileNotFoundError:
        pass

    return ""


def read_file_as_list(path:str) -> list[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read()
            lines = lines.split('\n')
            lines = [line for line in lines if line] #remove empty strings
            lines = [ii for n,ii in enumerate(lines) if ii not in lines[:n]] #remove duplicates
        return lines
    except FileNotFoundError:
        pass

    return []


def read_json(setting:str, path:str="tracking_ids.json") -> dict|list:

    with open(path, "r", encoding="utf-8") as f:
        data = json.loads(f.read())

    lines = data[setting]

    return lines


def update_tracking_ids_json_file(account_login:str, new_dict:dict, path:str = "tracking_ids.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.setdefault(account_login,{}).update(new_dict)

    with open(path, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_mime_type(file_path:str) -> str:
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type