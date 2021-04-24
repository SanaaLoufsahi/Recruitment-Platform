from django import template
import os

register = template.Library()


def os_path_isdir(path):
    return os.path.isdir('path')