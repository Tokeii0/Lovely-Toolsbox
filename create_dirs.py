import os

dirs = [
    'src',
    'src/ui',
    'src/core',
    'src/utils',
    'config',
    'tools'
]

for dir in dirs:
    os.makedirs(dir, exist_ok=True)
    print(f'Created directory: {dir}')
