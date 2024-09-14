# YouTube Summarizer

## Project Overview
- **Project Name**: YouTube Summarizer
- **Project Goal**: 
  Develop a web application that allows users to input YouTube links and get summarized content in their preferred language. The application will manage summary history, handle video embedding, support custom prompts, and provide a multilingual interface.
- **Key Features**:
  - YouTube video summarization
  - Custom prompt functionality
  - YouTube video embedding
  - Copy summarized result feature
  - Duplicate URL handling
  - History management and deletion
  - Multilingual summary support
  - Loading state indication during processing

## Project Scope
- **Feature Scope**:
  - Input YouTube links and receive a summarized result in the desired language.
  - Detect and provide existing summaries for duplicate links.
  - Provide YouTube video embedding along with the summary.
  - Manage users' request history with options for deleting entries.
  - Offer multiple language options for the summary output.
- **Limitations**:
  - Users can input only YouTube links via the provided fields.
  - API rate limits may affect usage.

## Project Timeline
1. **Planning**: 1 week
   - Requirement analysis
   - System design
2. **Design**: 1 week
   - UI/UX design
   - HTML/CSS layout design
3. **Development**: 2-3 weeks
   - Integration of YouTube API and OpenAI API
   - Development of custom prompt functionality
   - Duplicate URL handling logic
   - History management feature development
   - Multilingual support development
4. **Testing**: 1 week
   - Functional testing
   - Bug fixing
   - Performance optimization
5. **Deployment**: 1 week
   - Server deployment
   - Incorporating user feedback

## Team Structure
- **Project Manager (PM)**: Oversees project management and schedule.
- **Frontend Developer**: Focuses on UI/UX development using HTML/CSS/JavaScript.
- **Backend Developer**: Handles Flask development, API integration, and database design.
- **Tester**: Conducts application functionality and performance testing.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript, jQuery
- **Backend**: Python, Flask
- **API**: YouTube Data API, OpenAI API
- **Database**: JSON file or a simple NoSQL database (for history management)
- **Deployment**: Heroku or AWS EC2
- **Version Control**: Git, GitHub

## Risk Management
- **Technical Risks**:
  - **API Usage Limits**: Service downtime may occur due to YouTube and OpenAI API rate limits.
  - **Performance Issues**: Risk of server overload with many concurrent users.
  - **Browser Compatibility**: Issues could arise with various browsers.
- **Mitigation**:
  - Monitor API usage and consider alternatives if limits are reached.
  - Optimize API calls for better performance.
  - Test compatibility across major browsers.

## Performance Metrics
- **Performance Goals**:
  - Ensure summarization accuracy and comprehensiveness.
  - Provide fast response times.
  - Gather and incorporate user feedback.
- **Performance Indicators**:
  - API response time
  - User retention rate
  - Error logs and frequency

## Test Plan
- **Unit Testing**: Test individual functions and components.
- **Integration Testing**: Ensure smooth interaction between frontend and backend.
- **User Testing**: Gather feedback through user testing.
- **Performance Testing**: Measure response time and API performance.

## Deployment Plan
- **Deployment Environment**: Heroku or AWS EC2
- **Process**:
  1. Final testing in the staging environment.
  2. Set up and configure the server for deployment.
  3. Roll out updates and maintenance based on user feedback.

## Maintenance and Updates
- **Bug Fixes and Feature Enhancements**: Ongoing code refactoring and performance improvements.
- **New Feature Development**: Add features based on user requests (e.g., support for more languages, new API integrations).
- **Logs and Monitoring**: Regularly monitor server health and collect error logs for analysis.

---

Thank you for using **YouTube Summarizer**! Feel free to contribute to the project or report any issues you encounter.

---

## Features
- Automatically extracts and processes transcripts from YouTube videos.
- Summarizes long transcripts into concise, readable blog posts.
- Supports both English and Korean language summarization.
- Simple and intuitive web interface for easy use.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [API Key Setup](#api-key-setup)
4. [License](#license)

## Installation

To set up and run this project locally, follow these steps:

### Prerequisites
- Python 3.8 or higher
- Flask
- OpenAI API Key
- YouTube Transcript API
- `python-dotenv` for environment variable management

### Clone the Repository
```bash
git clone https://github.com/yourusername/youtube-video-summarizer.git
cd youtube-video-summarizer
```

### Install Dependencies
It's recommended to create a virtual environment first:

```bash
코드 복사
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Then, install the necessary dependencies:

```bash
pip install -r requirements.txt
```

### API Key Setup
To use OpenAI's GPT model, you'll need an API key. Create a .env file in the project root and add your OpenAI API key:

```bash
OPENAI_API_KEY=your-openai-api-key
```

### Run the Application
Start the Flask server with the following command:

```bash
python app.py
```

The application will be running at http://127.0.0.1:5000.

### Usage
Open the browser and go to http://127.0.0.1:5000.
Paste a YouTube video link into the input field and click "Summarize".
The summary will be generated and displayed in the results box. You can also copy the summary using the "Copy" button.
Configuration

Ensure the following environment variables are set in your .env file:

OPENAI_API_KEY: Your OpenAI API key.
Other settings related to Flask or APIs can be adjusted in the configuration files as needed.
Project Structure

```bash
youtube-video-summarizer/
│
├── app.py              # Main Flask app
├── youtube_summary.py   # Transcript and summarization logic
├── templates/
│   └── index.html       # Frontend HTML file
├── static/
│   └── style.css        # CSS file for styling
├── .env                 # Environment variables (not included in version control)
├── requirements.txt     # Python dependencies
└── README.md            # Project readme (this file)
```

### License
This project is licensed under the MIT License - see the LICENSE file for details.
