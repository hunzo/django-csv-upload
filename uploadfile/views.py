import json
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import UploadForm
from .lib import handle_file_upload, upload_email_validation, create_csv_file
from .models import FileUpload, ErrorLogUpload

import uuid

# Create your views here.


def home(request):
    field_ok = []
    if request.method == "POST":
        myForm = UploadForm(request.POST, request.FILES)
        if myForm.is_valid():
            print("is_valid")
            f = request.FILES["file"]
            upload_name = request.POST.get("name")
            file = handle_file_upload(f)

            # clean \r\n
            lines = file.split("\r\n")
            # clean space
            lines = [i for i in lines if i]

            # check field
            field_error = []
            for idx, line in enumerate(lines):
                field = line.split(",")
                if len(field) > 1:
                    field_error.append({
                        "line": idx,
                        "content": field
                    })
                    continue

                # if len(field) > 1:
                #     fcheck.append(f"invalid format line number: {idx+1}")
                    # messages.error(request, f"invalid csv format at line num: {idx + 1}")
                    # return redirect("import-file")

                # if not fcheck:
                #     messages.error(request, f"invalid csv format at line num: zzzzzz")
                    # return redirect("import-file")

                field_ok.append(field[0])

            is_email_valid = upload_email_validation(field_ok)

            ref_id = uuid.uuid4()

            upload = FileUpload()
            upload.content = is_email_valid["valid"]
            upload.count = len(is_email_valid["valid"])
            upload.author = request.user
            upload.name = upload_name
            upload.ref_id = ref_id

            upload.save()
            u = FileUpload.objects.get(ref_id=ref_id)
            for e in is_email_valid["invalid"]:
                u.error.create(
                    ref_id=ref_id,
                    line=e["line"],
                    email=e["email"],
                    error_message=e["error_message"],
                )

        return redirect("home")

    myForm = UploadForm()
    fileUpload = FileUpload.objects.all().order_by("-created_at")

    context = {
        "form": myForm,
        "title": "Upload File",
        "file_upload": enumerate(fileUpload)
    }
    return render(request, "index.html", context)


def valid_generate_csv(request):
    refId = request.GET.get("id")

    fileSet = FileUpload.objects.filter(ref_id=refId)
    temp = eval(fileSet[0].content)
    res = create_csv_file({"valid": temp}, "valid")

    return res


def invalid_generate_csv(request):
    refId = request.GET.get("id")

    fileSet = ErrorLogUpload.objects.filter(ref_id=refId)
    tempList = []

    for i in fileSet.all():
        temp = {}
        temp["line"] = i.line
        temp["email"] = i.email
        temp["error_message"] = i.error_message
        tempList.append(temp)

    res = create_csv_file({"invalid": tempList}, "invalid")

    return res
