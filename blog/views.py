# post/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Paragraph, Image
from .forms import PostForm, ParagraphFormSet
import logging

logger = logging.getLogger(__name__)

def post_list_view(request):
    posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')  # Get published posts
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Get the post or return 404 if not found
    paragraphs = post.paragraphs.all()  # Get related paragraphs
    return render(request, 'blog/post_detail.html', {'post': post, 'paragraphs': paragraphs})

@login_required
def add_post_view(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)#ask what request.POST returns
        formset = ParagraphFormSet(request.POST, queryset=Paragraph.objects.none())


        #atfirst, make the post, which is like a place holder for the paragraphs
        if post_form.is_valid() and formset.is_valid():
            post = post_form.save(commit=False)#atfirst add the user, then we will commit
            post.created_by = request.user
            post.save()

            paragraph_order = 0
            #now make and save the paragraphs
            for idx, form in enumerate(formset):
                paragraph = form.save(commit = False)
                paragraph.post = post
                paragraph.order = paragraph_order
                paragraph.save()
                paragraph_order += 1
                #handling multiple images for a paragraph
                image_field_key = f'images_{idx+1}'
                logger.debug(f"Checking for Key {image_field_key}")
                    
                if image_field_key in request.FILES:
                    
                    images = request.FILES.getlist(image_field_key)
                    logger.debug(f"Saving images for paragraph {paragraph.order}: {[img.name for img in images]}")
                    
                    for image in images:
                        Image.objects.create(paragraph=paragraph, image = image)
                else:
                    logger.warning(f"No images found for {request.FILES}")

            #for dynamically added paragraph
            additional_paragraphs = request.POST.getlist('paragraph-content')
            logger.debug(f"Saving dynamic images aaa for paragraph {additional_paragraphs}")
                
            for idx,content in enumerate(additional_paragraphs):
                logger.debug(f"Saving dynamic images pgc for paragraph {content}")
                
                new_paragraph = Paragraph.objects.create(post=post,content=content,order = paragraph_order)
                logger.debug(f"Saving dynamic images for paragraph {paragraph_order}")
                paragraph_order+=1
                dynamic_image_key = f'images_new_{idx+1}'
                logger.debug(f"Image comparision {dynamic_image_key} vs  {[img.name for img in request.FILES.getlist(dynamic_image_key)]}")
                
                if dynamic_image_key in request.FILES:
                    
                    for image in request.FILES.getlist(dynamic_image_key):
                        Image.objects.create(paragraph=new_paragraph, image = image)
                
            messages.success(request, 'Post and paragraph added successfully.')
            return redirect('post_list')#Redirect to the post list
    else:
        post_form = PostForm()#creating a brand new post
        formset = ParagraphFormSet(queryset=Paragraph.objects.none())

    return render(request, 'blog/add_post.html',{'post_form':post_form,'formset':formset})
