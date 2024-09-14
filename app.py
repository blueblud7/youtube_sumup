#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:06:27 2024

@author: Sangwon Chae
"""

from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import re
import tiktoken
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
        return ' '.join([entry['text'] for entry in transcript]), 'ko'
    except:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            return ' '.join([entry['text'] for entry in transcript]), 'en'
        except Exception as e:
            print(f"Failed to retrieve transcript: {str(e)}")
            return None, None

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def split_transcript(transcript, max_tokens=2000):
    chunks = []
    current_chunk = ""
    current_tokens = 0

    for sentence in re.split('(?<=[.!?]) +', transcript):
        sentence_tokens = num_tokens_from_string(sentence, "cl100k_base")
        if current_tokens + sentence_tokens > max_tokens:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_tokens = sentence_tokens
        else:
            current_chunk += " " + sentence
            current_tokens += sentence_tokens

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def summarize_chunk(chunk, chunk_number, total_chunks, language, custom_prompt=''):
    prompt = f"""
    Summarize the key points of this YouTube video into a concise, easy-to-understand blog post in Korean. 
    Ensure that all major topics and information are included, and the summary should allow readers to fully grasp the content without needing to watch the video. Organize the summary into paragraphs with a natural flow, and highlight the most important points.

    Additional Notes:
    - Start with a clear sentence explaining the video's topic.
    - Summarize the main ideas or information briefly and concisely.
    - Conclude with a key takeaway or final summary.

    Transcript part {chunk_number} of {total_chunks}:
    {chunk}
    
    Summary:
    """

    print(f"Generated prompt for chunk {chunk_number}: {prompt}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that summarizes parts of YouTube video transcripts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Failed to summarize chunk {chunk_number}: {str(e)}")
        return None

def generate_blog_post(summaries, language):
    combined_summary = "\n\n".join(summaries)
    
    prompt = f"""
    Based on the following summaries, write a blog post that is informative and easy to understand in Korean. 
    Summaries:
    {combined_summary}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that generates blog posts from YouTube video summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Failed to generate blog post: {str(e)}")
        return None

def summarize_youtube_video(youtube_link, custom_prompt=''):
    video_id = youtube_link.split("v=")[-1]
    transcript, language = get_youtube_transcript(video_id)

    if transcript:
        transcript_chunks = split_transcript(transcript)
        chunk_summaries = []

        for i, chunk in enumerate(transcript_chunks):
            summary = summarize_chunk(chunk, i+1, len(transcript_chunks), language, custom_prompt)
            if summary:
                chunk_summaries.append(summary)

        if chunk_summaries:
            return generate_blog_post(chunk_summaries, language)
    return "Failed to retrieve transcript."
