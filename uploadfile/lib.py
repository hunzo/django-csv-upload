from django.http import HttpResponse
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
import chardet
import csv


def create_csv_file(email_validate_result, validType):
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    respone = HttpResponse(content_type="text/csv")
    respone["Content-Disposition"] = f"attachment; filename={validType}_email_format_{now}.csv"

    writer = csv.writer(respone)

    if validType == "valid":
        for r in email_validate_result[validType]:
            writer.writerow([r])
        return respone
    
    if validType == "invalid":
        writer.writerow(["line", "email", "error_message"])

        for r in email_validate_result["invalid"]:
            writer.writerow([r["line"], r["email"], r["error_message"]])
            # print(r[""])
        return respone

    return None


def check_email(email):
    try:
        # Validate & take the normalized form of the email
        # address for all logic beyond this point (especially
        # before going to a database query where equality
        # does not take into account normalization).
        email = validate_email(email).email
        return "valid"
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        return str(e)


def handle_file_upload(fileRequest):
    # print(fileBytes.read().decode("utf-8-sig").encode("utf-8"))
    file = fileRequest.read()
    temp = chardet.detect(file)
    file_encoding = temp['encoding']

    try:
        if "UTF" in file_encoding:
            print(f"utf-detect: {file_encoding}")
            file_content = file.decode(file_encoding)
        else:
            print(f'none-utf-detet: {file_encoding}')
            file_content = file.decode('iso-8859-1')

    except Exception as e:
        print(str(e))
        return None

    return file_content


def upload_email_validation(recipient_list: list):
    valid_list = []
    invalid_list = []
    for idx, email in enumerate(recipient_list):
        chk = check_email(email)
        if chk == "valid":
            valid_list.append(email)
        else:
            err = {
                "line": idx,
                "email": email,
                "error_message": chk
            }
            invalid_list.append(err)

    return {
        "valid": valid_list,
        "invalid": invalid_list
    }
