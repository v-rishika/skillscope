
import streamlit as st

from src.ai_career_guide import ask_career_guide
from src.chat_storage import (
    initialize_chat_storage,
    create_conversation,
    delete_conversation,
    get_conversations,
    get_messages,
    rename_conversation,
    save_message,
)


def start_new_chat():
    conversation_id = create_conversation()
    st.session_state.active_conversation_id = conversation_id


def render_career_guide():
    # Initialize temporary chat storage.
    initialize_chat_storage()

    if "active_conversation_id" not in st.session_state:
        st.session_state.active_conversation_id = None

    st.markdown("## Your AI Career Guide")

    conversations = get_conversations()

    # Keep chat controls visible on the main page.
    col1, col2 = st.columns([1, 3])

    with col1:
        if st.button("＋ New chat", use_container_width=True):
            start_new_chat()
            st.rerun()

    # Display saved conversations from the current session.
    options = {
        conversation["id"]: conversation["title"]
        for conversation in conversations
    }

    active_id = st.session_state.active_conversation_id

    # Reset active conversation if it no longer exists.
    if active_id not in options:
        st.session_state.active_conversation_id = None
        active_id = None

    with col2:
        selected_id = st.selectbox(
            "Saved conversations",
            options=[None] + list(options.keys()),
            format_func=lambda chat_id: (
                "Choose a previous conversation"
                if chat_id is None
                else options[chat_id]
            ),
            index=(
                [None] + list(options.keys())
            ).index(active_id),
            key="selected_chat",
        )

    if selected_id is not None:
        if selected_id != st.session_state.active_conversation_id:
            st.session_state.active_conversation_id = selected_id
            st.rerun()

        with st.expander("Manage current chat"):
            new_title = st.text_input(
                "Chat title",
                value=options[selected_id],
                key=f"title_{selected_id}",
            )

            col_rename, col_delete = st.columns(2)

            with col_rename:
                if st.button(
                    "Rename chat",
                    key=f"rename_{selected_id}",
                ):
                    if new_title.strip():
                        rename_conversation(
                            selected_id,
                            new_title,
                        )
                        st.rerun()
                    else:
                        st.warning("Please enter a chat title.")

            with col_delete:
                if st.button(
                    "Delete chat",
                    key=f"delete_{selected_id}",
                ):
                    delete_conversation(selected_id)
                    st.session_state.active_conversation_id = None
                    st.session_state.selected_chat = None
                    st.rerun()

    # Get messages from the active conversation.
    conversation_id = st.session_state.active_conversation_id

    messages = (
        get_messages(conversation_id)
        if conversation_id is not None
        else []
    )

    # Display welcome screen when there is no active conversation.
    if conversation_id is None or not messages:
        st.markdown(
            """
            <div style="text-align: center; padding: 40px 0 24px 0;">
                <h2 style="margin-bottom: 10px;">
                    What are we figuring out today?
                </h2>
                <p>
                    Career paths, skills, interviews, or your next move.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### Explore a topic")

        prompt_col1, prompt_col2 = st.columns(2)

        with prompt_col1:
            if st.button(
                "↗ Build a career roadmap",
                use_container_width=True,
            ):
                st.session_state.suggested_question = (
                    "Help me build a personalized career roadmap."
                )
                st.rerun()

            if st.button(
                "↗ Prepare for interviews",
                use_container_width=True,
            ):
                st.session_state.suggested_question = (
                    "Help me prepare for technical interviews."
                )
                st.rerun()

        with prompt_col2:
            if st.button(
                "↗ Learn a technical skill",
                use_container_width=True,
            ):
                st.session_state.suggested_question = (
                    "Help me choose a technical skill to learn next."
                )
                st.rerun()

            if st.button(
                "↗ Explore career options",
                use_container_width=True,
            ):
                st.session_state.suggested_question = (
                    "Help me explore career roles that match my interests."
                )
                st.rerun()

    # Display existing messages.
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle suggested questions.
    suggested_question = st.session_state.pop(
        "suggested_question",
        None,
    )

    question = st.chat_input("Ask your career question...")

    if suggested_question:
        question = suggested_question

    if question:
        # Create a conversation when the first question is submitted.
        if conversation_id is None:
            conversation_id = create_conversation()
            st.session_state.active_conversation_id = conversation_id

        # Save the user's question.
        save_message(conversation_id, "user", question)

        # Prepare previous messages for Gemini.
        chat_history = [
            {
                "role": (
                    "model"
                    if message["role"] == "assistant"
                    else "user"
                ),
                "content": message["content"],
            }
            for message in get_messages(conversation_id)[:-1]
        ]

        # Generate AI response.
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = ask_career_guide(
                    question,
                    chat_history=chat_history,
                )

                st.markdown(answer)

        # Save the assistant response.
        save_message(conversation_id, "assistant", answer)

        # Automatically generate a title for new conversations.
        if not messages:
            title = question.strip().replace("\n", " ")

            if len(title) > 40:
                title = title[:37].rstrip() + "..."

            rename_conversation(
                conversation_id,
                title or "New conversation",
            )

        st.rerun()
