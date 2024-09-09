#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:06:27 2024

@author: Sangwon Chae
"""

from flask import Flask, render_template, request, jsonify

import youtube_summary  # YouTube 요약 코드를 포함한 파일

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    youtube_link = request.form['youtube_link']
    summary = youtube_summary.summarize_youtube_video(youtube_link)
    
    if summary:
        return summary  # AJAX를 통해 HTML에 직접 결과 표시
    else:
        return "Summary generation failed."

if __name__ == '__main__':
    app.run(debug=True)
