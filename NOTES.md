# NOTES.md

## Tools Used
- **Flask**: For building the API.
- **Pytest**: For writing and executing tests.
- **ChatGPT**: Used for architectural guidance, code structuring, and test planning. All generated code was reviewed and modified manually before integration.

---

## Approach & Architecture

- **Core Functionality First**: Started with implementing the `/api/shorten`, redirect (`/<short_code>`), and `/api/stats/<short_code>` endpoints.
- **Thread Safety**: Implemented using `threading.Lock()` within the `URLStore` class to ensure safe concurrent access.
- **Separation of Concerns**:
  - `main.py` contains route logic.
  - `models.py` contains in-memory storage and concurrency-safe methods.
  - `utils.py` handles reusable logic like URL validation and short code generation.
- **Short Code Logic**: Generates a random 6-character alphanumeric code and checks for collisions.

---

## Error Handling

- Validates input JSON and URL format.
- Returns `400` for invalid input and `404` for missing short codes.
- Covers both functional and edge cases.

---

## Testing Summary

> Total Tests Written: **6**  
(Covering all critical paths and an additional real-world URL test)

| Test Name                  | Purpose                                     |
|---------------------------|---------------------------------------------|
| `test_shorten_url`        | Tests successful shortening of a URL        |
| `test_invalid_url`        | Ensures invalid URLs are rejected           |
| `test_redirect`           | Tests redirection logic                     |
| `test_stats`              | Checks analytics and click tracking         |
| `test_not_found`          | Verifies behavior for unknown short codes   |
| `test_real_hindu_article` | Full integration with real, long URL        |

---

## Decisions & Trade-offs

- Used in-memory dictionary with lock for concurrency (no DB used as per instructions).
- Avoided overengineering by keeping routes flat and logic minimal.
- Prioritized clarity and modularity for scalability, if extended in future.

---

