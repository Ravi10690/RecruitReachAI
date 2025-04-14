# RecruitReach2

An AI-powered application for generating personalized recruiter outreach emails and cover letters for job applications.

## Features

- **Email Generation**: Create personalized recruiter outreach emails tailored to specific job descriptions and companies.
- **Cover Letter Generation**: Generate professional cover letters customized to your resume and the job requirements.
- **Company Research**: Automatically research company information using web search or AI to personalize your communications.
- **Job Description Analysis**: Extract key details from job descriptions to streamline the application process.
- **Email Sending**: Send emails directly from the application with your resume attached.
- **User-Friendly Interface**: Clean, intuitive interface with dark and light theme options.
- **Responsive Design**: Works well on both desktop and mobile devices.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer) or uv (optional, faster package manager)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/RecruitReach2.git
   cd RecruitReach2
   ```

2. Set up your environment (choose one of the following options):

   #### Option A: Using uv package manager (recommended)
   
   1. Install uv (if not already installed):
      ```bash
      # Using pip
      pip install uv
      
      # Or using curl (Linux/macOS)
      curl -LsSf https://astral.sh/uv/install.sh | sh
      
      # Or using PowerShell (Windows)
      irm https://astral.sh/uv/install.ps1 | iex
      ```
   
   2. Create a virtual environment and install dependencies in one command:
      ```bash
      uv venv
      ```
   
   3. Activate the virtual environment:
      ```bash
      # On Linux/macOS
      source .venv/bin/activate
      
      # On Windows
      .venv\Scripts\activate
      ```
   
   4. Install dependencies using uv:
      ```bash
      uv pip install -r requirements.txt
      ```
      
   #### Option B: Using traditional venv
   
   1. Create a virtual environment:
      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      ```
   
   2. Install dependencies:
      ```bash
      pip install -r requirements.txt
      ```

3. Configure the application:
   - Copy the sample configuration file:
     ```bash
     cp config/config.toml.sample config/config.toml
     ```
   - Edit `config/config.toml` with your API keys and email settings:
     ```toml
     [openai]
     OPENAI_API_KEY = "your-api-key"  # Your OpenAI API key

     [email]
     sender_email = "your@email.com"    # Your email address
     sender_name = "Your Name"          # Your name
     smtp_server = "smtp.gmail.com"     # SMTP server (default for Gmail)
     smtp_port = 587                    # SMTP port (default for Gmail)
     app_password = "your-app-password" # Your email app password
     ```
   - Alternatively, you can enter these values directly in the application UI

4. Add your resume:
   - Place your resume PDF file in the `data` directory with the name `resume.pdf`
   - Or upload your resume through the application interface

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. The application will open in your default web browser at `http://localhost:8501`

3. Using the application:
   - Select whether you want to generate an email or cover letter
   - Choose to use your default resume or upload a new one
   - Enter or upload a job description
   - Extract details from the job description or enter them manually
   - Generate your personalized email or cover letter
   - Preview, copy, download, or send your content

## Email Configuration

When using Gmail for sending emails, you'll need to:
1. Enable 2-Step Verification on your Google account
2. Generate an App Password
3. Use the App Password in the configuration instead of your regular password

For more information on setting up Gmail App Passwords, visit: https://support.google.com/accounts/answer/185833

## Project Structure

```
RecruitReach2/
├── app/                  # Application components
│   ├── api/              # API endpoints
│   └── web/              # Web interface
├── config/               # Configuration files
├── core/                 # Core business logic
│   ├── company_research/ # Company research functionality
│   ├── cover_letter/     # Cover letter generation
│   ├── email/            # Email generation
│   └── resume/           # Resume parsing
├── data/                 # Data files (resumes, etc.)
├── models/               # Data models and schemas
├── prompts/              # LLM prompts for various functionalities
├── services/             # External services integration
│   ├── email_service/    # Email sending service
│   └── llm/              # Language model service
├── tests/                # Test cases
├── utils/                # Utility functions
│   ├── config/           # Configuration utilities
│   ├── file_utils/       # File handling utilities
│   └── web_search/       # Web search utilities
├── main.py               # Application entry point
└── README.md             # Project documentation
```

## Requirements

The application requires the following Python packages:
- streamlit
- langchain
- langchain_openai
- pydantic
- tomli
- PyPDF2
- python-docx
- email
- beautifulsoup4
- googlesearch-python
- agents

See `requirements.txt` for the complete list of dependencies.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the language models
- Streamlit for the web application framework
