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
                        env['PATH'] = orca_dir + os.pathsep + old_path
                    print('STEP: about to set input_dir and creationflags')
                    input_dir = os.path.dirname(os.path.abspath(job.input_path))
                    creationflags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                    
                    # Prepare ORCA command arguments
                    # Use full absolute paths for both ORCA executable and input file for parallel job support
                    orca_executable = os.path.abspath(job.orca_path)
                    input_file = os.path.abspath(job.input_path)
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
