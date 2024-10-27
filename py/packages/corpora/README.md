# Corpora Package

Library code and modules for managing and enhancing corpora.

- [**models.py**](models.py): Defines data models.
- [**admin.py**](admin.py): Admin configuration.
- [**requirements.txt**](requirements.txt): Dependencies specific to the corpora package.

The goal of this software is to create a modular, high-performance tool that manages collections of files, known as *corpora*, within a repository or storage system. Each corpus can contain numerous files, and these files are processed to include AI summaries, vector representations, and split segments for enhanced querying, analysis, and AI-driven metadata generation.

The primary features of this system include:

1. **Corpus and File Management**: Users can create, retrieve, and organize corpora and their associated files within a database. Each corpus serves as a unique collection of files with specific metadata.

2. **Vector and AI Integration**: Files and file segments (splits) are vectorized and processed with AI to produce searchable and analyzable content representations. The system stores both the vector data and AI-generated summaries, facilitating tasks like similarity search or content categorization.

3. **API-Driven Architecture**: The software uses a Django and Ninja-based API, allowing external clients to interact with corpora and files over HTTP. This makes it suitable for SaaS deployment and enables secure, asynchronous data processing.

4. **CLI Client**: A command-line interface (CLI) will be developed as the first client, allowing users to interact with the API, process files locally, and push metadata and file data into the system, maintaining performance and security.

The ultimate goal is to build a scalable, robust, and flexible system that can integrate seamlessly with AI models and large data sources, making it suitable for research, content management, and AI-based data querying solutions.
