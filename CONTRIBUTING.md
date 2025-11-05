# Contributing to `TRIPs`

## Types of Contributions

You can contribute in many ways:

### Report Bugs

Report bugs at [gitlab.com/jeremy.zucker/TRIPs/-/issues][issues].

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the project's issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to implement a fix for it.

### Implement Features

Look through the project's issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.

### Write Documentation

You can contribute to the official docs, in docstrings, or even on the web in blog posts and articles.

### Submit Feedback

The best way to send feedback is to file an issue at [gitlab.com/jeremy.zucker/TRIPs/-/issues][issues].

If you are proposing a new feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome.

## Get Started

Here's how to set up `TRIPs` for local development. Please note this documentation assumes you already have `git`, [`uv`](https://docs.astral.sh/uv/getting-started/installation/) and [Task](https://taskfile.dev/installation/) installed and ready to go.

**Note**: You can technically use Task as a tool from `uv` (this is what is done in the `.gitlab-ci.yml` file). A command like `task --list` can be translated to `uvx --from go-task-bin task --list`. So in all instructions below you can replace `task` with `uvx --from go-task-bin task`. Installing Task directly on your system just makes it simpler to use.

To see all available tasks, run:

```bash
task
```

To see more information about a specific task, run:

```bash
task <task-name> --summary
```

### Step 1. Fork

[Fork][fork] the `TRIPs` repository.

### Step 2. Clone

Clone your fork locally:

```bash
cd <directory_in_which_repo_should_be_created>
git clone git@gitlab.com:<your-namespace>/TRIPs.git
```

### Step 3. Install

Now you need to install the environment. Navigate into the directory

```bash
cd TRIPs
```

Then, sync the environment and the pre-commit hooks by running:

```bash
task install
```

### Step 4. New branch

Create a branch for local development:

```bash
git checkout -b <name-of-your-bugfix-or-feature>
```

Now you can make your changes locally.

### Step 5. Add tests

Don't forget to add test cases for your added functionality to the `tests` directory.

### Step 6. Check formatting

When you're done making changes, check that your changes pass the formatting tests.

```bash
task check
```

### Step 7. Validate tests

Now, validate that all unit tests are passing:

```bash
task test
```

### Step 8. Document your changes

Reflect your changes in the documentation. Update relevant files in the `docs` directory, and potentially the `README`. You can check the updated documentation with:

```bash
task docs-serve
```

### Step 9. Commit and push

Commit your changes and push your branch to the remote:

```bash
git add <your-files>
git commit -m "Your detailed description of your changes."
git push origin <name-of-your-bugfix-or-feature>
```

### Step 10. Merge

Submit a [merge request][merge].

[issues]: https://gitlab.com/jeremy.zucker/TRIPs/-/issues
[fork]: https://gitlab.com/jeremy.zucker/TRIPs/-/forks/new
[merge]: https://gitlab.com/jeremy.zucker/TRIPs/-/merge_requests
