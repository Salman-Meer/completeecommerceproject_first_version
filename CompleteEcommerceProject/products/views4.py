from django.core.files.storage import FileSystemStorage
from .views2 import generate_unique_filename
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import product,product_image
from django.contrib import messages
from .utils import delete_image_file
import os

def images(request,slug):
    try:
        if request.method == "POST":
            renamad_images=[]
            slug=request.POST['slug']
            images=request.FILES.getlist('image')
            if not images:
                messages.warning(request,"please input atleast one image")
                return redirect("images",slug=slug)


            product_instance= get_object_or_404(product,slug=slug)
        

            for uploaded_image in images:
                new_name = generate_unique_filename(uploaded_image.name)
                fs = FileSystemStorage()
                filename = fs.save(new_name, uploaded_image)
                # Store the file path (URL) or ImageField instance for saving in the model
                renamad_images.append(filename)

                #return HttpResponse(renamad_images)

            for image_file in renamad_images:
                product_image.objects.create(product_id=product_instance,image=image_file)

            messages.success(request,"image uploaded successfully")
            return redirect("images",slug=slug)

        values={}
        products=product.objects.get(slug=slug)
        values.update({'products':products})
        return render(request,'products/images.html',values)
    except Exception as e:
        messages.warning(request,"something went wrong")
        messages.warning(request,e)
        return render(request,'home/notPageFoundError.html')

def delete_images(request,id):
    #return HttpResponse(id)
    try:
        image=product_image.objects.get(i_id=id)
        imageobj=get_object_or_404(product_image,i_id=id)
        image_path = image.image.path
        productObj=image.product_id
        slug=productObj.slug
        
        if os.path.exists(image_path):
            os.remove(image_path)
            imageobj.delete()
            messages.warning(request,"image deleted successfully")
            return redirect("images",slug=slug)#i think the problem is that the url needs a slug but think how to give the slug with redirect fuction
        else:
            messages.warning(request,"sory image is not found")
            return redirect("images",slug=slug)
        #else:

        # return HttpResponse("image is not found")
        #return HttpResponse(imagelist)
        
            # Deletes the file from media folder
            
        #record.delete()
        
        #return HttpResponse('product deleted successfully')
    except Exception as e:
            messages.warning(request,"something went wrong")
            messages.warning(request,e)
            return render(request,'home/notPageFoundError.html')

      