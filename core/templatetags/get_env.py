import os
from dotenv import load_dotenv

load_dotenv()

from django import template

register = template.Library()


@register.simple_tag
def get_env_var(key):
    return os.environ.get(key)