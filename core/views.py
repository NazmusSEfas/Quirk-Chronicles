from django.shortcuts import render
from django.utils import timezone
from blog.models import Post, Paragraph, Image
import logging

# Create your views here.

logger = logging.getLogger(__name__)
def index(request):
    return render(request, 'core/index.html')

def get_first_image(post):

    paragraph=post.paragraphs.first()
    logger.debug(f"Getting paragraph for paragraph {paragraph.order}: OK")
                    
    if paragraph:
        logger.debug(f"Getting paragraph is ok {paragraph.order}: OK")
    
        image = paragraph.images.first()
        if image:
            logger.debug(f"Getting first image url for  {image.image.url}: OK")
            return image.image.url

    return None
def home_view(request):
    #logger.info(f"Getting images for paragraph : OK")
    recent_post = Post.objects.filter(published_at__isnull=False).order_by('-published_at')[:5]
    
    
    posts_with_images = [{'post':post, 'image':get_first_image(post)} for post in recent_post]

    logger.debug(f"Post and Image url {posts_with_images}: OK")
           

    featured_categories = ["Mythical Journal","Random Musings", "Thoughts & Reflections", "Bizarre Realizations"]
    author_bio = "Welcome to The Quirk Chronicles, a collection of random musings and curious thoughts."


    current_year = timezone.now().year  # Get the current year for the footer
    return render(request, 'core/home.html', {'current_year': current_year,
                                              'posts_with_images':posts_with_images,
                                              'featured_categories':featured_categories,
                                              'author_bio':author_bio})

def dashboard_view(request):
    current_year = timezone.now().year  # Get the current year for the footer
    return render(request, 'core/dashboard.html', {'current_year': current_year})

