from django.shortcuts import render
from .resources import HomeResource
from django.http import HttpResponse, HttpResponseRedirect


from tablib import Dataset

def export(request):
	home_resource = HomeResource()
	dataset = home_resource.export()
	response = HttpResponse(dataset.csv, content_type = "text/csv")
	response['Content-Disposition'] = 'attachment; filename="homeprice.csv"'
	return response

# Create your views here.

def simple_upload(request):
	if request.method == 'POST':
		home_resource = HomeResource()
		dataset = Dataset()
		new_home = request.FILES['myfile']

		imported_data = dataset.load(new_home.read())
		result = home_resource.import_data(dataset, dry_run=True)
		if not result.has_errors():
			home_resource.import_data(dataset, dry_run=False)
	return render(request,'core/simple_upload.html')

def map_display(request):
	return render(request,'index.html')