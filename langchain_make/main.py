from typing import List, Optional

from agent import Agent
from history import CustomSQLChatMessageHistory
from utils import generate_unique_session


def _send_message(session_id: str, unique_session: List[Optional[str]], message: str) -> None:
    if session_id not in unique_session:
        print("Invalid session id")

    agent_executor = Agent().setup_agent(session_id=session_id, model="gpt-3.5-turbo-16k-0613")
    agent_executor.run(message)


def _get_message_history(session_id: str):
    return CustomSQLChatMessageHistory(session_id=session_id).get_messages_by_session_id()


def _print_message_history(session_id: str) -> None:
    history = _get_message_history(session_id)
    if history:
        print(f"Conversation with session id {session_id}: ")
        for message in history:
            print(message)


def _start_conversation():
    session_id = generate_unique_session()
    CustomSQLChatMessageHistory(session_id=session_id).create_conversation()


def _get_conversations():
    return CustomSQLChatMessageHistory(session_id="null").unique_session_ids()


def _print_conversations():
    unique_session = _get_conversations()
    if unique_session:
        print("Conversations: ")
        for i, conversation in enumerate(unique_session):
            print(f"{i + 1}. {conversation}")

        print("\n\n\n")


def _print_options():
    print("1. Conversations")
    print("2. Start new conversation")
    print("3. Get conversation")


def main():
    while True:
        _print_options()
        option = input("Enter option: ")

        if option == "1":
            _print_conversations()
        elif option == "2":
            _start_conversation()
        elif option == "3":
            session_id = input("Enter session id: ")
            if session_id not in _get_conversations():
                print("Invalid session id")
                break

            while True:
                print("Do exit this conversation type 'q' ")

                _print_message_history(session_id=session_id)

                message = input("Enter message: ")

                if message == "q":
                    break

                _send_message(
                    session_id=session_id,
                    unique_session=CustomSQLChatMessageHistory(
                        session_id="null"
                    ).unique_session_ids(),
                    message=message
                )


main()
