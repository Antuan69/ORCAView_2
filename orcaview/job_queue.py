import threading
import time
from enum import Enum
from collections import deque
import logging
import sys
import traceback
logging.basicConfig(level=logging.INFO, force=True)

class JobStatus(Enum):
    QUEUED = 'Queued'
    RUNNING = 'Running'
    DONE = 'Done'
    ERROR = 'Error'
    CANCELLED = 'Cancelled'

class OrcaJob:
    def __init__(self, input_path, output_path, orca_path=None):
        self.input_path = input_path
        self.output_path = output_path
        self.orca_path = orca_path
        self.status = JobStatus.QUEUED
        self.submitted_time = time.strftime('%Y-%m-%d %H:%M:%S')
        self.started_time = None
        self.finished_time = None
        self.error_msg = None
        self.process = None

class JobQueueManager:
    def __init__(self, on_update_callback=None):
        self.queue = deque()
        self.running_job = None
        self.completed_jobs = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self._should_stop = False
        self.on_update_callback = on_update_callback
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def add_job(self, job):
        with self.condition:
            self.queue.append(job)
            self.condition.notify()
        print('JOB ADDED:', job.input_path)
        self._trigger_update()

    def cancel_job(self, job):
        with self.lock:
            if job.status == JobStatus.QUEUED:
                self.queue.remove(job)
                job.status = JobStatus.CANCELLED
                self.completed_jobs.append(job)
                self._trigger_update()
                return True
            elif job.status == JobStatus.RUNNING:
                # Instead of terminating here (which can deadlock GUI), set a cancel flag
                job._cancel_requested = True
                return True
        return False

    def reorder_job(self, job, new_index):
        with self.lock:
            if job in self.queue:
                self.queue.remove(job)
                self.queue.insert(new_index, job)
        self._trigger_update()

    def remove_completed_job(self, job):
        """Remove a completed job from the completed jobs list."""
        with self.lock:
            if job in self.completed_jobs and job.status in (JobStatus.DONE, JobStatus.ERROR, JobStatus.CANCELLED):
                self.completed_jobs.remove(job)
                self._trigger_update()
                return True
        return False

    def remove_all_finished_jobs(self):
        """Remove all finished jobs (DONE, ERROR, CANCELLED) from the completed jobs list."""
        with self.lock:
            finished_jobs = [job for job in self.completed_jobs if job.status in (JobStatus.DONE, JobStatus.ERROR, JobStatus.CANCELLED)]
            for job in finished_jobs:
                self.completed_jobs.remove(job)
            self._trigger_update()
            return len(finished_jobs)

    def _worker(self):
        import threading
        while not self._should_stop:
            with self.condition:
                while self.running_job is not None or not self.queue:
                    self.condition.wait(timeout=0.5)
                    if self._should_stop:
                        return
                job = self.queue.popleft()
                print('DEQUEUED JOB:', job.input_path)
                self.running_job = job
                job.status = JobStatus.RUNNING
                job.started_time = time.strftime('%Y-%m-%d %H:%M:%S')
                print('SET JOB TO RUNNING:', job.input_path)
                self._trigger_update()  # Update UI when job starts running
            if job:
                try:
                    print('STEP: about to import subprocess and os')
                    import subprocess
                    import os
                    print('STEP: about to set up env')
                    env = os.environ.copy()
                    if job.orca_path:
                        orca_dir = os.path.dirname(os.path.abspath(job.orca_path))
                        old_path = env.get('PATH', '')
                        # Add ORCA directory to PATH for MPI and other dependencies
                        env['PATH'] = orca_dir + os.pathsep + old_path
                        
                        # Set ORCA-specific environment variables for better compatibility
                        env['RSH_COMMAND'] = 'ssh'  # For remote shell if needed
                        env['ORCA_EXE_DIR'] = orca_dir  # ORCA executable directory
                        
                        # Check MPI availability with improved detection
                        mpi_available = False
                        try:
                            # Try multiple MPI detection methods
                            print('Testing MPI availability...')
                            
                            # Method 1: Check mpiexec with help flag (more compatible than --version)
                            result = subprocess.run(['mpiexec', '-help'], 
                                                   capture_output=True, timeout=10, env=env, text=True)
                            print(f'mpiexec -help exit code: {result.returncode}')
                            print(f'mpiexec stdout: {result.stdout[:200]}...' if result.stdout else 'No stdout')
                            
                            # Consider MPI available if mpiexec responds (even with non-zero exit code)
                            mpi_available = True
                            print('MPI available - parallel execution enabled')
                            
                        except FileNotFoundError:
                            print('mpiexec not found in PATH - trying alternative detection')
                            
                            # Method 2: Check for common MPI installations
                            mpi_paths = [
                                'mpiexec.exe',
                                r'C:\Program Files\Microsoft MPI\Bin\mpiexec.exe',
                                r'C:\Program Files (x86)\Microsoft MPI\Bin\mpiexec.exe',
                                r'C:\Program Files\Intel\MPI\*\bin\mpiexec.exe'
                            ]
                            
                            for mpi_path in mpi_paths:
                                if '*' in mpi_path:
                                    # Handle wildcard paths
                                    import glob
                                    matches = glob.glob(mpi_path)
                                    if matches:
                                        print(f'Found MPI at: {matches[0]}')
                                        mpi_available = True
                                        # Add MPI directory to PATH
                                        mpi_dir = os.path.dirname(matches[0])
                                        env['PATH'] = mpi_dir + os.pathsep + env['PATH']
                                        break
                                else:
                                    import os
                                    if os.path.exists(mpi_path):
                                        print(f'Found MPI at: {mpi_path}')
                                        mpi_available = True
                                        # Add MPI directory to PATH
                                        mpi_dir = os.path.dirname(mpi_path)
                                        env['PATH'] = mpi_dir + os.pathsep + env['PATH']
                                        break
                            
                            if not mpi_available:
                                print('No MPI installation detected')
                                
                        except subprocess.TimeoutExpired:
                            print('mpiexec command timed out - assuming MPI is available but slow')
                            mpi_available = True
                            
                        except Exception as e:
                            print(f'MPI detection error: {e} - assuming MPI is available')
                            mpi_available = True
                        
                        # Only force serial execution if MPI is definitely not available
                        if not mpi_available:
                            print('MPI not available - forcing serial execution')
                            # Force ORCA to run in serial mode by setting nprocs to 1
                            env['ORCA_NPROCS'] = '1'
                            env['ORCA_MPI_PROCS'] = '1'
                            # Disable OpenMPI warnings about missing components
                            env['OMPI_MCA_btl_base_warn_component_unused'] = '0'
                            env['OMPI_MCA_mpi_warn_on_fork'] = '0'
                        else:
                            print('MPI detected - allowing parallel execution')
                    print('STEP: about to set input_dir and creationflags')
                    input_dir = os.path.dirname(os.path.abspath(job.input_path))
                    creationflags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                    
                    # Prepare ORCA command arguments
                    # Use full absolute paths for both ORCA executable and input file for parallel job support
                    orca_executable = os.path.abspath(job.orca_path)
                    input_file = os.path.abspath(job.input_path)
                    
                    # Only modify input file if MPI is not available
                    if env.get('ORCA_NPROCS') == '1':
                        print('Modifying input file for serial execution')
                        try:
                            # Read the input file
                            with open(input_file, 'r') as f:
                                input_content = f.read()
                            
                            # Check if %pal block exists and modify it
                            lines = input_content.split('\n')
                            modified_lines = []
                            in_pal_block = False
                            pal_block_modified = False
                            
                            for line in lines:
                                line_stripped = line.strip().lower()
                                if line_stripped.startswith('%pal'):
                                    in_pal_block = True
                                    modified_lines.append(line)
                                elif in_pal_block and line_stripped == 'end':
                                    in_pal_block = False
                                    if not pal_block_modified:
                                        # Add nprocs 1 before end
                                        modified_lines.append('   nprocs 1')
                                        pal_block_modified = True
                                    modified_lines.append(line)
                                elif in_pal_block and 'nprocs' in line_stripped:
                                    # Replace existing nprocs with 1
                                    modified_lines.append('   nprocs 1')
                                    pal_block_modified = True
                                else:
                                    modified_lines.append(line)
                            
                            # If no %pal block exists, add one
                            if not pal_block_modified:
                                # Find the first line that doesn't start with ! or #
                                insert_index = 0
                                for i, line in enumerate(modified_lines):
                                    if not line.strip().startswith(('!', '#', '%')):
                                        insert_index = i
                                        break
                                
                                # Insert %pal block
                                modified_lines.insert(insert_index, '%pal')
                                modified_lines.insert(insert_index + 1, '   nprocs 1')
                                modified_lines.insert(insert_index + 2, 'end')
                                modified_lines.insert(insert_index + 3, '')
                            
                            # Write back the modified content
                            with open(input_file, 'w') as f:
                                f.write('\n'.join(modified_lines))
                            
                            print('Input file modified for serial execution')
                        except Exception as e:
                            print(f'Warning: Could not modify input file for serial execution: {e}')
                    else:
                        print('MPI available - preserving original input file for parallel execution')
                    
                    orca_cmd = [orca_executable, input_file]
                    
                    print('ABOUT TO LAUNCH ORCA DIRECTLY:', orca_cmd)
                    print('WORKING DIRECTORY:', input_dir)
                    
                    # Open output file for writing
                    with open(job.output_path, 'w') as output_file:
                        job.process = subprocess.Popen(
                            orca_cmd,
                            stdout=output_file,
                            stderr=subprocess.STDOUT,  # Redirect stderr to stdout (output file)
                            text=True,
                            env=env,
                            cwd=input_dir,
                            creationflags=creationflags if sys.platform == "win32" else 0
                        )
                    print('ORCA LAUNCHED, WAITING FOR COMPLETION')
                    while True:
                        # Check for cancellation
                        if getattr(job, '_cancel_requested', False):
                            if job.process and job.process.poll() is None:
                                print('TERMINATING PROCESS FOR CANCEL:', job.input_path)
                                try:
                                    if sys.platform == 'win32':
                                        import subprocess
                                        print(f'Attempting to taskkill PID tree: {job.process.pid}')
                                        subprocess.run(['taskkill', '/T', '/F', '/PID', str(job.process.pid)], check=False)
                                    else:
                                        job.process.terminate()
                                except Exception as te:
                                    print('EXCEPTION DURING TERMINATE:', te)
                                job.status = JobStatus.CANCELLED
                                job.finished_time = time.strftime('%Y-%m-%d %H:%M:%S')
                                print('JOB CANCELLED:', job.input_path)
                                self._trigger_update()  # Update UI when job is cancelled
                                break
                        if job.process.poll() is not None:
                            break
                        time.sleep(0.2)
                    if job.status != JobStatus.CANCELLED:
                        job.process.wait()  # Ensure process is fully finished
                        print('ORCA FINISHED. RETURN CODE:', job.process.returncode)
                        print('OUTPUT WRITTEN TO:', job.output_path)
                        if job.process.returncode == 0:
                            job.status = JobStatus.DONE
                            job.finished_time = time.strftime('%Y-%m-%d %H:%M:%S')
                            print('JOB FINISHED SUCCESSFULLY:', job.input_path)
                        else:
                            # Check output file for normal ORCA termination
                            output_ok = False
                            try:
                                if job.output_path and os.path.isfile(job.output_path):
                                    with open(job.output_path, 'r', encoding='utf-8', errors='ignore') as f:
                                        for line in f:
                                            if 'ORCA TERMINATED NORMALLY' in line:
                                                output_ok = True
                                                break
                            except Exception as file_err:
                                print('ERROR READING OUTPUT FILE:', file_err)
                            if output_ok:
                                job.status = JobStatus.DONE
                                job.finished_time = time.strftime('%Y-%m-%d %H:%M:%S')
                                print('JOB FINISHED SUCCESSFULLY (output file check):', job.input_path)
                            else:
                                job.status = JobStatus.ERROR
                                job.error_msg = f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
                                job.finished_time = time.strftime('%Y-%m-%d %H:%M:%S')
                                print('JOB FAILED:', job.input_path, 'STDOUT:', stdout, 'STDERR:', stderr)
                except Exception as e:
                    print('EXCEPTION IN WORKER FOR JOB:', job.input_path if job else None, e)
                    traceback.print_exc()
                    job.status = JobStatus.ERROR
                    job.error_msg = str(e)
                    job.finished_time = time.strftime('%Y-%m-%d %H:%M:%S')
                with self.lock:
                    self.completed_jobs.append(job)
                    self.running_job = None
                    print('JOB MOVED TO COMPLETED:', job.input_path)
                    # Trigger UI update when job completes
                    self._trigger_update()
                    # Also notify condition to wake up worker for next job
                    self.condition.notify()
            time.sleep(0.5)

    def stop(self):
        self._should_stop = True
        self.worker_thread.join()

    def _trigger_update(self):
        # Always schedule the UI update in the main thread
        try:
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(0, self.on_update_callback)
        except Exception:
            # fallback for non-GUI/early init
            if self.on_update_callback:
                self.on_update_callback()

    def get_all_jobs(self):
        with self.lock:
            all_jobs = list(self.queue)
            if self.running_job:
                all_jobs = [self.running_job] + all_jobs
            all_jobs += self.completed_jobs
        return all_jobs
