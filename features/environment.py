import shutil


def after_scenario(context, feature):
    if hasattr(context, 'remove_path'):
        shutil.rmtree(context.remove_path)
