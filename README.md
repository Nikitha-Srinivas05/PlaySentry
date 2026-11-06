# PlaySentry

**Security monitoring platform for multiplayer game servers.**

PlaySentry collects logs and network events from a game server, detects cheating and attacks, groups related alerts into single incidents, and shows everything on a secured dashboard. Think of it as a small SIEM built specifically for game servers.

> **Status:**  In development.

---

## Why this project?

Game servers are frequent targets: DDoS floods, credential stuffing for account theft, port scans, and cheaters sending impossible actions. Most small server owners have no security monitoring, and enterprise SIEMs are too heavy for them. PlaySentry is a lightweight alternative, and a way to learn how detection systems work end to end.

## Features

- **Event ingestion API** with API-key auth, rate limiting, input validation and versioning (`/v1/events`)
- **Detection engine** with testable rules:
  - Security: brute force, port scan, connection flood, beaconing
  - Game-specific: impossible movement, abnormal action rate, impossible inventory changes
- **Alert correlation:** links weak signals into one incident (for example scan → brute force → login → item transfer = account theft), tagged with MITRE ATT&CK techniques
- **Dashboard** with JWT login, admin/analyst roles, live incidents, attacker IPs and event timelines
- **Simulators:** a small game server plus cheat bots and attack scripts to test every rule
- **PCAP support:** parse captured traffic as an additional event source
- **Privacy by design:** no passwords or tokens in logs, hashed identifiers, automatic data retention limit

## Architecture

```
 Game server + simulators ──► Ingestion API (FastAPI) ──► PostgreSQL
                                      │                      │
                                      ▼                      ▼
                              Detection engine ──► Correlation layer
                                                         │
                                                         ▼
                                              Dashboard (React)
```

## Tech stack

| Layer | Technology |
|---|---|
| Backend / API | Python, FastAPI, Pydantic |
| Database | PostgreSQL, SQLAlchemy |
| Frontend | React (Vite) |
| Auth | JWT, password hashing, role-based access |
| Networking | Scapy (PCAP parsing) |
| Testing | pytest, attack simulation scripts |
| DevOps | Docker, Docker Compose, GitHub Actions |

## Getting started

**Requirements:** Docker and Docker Compose.

```bash
git clone https://github.com/Nikitha-Srinivas05/playsentry.git
cd playsentry
cp .env.example .env     # then set your own values
docker compose up --build
```

- API health check: http://localhost:8000/health
- Interactive API docs: http://localhost:8000/docs

## Project structure

```
playsentry/
├── backend/          # FastAPI app, detection engine
├── dashboard/        # React dashboard
├── simulators/       # Game server, cheat bots, attack scripts
├── docs/             # Architecture diagram, threat model
├── docker-compose.yml
└── .env.example
```

## Security and privacy

- Passwords and tokens are never logged
- IPs and usernames can be stored hashed or truncated where a rule doesn't need the original
- Raw events are deleted after a configurable retention period
- Role-based access: only admins can view raw event data
- All data in this project is simulated; Only test against systems you own or have permission to test.

## License

Released under the [MIT License](LICENSE).
