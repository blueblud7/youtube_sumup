#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:11:04 2024

@author: Sangwon Chae
"""

from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import json
import re
import tiktoken
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 불러오기
load_dotenv()

# OpenAI API 키 설정
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

def get_youtube_transcript(video_id):
    try:
        # 먼저 한국어 자막을 시도
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
        return ' '.join([entry['text'] for entry in transcript]), 'ko'
    except:
        try:
            # 한국어 자막이 없으면 영어 자막을 시도
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            return ' '.join([entry['text'] for entry in transcript]), 'en'
        except Exception as e:
            print(f"트랜스크립트를 가져오는 데 실패했습니다: {str(e)}")
            return None, None

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
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

def summarize_chunk(chunk, chunk_number, total_chunks, language):
    prompt = f"""
    This is part {chunk_number} of {total_chunks} from a transcript of a YouTube video. 
    Please provide a brief summary (about 50 words) of the key points discussed in this part.
    The original language of the transcript is {language}.

    Transcript part {chunk_number}:
    {chunk}

    Summary:
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that summarizes parts of YouTube video transcripts. Please provide the summary in {language}."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"청크 요약 생성에 실패했습니다: {str(e)}")
        return None

def generate_blog_post(summaries, language):
    combined_summary = "\n\n".join(summaries)
    
    if language == 'ko':
        prompt = f"""
        다음은 YouTube 비디오의 요약입니다. 이를 바탕으로 일반 독자를 대상으로 하는 정보성 있고 이해하기 쉬운 블로그 포스트를 작성해 주세요. 블로그 포스트는 다음과 같은 구조로 작성되어야 합니다:

        제목: 비디오의 주요 주제를 반영하는 간결하고 주목을 끄는 제목.
        키워드 (5개): 비디오의 주요 주제를 요약하는 관련 키워드 5개.
        핵심요약 (50단어 이내): 비디오의 핵심 포인트를 강조하는 간단한 요약.
        상세요약 (200-300단어): 비디오 내용을 더 깊이 있게 설명하는 포괄적인 요약.
        결론 (50단어 이내): 비디오의 핵심 메시지를 강화하는 최종 생각 또는 요점.

        비디오 요약:
        {combined_summary}

        각 섹션이 명확히 구분되도록 하고, 사용된 언어는 간단하면서도 정보성 있게 작성해 주세요.
        """
    else:  # English
        prompt = f"""
        Based on the following summaries of a YouTube video, please write a blog post in English that is both informative and easy to understand, targeting a general audience. The blog post should be structured as follows:

        Title: A concise and attention-grabbing title that reflects the main topic of the video.
        Keywords (5): Five relevant keywords that summarize the main themes of the video.
        Key Summary (within 50 words): A brief summary highlighting the essential points of the video.
        Detailed Summary (200-300 words): A comprehensive summary that explains the video's content in more depth.
        Conclusion (within 50 words): A final thought or takeaway that reinforces the key message of the video.

        Video Summaries:
        {combined_summary}

        Please ensure that each section is clearly separated and that the language used is simple, yet informative.
        """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that generates blog posts in {language} from YouTube video summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"최종 블로그 포스트 생성에 실패했습니다: {str(e)}")
        return None

def summarize_youtube_video(youtube_link):
    # Get the video ID from the link
    video_id = youtube_link.split("v=")[-1]

    # Fetch the transcript and language
    transcript, language = get_youtube_transcript(video_id)

    if transcript:
        transcript_chunks = split_transcript(transcript)
        chunk_summaries = []

        # Summarize each chunk
        for i, chunk in enumerate(transcript_chunks):
            summary = summarize_chunk(chunk, i+1, len(transcript_chunks), language)
            if summary:
                chunk_summaries.append(summary)
        
        if chunk_summaries:
            # Generate the blog post
            blog_post_content = generate_blog_post(chunk_summaries, language)
            return blog_post_content
    else:
        return "트랜스크립트를 가져오는 데 실패했습니다."
