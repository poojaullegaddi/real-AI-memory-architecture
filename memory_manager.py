import streamlit as st

from token_utils import count_tokens
from summarizer import summarize_conversation

from vector_store import (
    store_memory,
    retrieve_relevant_memories
)

from importance_detector import (
    detect_important_memory
)

# --------------------------------
# LOWER TOKEN LIMIT FOR TESTING
# --------------------------------
MAX_TOKENS = 200


# --------------------------------
# UPDATE MEMORY
# --------------------------------
def update_memory(user_message, assistant_reply):

    # Store conversation
    st.session_state.recent_messages.append({
        "role": "user",
        "content": user_message
    })

    st.session_state.recent_messages.append({
        "role": "assistant",
        "content": assistant_reply
    })

    # --------------------------------
    # DETECT IMPORTANT MEMORY
    # --------------------------------
    is_important = detect_important_memory(
        user_message
    )

    if is_important:

        st.session_state.important_memories.append(
            user_message
        )

        store_memory(user_message)

        st.sidebar.success(
            "Important memory stored."
        )

    # --------------------------------
    # BUILD FULL CONTEXT
    # --------------------------------
    full_context = build_context(
        user_message
    )

    # --------------------------------
    # TOKEN COUNT
    # --------------------------------
    current_tokens = count_tokens(
        full_context
    )

    # Debug info
    st.sidebar.write(
        f"MAX TOKENS: {MAX_TOKENS}"
    )

    st.sidebar.write(
        f"CURRENT TOKENS: {current_tokens}"
    )

    # --------------------------------
    # TOKEN LIMIT CHECK
    # --------------------------------
    if current_tokens > MAX_TOKENS:

        st.sidebar.error(
            "TOKEN LIMIT EXCEEDED"
        )

        # Prevent empty summary
        if len(
            st.session_state.recent_messages
        ) > 8:

            old_messages = (
                st.session_state
                .recent_messages[:-8]
            )

        else:

            old_messages = (
                st.session_state
                .recent_messages
            )

        # Summarize
        summary = summarize_conversation(
            old_messages
        )

        # Store summary
        st.session_state.summary_memory += (
            "\n" + summary
        )

        # Keep latest messages only
        st.session_state.recent_messages = (
            st.session_state
            .recent_messages[-8:]
        )

        st.sidebar.success(
            "Conversation summarized."
        )


# --------------------------------
# BUILD CONTEXT
# --------------------------------
def build_context(user_input):

    messages = []

    # --------------------------------
    # SYSTEM PROMPT
    # --------------------------------
    messages.append({
        "role": "system",
        "content": """
        You are an intelligent study assistant.

        Maintain conversation continuity carefully.
        """
    })

    # --------------------------------
    # SUMMARY MEMORY
    # --------------------------------
    if st.session_state.summary_memory:

        messages.append({
            "role": "system",
            "content":
            f"Conversation Summary:\n"
            f"{st.session_state.summary_memory}"
        })

    # --------------------------------
    # IMPORTANT MEMORIES
    # --------------------------------
    if st.session_state.important_memories:

        important_text = "\n".join(
            st.session_state
            .important_memories
        )

        messages.append({
            "role": "system",
            "content":
            f"Important Memory:\n"
            f"{important_text}"
        })

    # --------------------------------
    # VECTOR MEMORY SEARCH
    # --------------------------------
    retrieved_memories = (
        retrieve_relevant_memories(
            user_input
        )
    )

    if retrieved_memories:

        retrieved_text = "\n".join(
            retrieved_memories
        )

        messages.append({
            "role": "system",
            "content":
            f"Relevant Past Memory:\n"
            f"{retrieved_text}"
        })

    # --------------------------------
    # RECENT CONVERSATION
    # --------------------------------
    messages.extend(
        st.session_state.recent_messages
    )

    return messages