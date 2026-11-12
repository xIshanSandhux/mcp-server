# LeetCode MCP Architecture - V1

The project will use a lean Python modular monolith with a simple layered architecture and a service layer. It is intentionally smaller than a full hexagonal or enterprise architecture.

## Goals

- Provide useful, explainable problem recommendations.
- Keep planning logic independent from MCP, SQLite, and LeetCode-specific code.
- Submit a solution explicitly from the IDE or CLI.
- Record progress and submission history locally.
- Make the important behavior easy to test.
- Keep the project local and single-user for the first version.

## Non-goals for the first version

- A hosted multi-user service.
- A web dashboard.
- Automatic or background submissions.
- A general-purpose AI coding agent.
- Microservices or a distributed architecture.
- A large plugin system.

## Architecture

```text
Codex / IDE / CLI
        |
        v
MCP and CLI interfaces
        |
        v
Application services
        |
        +--> Planning logic and models
        |
        +--> LeetCode client
        |
        +--> SQLite database
        |
        +--> Workspace file reader
```

The interfaces translate external requests into calls to application services. The services coordinate workflows. Planning logic contains the recommendation rules. Integrations handle external systems.

## Project layout

```text
mcp-server/
├── pyproject.toml
├── ARCHITECTURE.md
├── src/
│   └── leetcode_mcp/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── models.py
│       ├── planning.py
│       ├── services.py
│       ├── leetcode_client.py
│       ├── database.py
│       ├── file_reader.py
│       ├── mcp_server.py
│       └── cli.py
└── tests/
    ├── unit/
    ├── integration/
    └── fixtures/
```

The package inside `src/` gives the application a stable Python namespace. It is not an additional architectural layer.

## Module responsibilities

### `models.py`

Defines the application's main data structures, such as:

- `Problem`
- `Submission`
- `UserProgress`
- `StudyPlan`
- recommendation results

Models should describe data and enforce basic validation. They should not make network calls or query the database.

### `planning.py`

Contains pure recommendation logic, including:

- topic-gap detection
- difficulty progression
- recent-attempt analysis
- candidate scoring
- recommendation explanations

This module should receive data and return decisions. It should not know about MCP, SQLite, or HTTP.

### `services.py`

Contains application workflows that coordinate multiple pieces of the system.

Examples:

- synchronize LeetCode progress
- recommend the next problems
- build a study plan
- submit the current solution
- retrieve submission status

Services answer: “How do we complete this workflow?” Planning logic answers: “What is the correct recommendation?”

### `leetcode_client.py`

Contains all LeetCode-specific integration code:

- authentication/session handling
- problem and submission requests
- response parsing
- submission polling
- timeout and retry behavior

LeetCode-specific details should stay in this module so they do not spread through the application.

### `database.py`

Owns local SQLite persistence, including:

- database initialization
- migrations
- queries
- saving and loading problems
- saving submissions and sync results

The first version can use direct database functions. Separate repository classes should only be introduced if the database code becomes difficult to maintain or test.

### `mcp_server.py`

Defines MCP tools, resources, and prompts. MCP handlers should remain thin:

```text
validate input -> call a service -> format the result
```

They should not contain recommendation rules or raw database queries.

### `cli.py`

Provides optional command-line and IDE-facing commands, including submission of the current file. The CLI should call the same services as the MCP interface rather than duplicating submission logic.

### `config.py`

Loads configuration such as:

- allowed workspace directories
- database path
- authentication settings
- logging level
- polling timeouts

Secrets should not be committed or written to logs.

### `main.py`

Starts the application and wires together configuration, database access, the LeetCode client, services, and the MCP server.

## Main workflows

### Planning workflow

```text
Codex calls an MCP planning tool
        |
        v
MCP validates the request
        |
        v
Planning service loads progress and candidates
        |
        v
Planning logic scores candidates
        |
        v
MCP returns problems and explanations
```

Recommendations should explain why a problem was selected, for example:

```text
This problem is recommended because you have not practiced BFS recently,
you solved two tree DFS problems, and its difficulty is a reasonable next step.
```

### Submission workflow

```text
IDE or CLI requests submission
        |
        v
Validate problem, language, and workspace path
        |
        v
Read and hash the source file
        |
        v
Submit through the LeetCode client
        |
        v
Poll with a timeout and bounded retries
        |
        v
Save the result in SQLite
        |
        v
Return Accepted, Wrong Answer, Runtime Error, or other result
```

Submission must be explicit. The server should not submit code merely because a recommendation was generated.

## MCP surface

Potential planning tools:

- `get_user_progress`
- `get_recent_submissions`
- `search_problems`
- `recommend_next_problems`
- `build_study_plan`
- `sync_progress`

Potential submission tools:

- `submit_current_file`
- `get_submission_status`

Potential resources:

- `leetcode://profile`
- `leetcode://progress`
- `leetcode://problem/{slug}`
- `leetcode://submissions/recent`
- `leetcode://study-plan/current`

## Testing strategy

### Unit tests

Test fast, isolated behavior:

- recommendation scoring
- topic-gap detection
- difficulty progression
- model validation
- duplicate-submission detection

### Integration tests

Test local components together:

- SQLite initialization and persistence
- migrations
- service workflows
- submission flow using a fake LeetCode client
- MCP input validation

### End-to-end tests

Use sparingly for the complete local flow:

```text
MCP or CLI -> service -> fake LeetCode client -> SQLite
```

Real LeetCode submissions should remain manual or explicitly opt-in tests.

## Safety and reliability rules

- Restrict file reads to configured workspace directories.
- Require explicit confirmation before submission.
- Do not log passwords, cookies, tokens, or source code.
- Use request timeouts and bounded retries.
- Hash submitted source to detect accidental duplicate submissions.
- Persist pending submissions before polling for the final result.
- Keep authentication isolated inside the LeetCode integration.

## Design principles

1. Keep the architecture small until the code gives a reason to expand it.
2. Keep planning logic independent and easy to test.
3. Keep LeetCode-specific behavior in one integration module.
4. Share application services between MCP and CLI/IDE interfaces.
5. Prefer simple functions and modules before introducing abstractions.
6. Add ports, repositories, background workers, or separate packages only when they solve a demonstrated problem.

## Summary

The project is a lean Python modular monolith with a layered architecture:

```text
MCP / CLI interfaces
    -> application services
    -> planning and models
    -> LeetCode / SQLite / filesystem integrations
```

This provides enough separation for testing and future growth without making a local personal tool unnecessarily complex.
