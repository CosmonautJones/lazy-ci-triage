# Third-party notes

- Qwen2.5-Coder 1.5B Instruct, Q4_K_M, by the Qwen team, is used through Ollama. [Model metadata](https://ollama.com/library/qwen2.5-coder:1.5b), [Apache 2.0 license](https://ollama.com/library/qwen2.5-coder:1.5b/blobs/832dd9e00a68), [upstream model card](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct). Model weights are not distributed by this repository.
- Ollama is an external runtime, [MIT licensed](https://github.com/ollama/ollama/blob/main/LICENSE). It is not bundled. This project uses its documented local HTTP API.
- Python's standard library supplies parsing, HTTP, CLI, report and test functions. There are no third-party Python runtime dependencies.
- The synthetic fixtures, parser/validator implementation and writing were created for this new project. No application implementation was imported from another project.
- The DEV draft follows the official [Slow and Steady template](https://dev.to/challenges/hacktoberfest-week3-2026-10-19). Rules and disclosure references are listed in `docs/challenge-checklist.md`.
