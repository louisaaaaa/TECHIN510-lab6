import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import random

# Load API Key
load_dotenv()
API_KEY = os.getenv('API_KEY')
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Predefined Situations with Answers (Dictionary format)
situations = [
        {
            "question": "Several people attend a party at the home of a murderer. All the guests end up dead except for one man. How did he survive?",
            "answer": "The host served everyone drinks with poisoned ice cubes. The other party guests sipped their drinks while the poison slowly melted. The survivor drank his immediately in one gulp before the ice melted."
        },
    ]

# Function to generate yes/no answers using Gemini
def generate_answer(prompt, chosen_situation):
  """Generates a yes/no answer to the given prompt using Gemini"""
  prompt = "This is a situation puzzle, the situation is:" + chosen_situation+ " The question is: "+ prompt + "Please try to answer it with only yes or no. If you can't answer it with yes or no, tell me that you can't answer yes or no to that question. Try rephrasing it."
  response = model.generate_content(prompt)
  answer = response.text.strip().lower()
  print(answer)
  if "yes" in answer or "no" in answer:
    return answer
  else:
    return "I can't answer yes or no to that question. Try rephrasing it."

# Function to generate score for the user's guess
def generate_score(prompt, answer):
  prompt = "This is a situation puzzle, the answer is:" + answer+ " The user's answer is: "+ prompt + "Please give the user the corrent answer and tell them how their answer is, score their answer out of 10 and give them some advice on how to get a more accurate answer next time."
  response = model.generate_content(prompt)
  my_answer = response.text.strip().lower()
  return my_answer

# Main App Function
def main():
  # Choose a random situation question
  chosen_situation, answer = random.choice(situations).values()
  print(chosen_situation)
  print(answer)
  # Title and Instructions
  st.title("Situation Puzzle Game")
  image = "situation.png"  # Change this to the path of your image file
  st.image(image, caption='Are you ready?', width=300)
  st.write("Welcome! Situation puzzles, also known as lateral thinking puzzles or \"yes or no\" puzzles, are puzzles that require players to ask yes or no questions to determine what happened in a situation. Play with me, try to guess the answer and see how close you got!")

  # Display Situation
  st.subheader("Situation:")
  
  # Randomly select a situation
  st.write(chosen_situation)

  # User Input for Question
  user_question = st.text_input("Ask me a yes or no question:")

  # Generate Answer Button
  if st.button("Ask me!"):
    if user_question:
      generated_answer = generate_answer(user_question, chosen_situation)
      st.write("My Answer:", generated_answer)
    else:
      st.warning("Please enter a question!")

  # Check Guess and Display Score
  user_answer = st.text_input("When you're ready give me your answer!")
  if st.button("Guess!"):
    if user_answer:
      generated_answer = generate_score(user_answer, answer)
      st.write("Results:", generated_answer)
    else:
      st.warning("Please enter your guess!")

# Run the App
if __name__ == "__main__":
  main()
