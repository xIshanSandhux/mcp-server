# LeetCode MCP Architecture - V1

This project is a local LeetCode MCP server for two workflows:

1. Context: provide Codex with accurate progress, submission, and problem data so it can decide what to solve next.
2. Submission: submit the current solution from the IDE or command line and record the result.

The project will use a lean Python modular monolith with a simple layered architecture and a service layer. It is intentionally smaller than a full hexagonal or enterprise architecture.
The MCP server will not contain an AI recommendation engine; Codex owns the reasoning and study planning.

## Goals

- Provide accurate, useful learning context to Codex.
- Keep data collection and context-building independent from MCP, SQLite, and LeetCode-specific code.
- Submit a solution explicitly from the IDE or CLI.
- Record progress and submission history locally.
- Make the important behavior easy to test.
- Keep the project local and single-user for the first version.

## Non-goals for the first version

- A hosted multi-user service.
- A web dashboard.
- Automatic or background submissions.
- A general-purpose AI coding agent.
- Server-side AI recommendation or study-plan generation.
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
        +--> Context building and models
        |
        +--> LeetCode client
        |
        +--> SQLite database
        |
        +--> Workspace file reader
```

The interfaces translate external requests into calls to application services. The services coordinate workflows. Context building summarizes facts for Codex. Integrations handle external systems.

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
│       ├── context.py
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
- `LearningContext`
- filtered candidate results

Models should describe data and enforce basic validation. They should not make network calls or query the database.

### `context.py`

Builds structured learning context for Codex, including:

- solved and unsolved problems
- recent submissions and failures
- topic counts and activity
- difficulty distribution
- filtered candidate problems
- user preferences and constraints

This module summarizes facts and applies practical filters. It should not choose the next problem, generate a study plan, or make subjective recommendations. It should not know about MCP, SQLite, or HTTP.

### `services.py`

Contains application workflows that coordinate multiple pieces of the system.

Examples:

- synchronize LeetCode progress
- build learning context for Codex
- search and filter problems
- submit the current solution
- retrieve submission status

Services answer: “How do we complete this workflow?” Codex answers: “What should I solve next and why?”

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

### Context workflow

```text
Codex calls an MCP context tool
        |
        v
MCP validates the request
        |
        v
Context service loads progress, submissions, and candidates
        |
        v
MCP returns structured facts to Codex
```

The server should return facts that allow Codex to reason, for example:

```text
You have solved 42 problems. Your recent topics were arrays and trees.
You have not practiced graphs recently. Your recent medium-problem success
rate is 60%. These 20 unsolved problems match the selected filters.
```

Codex then decides which problem to recommend and explains why.

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

Potential context tools:

- `get_learning_context`
- `get_progress`
- `get_recent_submissions`
- `search_problems`
- `get_candidate_problems`
- `sync_progress`

Potential submission tools:

- `submit_current_file`
- `get_submission_status`

Potential resources:

- `leetcode://profile`
- `leetcode://progress`
- `leetcode://problem/{slug}`
- `leetcode://submissions/recent`

## Testing strategy

### Unit tests

Test fast, isolated behavior:

- context aggregation
- problem filtering
- progress statistics
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
2. Let Codex own recommendations and study planning.
3. Keep context building factual, deterministic, and easy to test.
4. Keep LeetCode-specific behavior in one integration module.
5. Share application services between MCP and CLI/IDE interfaces.
6. Prefer simple functions and modules before introducing abstractions.
7. Add ports, repositories, background workers, or separate packages only when they solve a demonstrated problem.

## Summary

The project is a lean Python modular monolith with a layered architecture:

```text
MCP / CLI interfaces
    -> application services
    -> context and models
    -> LeetCode / SQLite / filesystem integrations
```

The MCP server provides data, context, and actions. Codex provides the recommendations, explanations, and study plans. This provides enough separation for testing and future growth without making a local personal tool unnecessarily complex.
