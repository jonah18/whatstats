import os

rootDir = os.path.dirname(__file__)

# Configurations for app
env = dict(
    uploadFolder=os.path.join(rootDir, '/resources')
)
