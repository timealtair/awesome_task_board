# 📋 Task Board Manager

A lightweight command-line task board application for managing your tasks and workflows efficiently.

![Demo](/utils/media/demo.mp4)

## 🌟 Overview

Task Board Manager is a simple yet powerful Python-based task management tool that helps you organize your work. Create boards, add tasks, and track their progress through customizable status workflows - all from your terminal.

## ✨ Features

- 📊 **Multiple Task Boards** - Create and manage separate boards for different projects
- ✅ **Task Management** - Easily add, modify, and delete tasks
- 🔄 **Status Tracking** - Track task progress through customizable status workflows
- ⚙️ **Configurable** - Customize default task statuses to match your workflow
- 🚀 **Fast & Lightweight** - Built with modern Python tooling using [uv](https://docs.astral.sh/uv/)

## 📋 Prerequisites

- [uv](https://docs.astral.sh/uv/) - Modern Python package manager (handles Python installation automatically)

### Installing uv

```sh
# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 🚀 Getting Started

### Create a Task Board

Initialize a new task board to start organizing your work. This sets up the workspace where all your tasks will be stored.

```sh
uv run create_task_board.py
```

### Add Tasks

Create new tasks on your board. You'll be prompted to enter task details such as title and initial status.

```sh
uv run add_new_task.py
```

### Manage Tasks

Update existing tasks by changing their status (e.g., from "Todo" to "In Progress") or remove completed/obsolete tasks from your board.

```sh
uv run modify_tasks.py
```

## ⚙️ Configuration

### Customize Default Task Statuses

Tailor the available task statuses to match your workflow. Edit the configuration file with your preferred text editor:

```sh
# Using your preferred editor
$EDITOR settings/default_status_set.py

# Examples:
nano settings/default_status_set.py
vim settings/default_status_set.py
code settings/default_status_set.py
```

Common status workflows you might configure:
- **Simple**: `Todo → Done`
- **Standard**: `Backlog → In Progress → Done`
- **Advanced**: `Backlog → Todo → In Progress → Review → Done`

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## 📄 License

This project is licensed under the terms of the [LICENSE](/LICENSE) file.

## 🙏 Acknowledgments

- Built with [uv](https://docs.astral.sh/uv/) - An extremely fast Python package installer and resolver

---

**Happy Task Managing! 🎯**
