# Wren: Your AI Motivational Coach via Discord
## Project Roadmap & Future Enhancements:

This project is currently a prototype with the following planned enhancements:

<!-- 1.  [ ]**WhatsApp Integration**: Transition from basic SMS support to full WhatsApp messaging capabilities.
    1.  Implementing whatsapp with twilio seems like a hassle. I'm going to find some alternatives for whatsapp bots.
    2.  It seems like Meta developers may be a way to go. 
 -->

1. [ ] **Discord Integration**: Use discord as the main chat interface instead of whatsapp, ideally be able to generalize into various MCP text-based channels 
   - Future: Augment to voice / various ways to accept infromation
2.  [ ] **Advanced Agentic Features**: Incorporate more sophisticated agentic functionalities beyond a basic chat client.
    -  What are things your coach does for you, other than just chat? 
        - [ ] Your coach can help you set goals and track progress and celebrate your milestones (see goal management web app repo for core logic). **main change**: App -> MCP.
    - [ ]  I'm thinking of adding planning and habit building abilities (see habit builder repo).
    - [ ] I'm thinking of adding scheduling capabilities.
3.  [ ] **Persistent Memory**: Migrate conversation memory from local file storage to a robust database solution, enabling advanced search and recollection features.
    - [ ] I'm thinking about adding a vector database to store embeddings of conversations, goals, actions, events, notes, and reminders.
