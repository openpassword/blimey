import shutil


def after_step(context, feature):
    if hasattr(context, 'remove_path'):
        shutil.rmtree(context.remove_path)
