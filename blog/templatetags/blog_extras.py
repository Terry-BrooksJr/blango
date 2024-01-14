from blog.models import Post
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from typing import Union, Optional
register = template.Library()

@register.filter
def author_details(post_author: User, current_user: Optional[User]) -> str: 
    """Returns a string containing the post's author details."""
    if not isinstance(post_author,User):
         return " "
    try:
        user_data = User.objects.get(pk=post_author.id)
        if post_author.id == current_user.id:
            return format_html('<strong>Me!</strong>')
        if user_data.first_name and user_data.last_name:
            name = escape(f"{escape(user_data.first_name)} {escape(user_data.last_name)}")
        elif user_data.first_name:
            name = escape(user_data.first_name)
        else: 
            name = escape(user_data.username)
            

        if user_data.email:
            prefix = format_html('<a href="mailto:{}">', user_data.email)
            suffix = format_html("</a>")
        else: 
            prefix = ""
            suffix = ""
        return format_html('{}{}{}', prefix, name, suffix)
    except ObjectDoesNotExist as e:
        return " "
