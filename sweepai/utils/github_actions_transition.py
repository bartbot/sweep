import os
import re


def update_workflow_file(file_path):
    set_output_pattern = re.compile(r'echo "::set-output name=(\w+)::(.+)"')
    save_state_pattern = re.compile(r'echo "::save-state name=(\w+)::(.+)"')
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = set_output_pattern.sub(r'echo "\1=\2" >> $GITHUB_OUTPUT', content)
    content = save_state_pattern.sub(r'echo "\1=\2" >> $GITHUB_ENV', content)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
