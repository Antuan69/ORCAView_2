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
    def __init__(self, input_path, output_path, bat_path, orca_path=None):
        self.input_path = input_path
        self.output_path = output_path
        self.bat_path = bat_path
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
                        orca_dir = os.path.dirname(job.orca_path)
                        old_path = env.get('PATH', '')
                        env['PATH'] = orca_dir + os.pathsep + old_path
                    print('STEP: about to set input_dir and creationflags')
                    input_dir = os.path.dirname(job.input_path) or os.getcwd()
                    creationflags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
                    print('ABOUT TO LAUNCH BATCH:', job.bat_path)
                    print('STEP: checking platform')
                    if sys.platform == "win32":
                        print('USING SHELL=TRUE FOR WINDOWS')
                        job.process = subprocess.Popen(
                            job.bat_path,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            env=env,
                            cwd=input_dir,
                            creationflags=creationflags,
                            shell=True
                        )
                    else:
                        job.process = subprocess.Popen(
                            [job.bat_path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            env=env,
                            cwd=input_dir
                        )
                    print('BATCH LAUNCHED, WAITING FOR COMPLETION')
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
                        stdout, stderr = job.process.communicate()
                        print('BATCH FINISHED. RETURN CODE:', job.process.returncode)
                        print('BATCH STDOUT:')
                        print(stdout)
                        print('BATCH STDERR:')
                        print(stderr)
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
