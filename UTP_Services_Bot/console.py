from model import UTPAssistModel

def main():
    bot = UTPAssistModel()  # Load your CSV dataset
    print("Welcome to UTP Assist Bot!")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break

        response = bot.get_response(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    main()
