from pprint import pprint
from django.shortcuts import redirect, render
from .forms import UploadForm
from .lib import handle_file_upload, validate_email
from pprint import pprint

# Create your views here.


def home(request):
    content  = []
    if request.method == "POST":
        myForm = UploadForm(request.POST, request.FILES)
        if myForm.is_valid():
            print("is_valid")
            f = request.FILES["file"]
            file = handle_file_upload(f)
            
            # clean \r\n
            lines = file.split("\r\n")
            # clean space
            lines = [i for i in lines if i]

            # check field
            fcheck = []
            for idx, line in enumerate(lines):
                field = line.split(",")
                if len(field) > 1:
                    fcheck.append({
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

                content.append(field[0])

            pprint(fcheck)
        
        return redirect("home")

    myForm = UploadForm()

    context = {
        "form": myForm,
        "title": "Upload File"
    }
    return render(request, "index.html", context)
