#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:06:27 2024

@author: Sangwon Chae
"""

from flask import Flask, render_template, request, jsonify
import youtube_summary  # YouTube 요약 코드를 포함한 파일
import json  # json 모듈 임포트
import os

app = Flask(__name__)

# 히스토리를 저장하는 리스트
history = []

# history.json 파일에서 기존 히스토리 로드
if os.path.exists('history.json'):
    with open('history.json', 'r') as f:
        history = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    youtube_link = request.form['youtube_link']
    custom_prompt = request.form.get('custom_prompt', '')

    # 유튜브 링크에서 VIDEO_ID를 추출하는 함수 호출
    video_id = extract_video_id(youtube_link)

    if not video_id:
        return jsonify({"error": "Invalid YouTube link."}), 400

    # YouTube Video ID로 중복된 비디오가 있는지 확인
    for entry in history:
        if entry.get('video_id') == video_id:
            return jsonify({"message": "중복된 URL입니다. 기존 요약을 보여드리겠습니다.",
                            "youtube_link": entry['youtube_link'], 
                            "summary": entry['summary'],
                            "title": entry['title']})

    # 요약 결과 생성
    summary = youtube_summary.summarize_youtube_video(video_id, custom_prompt)

    if summary:
        # 히스토리에 추가
        entry = {'youtube_link': youtube_link, 'video_id': video_id, 'summary': summary, 'title': 'Video Title'}
        history.append(entry)

        # 새로운 요약이 추가될 때 history.json 파일에 저장
        with open('history.json', 'w') as f:
            json.dump(history, f)

        return jsonify(entry)
    else:
        return jsonify({"error": "Summary generation failed."}), 500

@app.route('/history', methods=['GET'])
def get_history():
    page = int(request.args.get('page', 1))
    items_per_page = int(request.args.get('itemsPerPage', 20))

    start = (page - 1) * items_per_page
    end = start + items_per_page
    total_pages = (len(history) + items_per_page - 1) // items_per_page

    paginated_history = history[start:end]

    return jsonify({
        'history': paginated_history,
        'page': page,
        'totalPages': total_pages
    })

def extract_video_id(youtube_link):
    """YouTube 링크에서 VIDEO_ID를 추출하는 함수"""
    if "youtube.com/watch?v=" in youtube_link:
        return youtube_link.split("v=")[1].split("&")[0]  # 브라우저 URL 처리
    elif "youtu.be/" in youtube_link:
        return youtube_link.split("youtu.be/")[1].split("?")[0]  # 공유 URL 처리
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)
