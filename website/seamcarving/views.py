import numpy as np
import cv2
import time
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.core.files import File
from .util import save_upload
from .seam_carving import SeamCarver
# Create your views here.


def index(request):
	template = 'seamcarving/index.html'
	return render(request, template)

def resize(request):
	template = 'seamcarving/resize.html'
	return render(request, template)

def amplification(request):
	template = 'seamcarving/amplification.html'
	return render(request, template)

def mask(request):
	template = 'seamcarving/mask.html'
	return render(request, template)

def removal(request):
	template = 'seamcarving/removal.html'
	return render(request, template)

def video(request):
	template = 'seamcarving/video.html'
	return render(request, template)

def process(request):
	if request.method == 'POST':
		input_image = request.FILES['input-image']
		input_image_filename = './data/' + str(time.time()) + '_input.png'
		save_upload(input_image, input_image_filename)
		operation = int(request.POST.get('operation', '1'))
		operations = ['Resize w/o Mask', 'Resize w/ Mask', 'Object Removal', 'Content Amplification']
		print('Operation: ' + operations[operation - 1])
		# input_image = cv2.imdecode(np.fromstring(request.FILES['input-image'].read(), np.uint8), cv2.IMREAD_COLOR)
		# image resize without mask or image resize with mask
		if operation == 1 or operation == 2:
			new_height = int(request.POST.get('new-height', '0'))
			new_width = int(request.POST.get('new-width', '0'))
			print('New height: ' + str(new_height))
			print('New width: ' + str(new_width))
		# image resize with mask or object removal
		if operation == 2 or operation == 3:
			mask_image = request.FILES['mask-image']
			mask_image_filename = './data/' + str(time.time()) + '_mask.png'
			save_upload(mask_image, mask_image_filename)

		if operation == 1:
			obj = SeamCarver(input_image_filename, new_height, new_width)
		elif operation == 2:
			obj = SeamCarver(input_image_filename, new_height,
							 new_width, protect_mask=mask_image_filename)
		elif operation == 3:
			obj = SeamCarver(input_image_filename, 0, 0,
							 object_mask=mask_image_filename)
		elif operation == 4:
			obj = SeamCarver(input_image_filename, 0, 0)

		output_image_filename = './data/' + str(time.time()) + '_output.png'
		obj.save_result(output_image_filename)
		return HttpResponse(output_image_filename)
		
	else:
		return HttpResponseForbidden('Allowed only via POST')
