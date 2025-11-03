import streamlit as st
import json
import os
from datetime import datetime
from newspaper import Article
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# File to store summaries
SUMMARIES_FILE = "news_summaries.json"

# Model configuration
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Initialize OpenAI client
@st.cache_resource
def get_llm():
    """Initialize and cache the OpenAI client"""
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_article_content(url):
    """Extract article content using Newspaper3k"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        return {
            "title": article.title,
            "text": article.text,
            "publish_date": article.publish_date.strftime("%Y-%m-%d") if article.publish_date else datetime.now().strftime("%Y-%m-%d"),
            "authors": article.authors,
            "url": url
        }
    except Exception as e:
        st.error(f"Error extracting article: {str(e)}")
        return None

def summarize_article(article_data, client):
    """Summarize article and classify type using OpenAI Chat Completions"""
    try:
        # Generate summary
        summary_resp = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional news summarizer. Summarize the article in 3-4 concise sentences, "
                        "focusing on key points, main events, and important details."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Title: {article_data['title']}\n\n"
                        f"Article Text:\n{article_data['text'][:4000]}\n\n"
                        "Provide only the summary."
                    ),
                },
            ],
        )
        summary = (summary_resp.choices[0].message.content or "").strip()

        # Classify article type
        classify_resp = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Classify the article type based on the title and summary. "
                        "Choose ONE from: financial, technology, sports, politics, health, entertainment, "
                        "science, business, world, other. Return ONLY the category in lowercase."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Title: {article_data['title']}\n\n"
                        f"Summary: {summary}\n\n"
                        "Category:"
                    ),
                },
            ],
        )
        article_type = (classify_resp.choices[0].message.content or "other").strip().lower()

        return {
            "date": article_data["publish_date"],
            "summary": summary,
            "articleType": article_type,
            "title": article_data["title"],
            "url": article_data["url"],
        }
    except Exception as e:
        st.error(f"Error during summarization: {str(e)}")
        return None

def load_summaries():
    """Load summaries from JSON file"""
    if os.path.exists(SUMMARIES_FILE):
        try:
            with open(SUMMARIES_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_summaries(summaries):
    """Save summaries to JSON file"""
    with open(SUMMARIES_FILE, 'w') as f:
        json.dump(summaries, f, indent=2)

def answer_question(question, summaries, client):
    """Answer questions based on stored summaries using OpenAI Chat Completions"""
    # Prepare context from summaries
    context = "\n\n".join([
        f"Date: {s['date']}\nType: {s['articleType']}\nTitle: {s.get('title', 'N/A')}\nSummary: {s['summary']}"
        for s in summaries
    ])
    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You answer questions strictly based on the provided news summaries. "
                        "If the information is not present, respond with that fact."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Here are the news summaries you have access to:\n" + context +
                        f"\n\nQuestion: {question}\n\nProvide a concise answer."
                    ),
                },
            ],
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        return f"Error answering question: {str(e)}"

# Streamlit UI
def main():
    st.set_page_config(page_title="News Summarization Tool", page_icon="📰", layout="wide")
    
    st.title("📰 News Summarization Tool")
    st.markdown("---")
    
    # Initialize session flags
    if "do_summarize" not in st.session_state:
        st.session_state["do_summarize"] = False
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        st.markdown("---")
        st.markdown("### 📊 Statistics")
        summaries = load_summaries()
        st.metric("Total Summaries", len(summaries))
        
        if summaries:
            types = {}
            for s in summaries:
                article_type = s.get('articleType', 'other')
                types[article_type] = types.get(article_type, 0) + 1
            st.write("**By Type:**")
            for atype, count in types.items():
                st.write(f"• {atype.capitalize()}: {count}")
    
    # Main content area
    st.header("Extract and Summarize News Article")
    
    url = st.text_input("Enter News Article URL:", placeholder="https://example.com/news-article", key="url_input")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        def _trigger_summarize():
            st.session_state["do_summarize"] = True
        st.button("🚀 Summarize", type="primary", on_click=_trigger_summarize, disabled=st.session_state.get("do_summarize", False))
    
    if st.session_state.get("do_summarize") and url:
        if not os.getenv("OPENAI_API_KEY"):
            st.error("⚠️ Please provide an OpenAI API key in the sidebar!")
        else:
            with st.spinner("🔍 Extracting article content..."):
                article_data = extract_article_content(url)
            
            if article_data:
                st.success("✅ Article extracted successfully!")
                
                with st.expander("📄 View Extracted Content", expanded=False):
                    st.write(f"**Title:** {article_data['title']}")
                    st.write(f"**Date:** {article_data['publish_date']}")
                    st.write(f"**Authors:** {', '.join(article_data['authors']) if article_data['authors'] else 'N/A'}")
                    st.write(f"**Text Preview:** {article_data['text'][:500]}...")
                
                with st.spinner("🤖 Generating summary with AI..."):
                    client = get_llm()
                    summary_data = summarize_article(article_data, client)
                
                if summary_data:
                    st.success("✅ Summary generated successfully!")
                    
                    # Display summary in a nice card
                    st.markdown("### 📋 Summary")
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.info(f"**Date:** {summary_data['date']}")
                    with col2:
                        st.info(f"**Type:** {summary_data['articleType'].capitalize()}")
                    
                    st.markdown(f"**Title:** {summary_data['title']}")
                    st.markdown("**Summary:**")
                    st.write(summary_data['summary'])
                    
                    # Save summary
                    summaries = load_summaries()
                    summaries.append(summary_data)
                    save_summaries(summaries)
                    
                    st.success("💾 Summary saved to database!")
                    # Reset action flag to prevent repeated runs
                    st.session_state["do_summarize"] = False
    
    elif st.session_state.get("do_summarize") and not url:
        st.warning("⚠️ Please enter a valid URL!")

    # Q&A Section
    st.markdown("---")
    st.header("Ask Questions from Stored Summaries")

    question = st.text_input(
        "Enter your question:",
        placeholder="e.g., What happened in the latest central bank announcement?",
        key="qa_input",
    )

    col_q1, col_q2 = st.columns([1, 5])
    with col_q1:
        ask_btn = st.button("🧠 Ask", type="primary", key="ask_button")

    if ask_btn:
        summaries_for_qa = load_summaries()
        if not summaries_for_qa:
            st.warning("No summaries found. Add some articles first.")
        elif not question.strip():
            st.warning("Please enter a valid question.")
        else:
            client = get_llm()
            with st.spinner("🤔 Thinking..."):
                response = answer_question(question.strip(), summaries_for_qa, client)
            st.markdown("**Answer:**")
            st.write(response)

            with st.expander("📦 View summaries used as context", expanded=False):
                st.json(summaries_for_qa)

if __name__ == "__main__":
    main()

