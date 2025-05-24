# RecruitReach AI Gradio Application

A Gradio-based web application for generating personalized emails and cover letters for job applications using AI.

## Directory Structure

```
Recruiter/app/web/gradio/
├── app.py                 # Main application entry point
├── components/           # UI components
│   ├── __init__.py
│   ├── settings_component.py    # Settings UI
│   ├── resume_component.py      # Resume upload UI
│   ├── job_details_component.py # Job details UI
│   └── output_component.py      # Output display UI
├── handlers/             # Business logic handlers
│   ├── __init__.py
│   ├── content_generator.py     # Content generation
│   ├── email_handler.py        # Email sending
│   └── file_handler.py         # File processing
└── utils/               # Utility functions
    ├── __init__.py
    ├── config_loader.py        # Configuration loading
    └── email_validator.py      # Email validation
```

## Components

### Settings Component
- API key configuration
- Email settings (sender email, name, app password)

### Resume Component
- Default/custom resume selection
- Resume file upload
- Generation type selection (Email/Cover Letter)

### Job Details Component
- Job description input (text/file)
- Company details
- Recruiter information
- Job position and source

### Output Component
- Preview (HTML/Plain Text)
- Action buttons (Copy/Send/Download)
- Feedback and regeneration

## Handlers

### Content Generator
- Job description detail extraction
- Email/cover letter generation
- Company research integration

### Email Handler
- Email sending functionality
- Resume attachment handling

### File Handler
- Resume file processing
- Job description file processing

## Utils

### Config Loader
- Configuration file management
- Default settings loading

### Email Validator
- Email format validation

## Usage

1. Configure settings (API key and email)
2. Upload or select default resume
3. Input job description
4. Extract or enter job details
5. Generate email or cover letter
6. Preview and modify as needed
7. Send email or download content

## Running the Application

```python
from Recruiter.app.web.gradio.app import main

if __name__ == "__main__":
    main()
```

The application will be available at `http://localhost:7861`
