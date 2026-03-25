# Getting Started with TwinTrim

Welcome to the TwinTrim getting started guide! This document will walk you through the steps to get started with the project.

### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python Installation**: Make sure you have Python 3.6 or above installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).
- **Git**: Ensure you have Git installed to clone the repository. You can get it from the [official Git website](https://git-scm.com/downloads).
- **GitHub Account**: A GitHub account is required if you plan to contribute to the project.

### Installing TwinTrim

To install TwinTrim, follow these steps:

1. **Clone the Repository**: Clone the repository from GitHub to your local machine.

    ```bash
    git clone https://github.com/Kota-Karthik/twinTrim.git
    ```

2. **Navigate to the Project Directory**: Change into the project directory.

    ```bash
    cd twinTrim
    ```

3. **Install Dependencies**: Install the required dependencies using the following command. If you are using `poetry`, you can install dependencies with:

    ```bash
    poetry install
    ```

    Alternatively, if you are using `pip`, install the dependencies from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

### Running TwinTrim

To run TwinTrim, follow these steps:

1. **Navigate to the Project Directory** (if not already there):

    ```bash
    cd twinTrim
    ```

2. **Run the Application**: Start the application with the following command:

    ```bash
    python -m twinTrim.main <directory> [OPTIONS]
    ```

    Replace `<directory>` with the path to the directory you want to scan. You can add options such as `--all` to automatically remove duplicates or specify filters (e.g., `--min-size` or `--file-type`).

    The application will scan the directory and, based on your options, either prompt you to review the duplicates or automatically remove them.

### Contributing to TwinTrim

We welcome contributions! Follow these steps to contribute:

1. **Fork the Repository**: Fork the repository on GitHub from [here](https://github.com/Kota-Karthik/twinTrim/fork).

2. **Clone Your Fork**: Clone the forked repository to your local machine.

    ```bash
    git clone https://github.com/<your-username>/twinTrim.git
    ```

3. **Create a New Branch**: Create a new branch to work on your changes.

    ```bash
    git checkout -b new-branch-name
    ```

4. **Make Changes**: Make the necessary changes to the code.

5. **Commit Changes**: Commit your changes with a descriptive message.

    ```bash
    git commit -m "Descriptive commit message"
    ```

6. **Push Changes**: Push your changes to your fork on GitHub.

    ```bash
    git push origin new-branch-name
    ```

7. **Create a Pull Request**: Go to the GitHub repository and create a pull request from your fork's branch to the main repository's `main` branch.

Your changes will be reviewed, and if everything looks good, they will be merged into the main project.

### Contact

If you have any questions or need further assistance, feel free to reach out to [Karthik Kota](https://www.linkedin.com/in/kota-karthikk/).
