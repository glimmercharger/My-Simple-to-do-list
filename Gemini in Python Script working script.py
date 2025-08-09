import os
import sys
import subprocess

try:
    import google.generativeai as genai
except ImportError:
    print("The 'google-generativeai' library was not found.")
    print("Attempting to install it now...")
    try:
        # Use a more reliable way to call pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
        print("\nInstallation successful! Now attempting to import again...")
        import google.generativeai as genai
    except subprocess.CalledProcessError:
        print("\nERROR: Failed to install the 'google-generativeai' library.")
        print("Please try running 'pip install google-generativeai' manually.")
        sys.exit(1)
    except ImportError:
        print("\nERROR: The library was installed but could not be imported.")
        print("This often happens when you have multiple Python versions.")
        print("Please check which Python interpreter is running your script and which one 'pip' is installing to.")
        print("You can use the following commands in your terminal to check:")
        print("  - 'python --version' or 'python3 --version'")
        print("  - 'pip --version' or 'pip3 --version'")
        print("Make sure the paths displayed by these commands are consistent.")
        print("Exiting.")
        sys.exit(1)


def main():
    """
    The main function that runs the chatbot.
    """
    print("---------------------------------")
    print(" Welcome to the Gemini Chatbot! Ask Me Anything!")
    print("---------------------------------")
    
    # --- Ask for the user's name and store it ---
    user_name = None
    try:
        user_name = input("Bot: Before we begin, what's your name? ").strip()
    except KeyboardInterrupt:
        print("\n\nExiting chatbot. Goodbye!")
        return
    
    if not user_name:
        print("Bot: No name provided, proceeding without a personalized greeting.")
    else:
        print(f"Bot: Hello, {user_name}! I'm ready to chat.")
    # --------------------------------------------------------

    print("\nYou can start chatting. Type 'quit', 'exit', or 'bye' to end the conversation.")
 
 # Put your Google Gemini API Key below or input it at the start of the chat!
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        try:
            api_key = input("Please enter your Gemini API Key: ").strip()
        except KeyboardInterrupt:
            print("\n\nExiting chatbot. Goodbye!")
            return
    
    if not api_key:
        print("\nERROR: API Key not provided. Exiting.")
        return

    try:
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        chat = model.start_chat(history=[])

    except Exception as e:
        print(f"\nERROR: Failed to configure the model. Please check your API key and network connection.")
        print(f"Details: {e}")
        return

    while True:
        try:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ["quit", "exit", "bye"]:
                # --- Modified code: Use the stored name in the farewell message ---
                if user_name:
                    print(f"\nBot: Goodbye, {user_name}! Have a great day.")
                else:
                    print("\nBot: Goodbye! Have a great day.")
                # -----------------------------------------------------------------
                break

            if not user_input:
                continue

            print("\nBot: Thinking...")
            response = chat.send_message(user_input)

            print(f"\rBot: {response.text}")

        except KeyboardInterrupt:
            print("\n\nExiting chatbot. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()
