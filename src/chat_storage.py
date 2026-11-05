
import streamlit as st
from datetime import datetime


def initialize_chat_storage():
    if "chat_conversations" not in st.session_state:
        st.session_state.chat_conversations = {}

    if "next_conversation_id" not in st.session_state:
        st.session_state.next_conversation_id = 1


def create_conversation(title="New conversation"):
    initialize_chat_storage()

    conversation_id = st.session_state.next_conversation_id
    st.session_state.next_conversation_id += 1

    now = datetime.now().isoformat()

    st.session_state.chat_conversations[conversation_id] = {
        "id": conversation_id,
        "title": title,
        "created_at": now,
        "updated_at": now,
        "messages": [],
    }

    return conversation_id


def get_conversations():
    initialize_chat_storage()

    conversations = st.session_state.chat_conversations.values()

    return sorted(
        [
            {
                "id": chat["id"],
                "title": chat["title"],
                "created_at": chat["created_at"],
                "updated_at": chat["updated_at"],
            }
            for chat in conversations
        ],
        key=lambda chat: chat["updated_at"],
        reverse=True,
    )


def save_message(conversation_id, role, content):
    initialize_chat_storage()

    if role not in ("user", "assistant"):
        raise ValueError("Invalid message role.")

    conversation = st.session_state.chat_conversations.get(
        conversation_id
    )

    if conversation is None:
        raise ValueError("Conversation not found.")

    conversation["messages"].append({
        "id": len(conversation["messages"]) + 1,
        "conversation_id": conversation_id,
        "role": role,
        "content": content,
        "created_at": datetime.now().isoformat(),
    })

    conversation["updated_at"] = datetime.now().isoformat()


def get_messages(conversation_id):
    initialize_chat_storage()

    conversation = st.session_state.chat_conversations.get(
        conversation_id
    )

    if conversation is None:
        return []

    return conversation["messages"]


def rename_conversation(conversation_id, title):
    initialize_chat_storage()

    title = title.strip()

    if not title:
        raise ValueError("Conversation title cannot be empty.")

    conversation = st.session_state.chat_conversations.get(
        conversation_id
    )

    if conversation:
        conversation["title"] = title
        conversation["updated_at"] = datetime.now().isoformat()


def delete_conversation(conversation_id):
    initialize_chat_storage()

    st.session_state.chat_conversations.pop(
        conversation_id, None
    )
