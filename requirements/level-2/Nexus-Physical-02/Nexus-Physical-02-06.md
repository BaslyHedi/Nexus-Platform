# Nexus-Physical-02-06 - Test applications

Software element, level 2, handed over: the repository in the [configuration table](../../level-0/Nexus-Enabling.md) derives its own software requirements from these and cites their IDs. Written to [../system/method.md](../../../system/method.md) and [rules.md](../../rules.md).

- **Purpose and boundary.** Two throwaway programs that print their name and version, proving the repository, CI and image chain (T2.1).
- **Interfaces.** Carried by the Linux image [02-03](Nexus-Physical-02-03.md).
- **Allocated functions.** 503 F4.
- **Modes.** Running.

## Requirements

### Nexus-Physical-02-06-R001

**Statement.** When started, each test application shall print the name and the version of the test application.

- Function: Nexus-Logical-503-F04
- Derived-from: Nexus-Physical-02-R009
- Allocated-to: -
- Phase: 1
- Verification: Test T2.1
- Realised-by: SW
