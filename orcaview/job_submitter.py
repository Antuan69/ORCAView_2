import os

class JobSubmitter:
    """
    A class to handle job submission.
    """
    def __init__(self, orca_path="path/to/orca.exe"):
        self.orca_path = orca_path

    def create_submission_script(self, job_name, input_file_path):
        """
        Create a simple submission script for Windows.
        """
        script_content = f'"""{self.orca_path}""" "{input_file_path}" > "{job_name}.out"'
        
        script_path = os.path.join(os.path.dirname(input_file_path), f"{job_name}.bat")
        
        with open(script_path, "w") as f:
            f.write(script_content)
            
        return script_path
