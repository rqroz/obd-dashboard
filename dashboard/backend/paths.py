"""
Path definition for file attributes on models.
"""

def user_img_path(instance, filename):
    return f'users/{instance.user.id}/imgs/{filename.encode("utf-8")}'
