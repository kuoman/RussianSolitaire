# Russian Solitaire Project

Python implementation of Russian Solitaire card game.

## Development Approach

### Test-Driven Development
- **Spec-driven**: All features specified before implementation
- **Test-first**: Write tests before production code
- **Characterization tests**: Used to validate and document functionality
- Both test types written in **fluent style syntax**

### Object-Oriented Design
- **Smalltalk-inspired OOP**: Strong object model with message passing
- **SOLID principles**: 
  - Single Responsibility Principle
  - Open/Closed Principle
  - Liskov Substitution Principle
  - Interface Segregation Principle
  - Dependency Inversion Principle
- **XP (Extreme Programming) principles**:
  - Simple design
  - Refactoring
  - Pair programming mindset (human + AI)
  - Continuous testing

### Architecture
- Text-based prototype interface
- Data persistence in `./data` folder
- Clean separation of concerns
- Message-passing between objects

## Project Structure

```
/
├── docs/           # Documentation
│   ├── rules.md    # Game rules
│   └── gameplay.md # Gameplay explanation
├── data/           # Persisted game data
└── src/            # Source code (TBD)
```

## Testing Philosophy

- Tests express intent clearly through fluent syntax
- Characterization tests document existing behavior
- Test-first tests drive new functionality
- Tests are first-class citizens - modify with permission only

## Code Style

- Small, focused classes with single responsibilities
- Objects tell, don't ask
- Favor composition over inheritance
- Immutability where appropriate
- Clear, intention-revealing names

## Commit Workflow

- **Micro commits**: Commit small, atomic changes frequently
- **Arlo Belshee's commit notation**: Use strict Arlo notation — single character prefix, no colon:
  - `t` — test only, no production code changed
  - `r` — refactor, provably safe (behaviour unchanged, passes before and after)
  - `R` — refactor, higher risk (touching production logic)
  - `F` — new feature (production code, new behaviour)
  - `b` — bug fix
  - `d` — documentation only
  - Uppercase = higher risk; lowercase = safe/mechanical
- **Committer skill**: Always use the committer skill when creating commits (invoked via `c` or `/commit`)
- Commits should be small enough to easily understand and revert if needed

## Branching Strategy

- **Trunk-based development**: `main` is the integration branch — all work lands here
- **Short-lived branches only**: Subagents may create feature branches for isolation during TDD/test-first work, but these must be merged back to `main` before the task is considered done
- **No long-lived branches**: A task is not complete until its code is on `main`
- Single developer — no PRs required, direct merge to main is the norm
