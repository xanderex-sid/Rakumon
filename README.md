# Rakumon
The Rakumon 🤖 : Your Real Life Doraemon
------------------------------------------------------------------------------------------------------------------------------------

⭐ Don't forget to star this project! We welcome contributions, new features, and fresh ideas.

## Introduction

Let's take a scenario 🙋‍♂️,

Whenever you go shopping with your family or friends, you might enter a clothing store filled with a wide variety of shirts, T-shirts, jeans, trousers, pants, socks, belts, and what not! The sheer number of options can be overwhelming, making it difficult to decide. Let's say you're looking for your dream shirt—the perfect design, fabric, and color. However, finding that exact shirt can be challenging. Often, you either settle for something else with a bit of disappointment, or you leave the store still searching for that dream shirt.

That’s where the shopkeeper comes in. The shopkeeper knows exactly where your dream shirt is. They understand your personalized specifications and help you find your dream shirt, so you don’t have to search for it yourself.

Also, Your family and friends who are with you always help you find exactly what you need.

Wouldn't it be great if you could get these personalizations—the help from the shopkeeper, family, and friends—on your e-commerce platform? Think about how much easier online shopping would be if you didn't have to figure everything out on your own.

That’s where Rakumon comes in. It’s a new type of e-commerce platform, a system where you have your own personalized online shopkeeper (AI). Where you can add your family and friends so all of you can shop online together. You can chat with each other, browse products together, and get personalized product recommendations and descriptions tailored to your needs from your online shopkeeper — THE RAKUMON 🤖.

## Demo Video

[![Rakumon](https://img.youtube.com/vi/KWtN9PD8FGo/0.jpg)](https://www.youtube.com/watch?v=KWtN9PD8FGo)


Click on the video above or <a href="https://www.youtube.com/watch?v=KWtN9PD8FGo">here</a> to watch the demo.


## Detailed Approach

![Detailed Approach](https://github.com/RustyGrackle/Rakumon/blob/main/readme_content/detailed_approach.jpg)

## Try It Yourself!

### NOTE: Necessary Step

You need to create your own dataset and vector database. You can then retrieve products using Pinecone (recommended) or FAISS.
After creating your own dataset and vector database, please update the code in the necessary files as needed, especially `query_service_agent.py`.

If you want to access our vector database of products and our Pinecone retrieval method, or if you need help creating your own RAG, please contact these members of the project.

1. Snehanshu Mukherjee
- 21je0928@iitism.ac.in ( To gain access to our data, get help, or fully understand how to create your own RAG pipeline. )

2. Siddharth Mishra
- 21je0918@iitism.ac.in ( If you need help creating and integrating your own RAG pipeline with the chat agent in the project. )

### STEPS

1. If you have completed the 'Necessary Step' as provided above, First run the `query_service_agent.py` file. It will run the RAG pipeline.
   ```
   python3 query_service_agent.py
   ```
2. Second, run the `gemini_chat_agent.py` file. It will run the Chat agent pipeline.
   ```
   python3 gemini_chat_agent.py
   ```
3. Finally, run the `main.py` file. It will start the project on localhost, allowing you to interact with Rakumon. Feel free to add or update user details in `users.json`, and then change the user ID in the `main.py` file accordingly.
   ```
   python3 main.py
   ```

## Members of This Project

I want to extend my heartfelt thanks to every member of this project and their contributions. This project would not have been possible without them.

1. Snehanshu Mukherjee,  `email:` 21je0928@iitism.ac.in

- Thank you for leading this project and being the primary source of ideation of this project. Your contributions to creating data of e-commerce products, creating and enhancing the full RAG pipeline have been truly invaluable.

2. Gurleen Kaur Gill, `email:` and,
3. AVNEET KAUR, `email:` 

- Thank you for your exceptional UI/UX design work, creating the complete frontend pipeline, and designing the web framework. This project would not have succeeded in Rakathon without both of you on our team.

4. Siddharth Mishra, `email` 21je0918@iitism.ac.in

- I want to thank my team for their support. Creating the full pipeline, integrating each part (frontend, backend, AI agents) of the project, and developing the chat agent and AG component of the RAG would not have been possible without the constant feedback from my teammates.

## Final Words

Rakumon is still in its early stages, and we’re eager to make it even better. We welcome contributions, new features, and fresh ideas. If you’re interested in contributing or want to learn more about the project, please feel free to reach out to us.


