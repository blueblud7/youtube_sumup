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
    # 히스토리를 넘겨주어야 하므로 'history=history'를 전달
    return render_template('index.html', history=history)

@app.route('/summarize', methods=['POST'])
def summarize():
    youtube_link = request.form['youtube_link']
    custom_prompt = request.form.get('custom_prompt', '')  # custom_prompt 가져오기
    
    # 요약 결과 생성
    summary = youtube_summary.summarize_youtube_video(youtube_link, custom_prompt)
    
    if summary:
        # 히스토리에 추가
        entry = {'youtube_link': youtube_link, 'summary': summary}
        history.append(entry)
        
        # history.json 파일에 히스토리 저장
        with open('history.json', 'w') as f:
            json.dump(history, f)
        
        return jsonify(entry)  # 결과 반환 (AJAX를 통해 HTML에 직접 결과 표시)
    else:
        return jsonify({"error": "Summary generation failed."}), 500

@app.route('/history', methods=['GET'])
def get_history():
    # 히스토리 전체를 반환
    return jsonify(history)

@app.route('/history/<int:index>', methods=['GET'])
def get_history_item(index):
    # 히스토리 항목 가져오기
    if index < len(history):
        return jsonify(history[index])
    else:
        return jsonify({"error": "History item not found."}), 404

# 히스토리에서 항목 삭제
@app.route('/history/delete/<int:index>', methods=['DELETE'])
def delete_history_item(index):
    if index < len(history):
        del history[index]
        
        # 히스토리 업데이트 후 JSON 파일에 다시 저장
        with open('history.json', 'w') as f:
            json.dump(history, f)
        
        return jsonify({"success": "History item deleted."})
    else:
        return jsonify({"error": "History item not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
