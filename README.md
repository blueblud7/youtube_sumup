# YouTube Video Summarizer

A web application that automatically summarizes YouTube videos by extracting transcripts and generating concise summaries using OpenAI's GPT model. This project is built with Flask and OpenAI API, allowing users to input a YouTube link and receive a summary of the video.

## Features
- Automatically extracts and processes transcripts from YouTube videos.
- Summarizes long transcripts into concise, readable blog posts.
- Supports both English and Korean language summarization.
- Simple and intuitive web interface for easy use.

## Demo
Check out the [live demo](#) (if hosted).

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


### 사용 방법
1. 위 내용을 복사하여 프로젝트의 루트 디렉토리에 `README.md` 파일을 생성한 후 붙여넣으세요.
2. `yourusername`과 같은 부분을 GitHub 사용자명과 리포지토리명에 맞게 변경하세요.
3. 커밋 후 GitHub에 푸시하면 `README.md` 파일이 GitHub 리포지토리 페이지에 자동으로 표시됩니다.
