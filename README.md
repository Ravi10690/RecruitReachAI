# RecruitReachAI 🤖

RecruitReachAI is an intelligent job application assistant that automates and personalizes the process of applying for jobs. It uses AI to generate customized emails, analyze job descriptions, and streamline the job application process.

## 🌟 Features

- **Smart Email Generation**: Automatically generates personalized job application emails based on:
  - Your resume
  - Job description
  - Company research
  - Position details
  
- **Company Research**: Automatically researches and includes relevant company information in your application

- **Resume Handling**:
  - Support for default resume
  - Upload custom resumes (PDF, DOCX)
  - Intelligent resume parsing

- **Job Description Analysis**:
  - Extracts key information from job postings
  - Identifies company name, recruiter email, and position
  - Supports both text input and file upload

- **Email Management**:
  - Direct email sending capability
  - Professional email formatting
  - Attachment handling
  - Email preview and editing

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Required Python packages (install via `pip`):
  ```bash
  pip install -r requirements.txt
  ```

### Configuration

1. Copy the sample configuration file:
   ```bash
   cp RecruitReach_AI/config/config.toml.sample RecruitReach_AI/config/config.toml
   ```

2. Update the configuration in `config.toml` with your:
   - API keys
   - Email settings
   - Other personal preferences

### Running the Application

1. Start the Streamlit web interface:
   ```bash
   streamlit run RecruitReach_AI/web/streamlit_app.py
   ```

2. Access the application at `http://localhost:8501`

## 💻 Usage

1. **Input Job Description**:
   - Paste the job description text directly
   - Or upload a job description file

2. **Choose Resume**:
   - Use your default resume
   - Upload a custom resume for this application

3. **Review Details**:
   - Verify extracted company name
   - Confirm recruiter email
   - Check job position
   - Add job source

4. **Generate & Send Email**:
   - Click "Generate Email" to create your personalized application
   - Preview the generated email
   - Make any necessary adjustments
   - Send directly through the platform

## 🏗️ Project Structure

```
RecruitReach_AI/
├── Company_Research/       # Company research functionality
├── Email/                 # Email generation and sending
├── Resume/               # Resume parsing and handling
├── config/              # Configuration files
├── models/              # LLM and AI models
├── prompts/             # System prompts
├── schema/              # Data models
├── utils/               # Utility functions
└── web/                 # Web interface (Streamlit)
```

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **AI/ML**: LangChain
- **Email**: SMTP/Email libraries
- **File Processing**: PyPDF2, python-docx
- **Data Validation**: Pydantic

## 🔒 Security

- Sensitive information is stored in configuration files
- Email credentials are handled securely
- Personal data is processed locally

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ✨ Acknowledgments

- Thanks to all contributors who have helped shape RecruitReachAI
- Special thanks to the open-source community for the amazing tools and libraries

---

Built with ❤️ using AI to make job applications smarter and more efficient.
