from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QMenu, QDialog, QTextEdit, QVBoxLayout as QVBL
from PyQt6.QtGui import QAction, QTextCursor
from PyQt6.QtCore import Qt, QTimer, QPoint
from .job_queue import JobStatus
import os
import threading

class JobQueueTab(QWidget):
    def __init__(self, queue_manager, parent=None):
        super().__init__(parent)
        self.queue_manager = queue_manager
        self.layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "Input File", "Output File", "Status", "Submitted", "Started", "Finished", "Duration", "Actions"
        ])
        self.layout.addWidget(self.table)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._show_context_menu)
        self._open_monitors = []  # Hold references to open monitor dialogs
        self.refresh()

    def refresh(self):
        jobs = self.queue_manager.get_all_jobs()
        self.jobs = jobs  # Store for context menu access
        self.table.setRowCount(len(jobs))
        for row, job in enumerate(jobs):
            self.table.setItem(row, 0, QTableWidgetItem(job.input_path))
            self.table.setItem(row, 1, QTableWidgetItem(job.output_path))
            status_item = QTableWidgetItem(job.status.value)
            if job.status == JobStatus.RUNNING:
                status_item.setBackground(Qt.GlobalColor.yellow)
                status_item.setForeground(Qt.GlobalColor.black)
            elif job.status == JobStatus.QUEUED:
                status_item.setBackground(Qt.GlobalColor.cyan)
                status_item.setForeground(Qt.GlobalColor.black)
            elif job.status == JobStatus.DONE:
                status_item.setBackground(Qt.GlobalColor.green)
            elif job.status == JobStatus.ERROR:
                status_item.setBackground(Qt.GlobalColor.red)
            elif job.status == JobStatus.CANCELLED:
                status_item.setBackground(Qt.GlobalColor.gray)
            self.table.setItem(row, 2, status_item)
            self.table.setItem(row, 3, QTableWidgetItem(job.submitted_time or ""))
            self.table.setItem(row, 4, QTableWidgetItem(job.started_time or ""))
            self.table.setItem(row, 5, QTableWidgetItem(job.finished_time or ""))

            # Duration column
            duration_str = ""
            from datetime import datetime
            def parse_time(t):
                try:
                    return datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
                except Exception:
                    return None
            start = parse_time(job.started_time) if job.started_time else None
            end = parse_time(job.finished_time) if job.finished_time else None
            if job.status == JobStatus.DONE and start and end:
                duration = end - start
                duration_str = str(duration).split('.')[0]  # HH:MM:SS
            elif job.status == JobStatus.RUNNING and start:
                now = datetime.now()
                duration = now - start
                duration_str = str(duration).split('.')[0]
            self.table.setItem(row, 6, QTableWidgetItem(duration_str))

            # Actions: Cancel, Move Up, Move Down
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_widget = QWidget()
            if job.status in (JobStatus.QUEUED, JobStatus.RUNNING):
                cancel_btn = QPushButton("Cancel")
                cancel_btn.setMinimumWidth(60)
                cancel_btn.clicked.connect(lambda _, j=job: self._cancel_job(j))
                actions_layout.addWidget(cancel_btn)
            if job.status == JobStatus.QUEUED:
                up_btn = QPushButton("Up")
                down_btn = QPushButton("Down")
                up_btn.setMinimumWidth(38)
                down_btn.setMinimumWidth(38)
                up_btn.clicked.connect(lambda _, j=job, r=row: self._move_job(j, r-1))
                down_btn.clicked.connect(lambda _, j=job, r=row: self._move_job(j, r+1))
                actions_layout.addWidget(up_btn)
                actions_layout.addWidget(down_btn)
            actions_layout.addStretch()
            actions_widget.setLayout(actions_layout)
            actions_widget.setMinimumWidth(150)
            self.table.setCellWidget(row, 6, actions_widget)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def _cancel_job(self, job):
        ok = self.queue_manager.cancel_job(job)
        if not ok:
            QMessageBox.warning(self, "Cancel Failed", "Unable to cancel this job.")
        self.refresh()

    def _move_job(self, job, new_index):
        self.queue_manager.reorder_job(job, new_index)
        self.refresh()

    def _show_context_menu(self, pos: QPoint):
        index = self.table.indexAt(pos)
        row = index.row()
        if row < 0 or row >= len(self.jobs):
            return
        job = self.jobs[row]
        menu = QMenu(self)
        # Cancel
        if job.status in (JobStatus.QUEUED, JobStatus.RUNNING):
            cancel_action = QAction("Cancel Job", self)
            cancel_action.triggered.connect(lambda: self._cancel_job(job))
            menu.addAction(cancel_action)
        # Move Up
        if job.status == JobStatus.QUEUED and row > 0:
            up_action = QAction("Move Up", self)
            up_action.triggered.connect(lambda: self._move_job(job, row-1))
            menu.addAction(up_action)
        # Move Down
        if job.status == JobStatus.QUEUED and row < len(self.jobs)-1:
            down_action = QAction("Move Down", self)
            down_action.triggered.connect(lambda: self._move_job(job, row+1))
            menu.addAction(down_action)
        # Monitor Output File
        if job.output_path:
            monitor_action = QAction("Monitor Output File", self)
            monitor_action.triggered.connect(lambda: self._monitor_output_file(job))
            menu.addAction(monitor_action)
        menu.exec(self.table.viewport().mapToGlobal(pos))

    def _monitor_output_file(self, job):
        dialog = QDialog()
        dialog.setWindowFlag(Qt.WindowType.Window)
        dialog.setWindowTitle(f"Monitor Output: {os.path.basename(job.output_path)}")
        layout = QVBL(dialog)
        text_edit = QTextEdit(dialog)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        dialog.setLayout(layout)
        timer = QTimer(dialog)
        timer.setInterval(500)
        last_size = {'val': 0}  # Mutable holder
        def poll_file():
            try:
                if os.path.exists(job.output_path):
                    with open(job.output_path, 'r', encoding='utf-8', errors='ignore') as f:
                        if last_size['val'] == 0:
                            # Always show full file on first tick or if window is reopened
                            content = f.read()
                            text_edit.setPlainText(content)
                            last_size['val'] = f.tell()
                            text_edit.moveCursor(QTextCursor.MoveOperation.End)
                        else:
                            f.seek(last_size['val'])
                            new_data = f.read()
                            if new_data:
                                text_edit.moveCursor(QTextCursor.MoveOperation.End)
                                text_edit.insertPlainText(new_data)
                                text_edit.moveCursor(QTextCursor.MoveOperation.End)
                            last_size['val'] = f.tell()
                # Stop polling if job is done/error/cancelled
                if job.status not in (JobStatus.RUNNING, JobStatus.QUEUED):
                    timer.stop()
            except Exception:
                pass
        timer.timeout.connect(poll_file)
        # Always show file content on open
        try:
            if os.path.exists(job.output_path):
                with open(job.output_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    text_edit.setPlainText(content)
                    last_size['val'] = f.tell()
                    text_edit.moveCursor(QTextCursor.MoveOperation.End)
            else:
                text_edit.setPlainText(f"Output file does not exist:\n{job.output_path}\n\nCheck if the job has started, or if the output path is correct.")
        except Exception as e:
            text_edit.setPlainText(f"(Could not read output file)\n{job.output_path}\nError: {e}")
        if job.status in (JobStatus.RUNNING, JobStatus.QUEUED):
            timer.start()
        def on_close():
            timer.stop()
            try:
                self._open_monitors.remove(dialog)
            except ValueError:
                pass
        dialog.finished.connect(on_close)
        self._open_monitors.append(dialog)
        dialog.resize(800, 600)
        dialog.show()
