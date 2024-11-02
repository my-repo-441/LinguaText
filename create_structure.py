import os

def create_project_structure(base_dir='project-root'):
    # Directory structure
    structure = {
        'frontend': {
            'public': {},
            'src': {
                'components': {},
                'App.js': ''
            },
            'package.json': ''
        },
        'backend': {
            'app.py': '',
            'requirements.txt': '',
            'transcription.py': ''
        },
        'docker-compose.yml': '',
        'README.md': ''
    }

    def create_dirs_and_files(base, struct):
        for name, content in struct.items():
            path = os.path.join(base, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_dirs_and_files(path, content)
            else:
                with open(path, 'w') as f:
                    f.write(content)

    os.makedirs(base_dir, exist_ok=True)
    create_dirs_and_files(base_dir, structure)

    print(f"Project structure created under '{base_dir}'")

# Execute the function
create_project_structure()
