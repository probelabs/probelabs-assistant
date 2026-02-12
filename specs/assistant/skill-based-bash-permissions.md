# Spec: Skill-Based Bash Command Permissions

## 1. Problem

The assistant's `bash` tool currently uses a single, global configuration for allowed and disallowed commands. This is inflexible, as different skills may require different sets of commands to function correctly. A skill that needs to interact with `git` should be able to enable it without enabling it for all other skills.

## 2. Proposal

We will extend the skill definition schema in `config/skills.yaml` to include two new optional fields: `allowed_commands` and `disallowed_commands`. This will allow each skill to declare the specific bash commands it requires. The system will dynamically compute the final set of permissions at runtime based on the active skills for the current request.

## 3. User Stories

- **As a Skill Developer,** I want to specify the exact bash commands my skill needs so that I can ensure it has the necessary permissions without granting overly broad access.
- **As an Assistant Administrator,** I want to ensure that skills can only run pre-approved commands to maintain a secure execution environment.
- **As an Assistant Administrator,** I want a global deny list that cannot be overridden by any skill to enforce baseline security policies.

## 4. Acceptance Criteria

1.  **Given** a skill is active and defines `allowed_commands: ['my-custom-command *']`, **when** the assistant tries to run `my-custom-command --version`, **then** the command is executed successfully.
2.  **Given** a skill is active and defines `disallowed_commands: ['git push *']`, **when** the assistant tries to run `git push origin main`, **then** the command is rejected with a permission error.
3.  **Given** a skill defines `allowed_commands: ['sudo *']` and the global deny list contains `sudo`, **when** the assistant tries to run `sudo ls`, **then** the command is rejected due to the global deny rule's precedence.
4.  **Given** one active skill defines `allowed_commands: ['curl *']` and another active skill defines `disallowed_commands: ['curl *']`, **when** the assistant tries to run `curl example.com`, **then** the command is rejected due to the skill-level deny rule's precedence.
5.  **Given** an active skill defines `allowed_commands: ['ls *']`, **when** the assistant tries to run a command not on any allow list (e.g., `grep 'foo' bar.txt`), **then** the command is rejected.
6.  **Given** Skill A allows `git log *` and Skill B allows `npm install`, **when** both skills are active, **then** both `git log` and `npm install` commands are allowed.
7.  **Given** no skills with command permissions are active, **when** the assistant runs a bash command, **then** only the global allow/deny lists are used for validation.

## 5. Technical Notes

### Configuration Schema

Two new optional fields will be added to the skill definition:

- `allowed_commands`: A list of strings representing commands that the skill needs to execute. Wildcards (`*`) are supported (e.g., `git *`, `npm run *`).
- `disallowed_commands`: A list of strings representing commands that should be explicitly forbidden when this skill is active.

*Example `config/skills.yaml` entry:*
```yaml
- id: git-contributor-skill
  description: a skill for finding git contributors
  allowed_commands:
    - 'git log *'
    - 'git shortlog *'
  disallowed_commands:
    - 'git push *'
```

### Precedence and Execution Logic

Command permissions will be evaluated in the following order. The first rule that matches determines the outcome:

1.  **Global Deny List (Final)**: Checked against the system-wide, hardcoded deny list. If it matches, it is **REJECTED**. This cannot be overridden.
2.  **Skill-Level Disallow**: Checked against the `disallowed_commands` from all *active* skills. If it matches, it is **REJECTED**.
3.  **Skill-Level Allow**: Checked against the `allowed_commands` from all *active* skills. If it matches, it is **ALLOWED**.
4.  **Global Allow List**: Checked against the default system-wide allowed commands. If it matches, it is **ALLOWED**.
5.  **Default**: If no rule matches, the command is **REJECTED**.

## 6. Out of Scope

- This feature does not cover permissions for tools other than `bash`.
- Dynamic loading of skills during a session is not included. Permissions are calculated at the start of the request.
