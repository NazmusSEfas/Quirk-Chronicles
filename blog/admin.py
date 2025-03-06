# random_musings/admin.py

from django.contrib import admin
from .models import Post, Paragraph, Image

# Inline class to handle Images within Paragraphs
class ImageInline(admin.StackedInline):
    model = Image
    extra = 1  # Display one extra image field by default
    #fields = ['image', 'uploaded_at']  # Fields to display
    #readonly_fields = ['uploaded_at']  # 'uploaded_at' should be readonly

# Inline class to handle Paragraphs within Posts
class ParagraphInline(admin.StackedInline):
    model = Paragraph
    extra = 1  # Display one extra paragraph field by default
    fields = ['content', 'order']  # Display content and order for each paragraph
    ordering = ['order']  # Default ordering of paragraphs
    inlines = [ImageInline]  # Nest ImageInline to allow images to be added for each paragraph

# Admin class to manage Posts
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'created_at', 'published_at']  # Display these fields in the post list
    search_fields = ['title', 'created_by__username']  # Searchable fields in the admin interface
    list_filter = ['created_by', 'published_at']  # Enable filtering by author and publish date

    inlines = [ParagraphInline]  # Paragraphs (and their images) can be managed inline within a post

    # Automatically set the current user as the creator when saving a new post
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# Register the Post model with its custom PostAdmin configuration
admin.site.register(Post, PostAdmin)

# Optionally register Paragraph and Image models if needed
admin.site.register(Paragraph)
admin.site.register(Image)

