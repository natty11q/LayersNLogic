simpleGui is missing various event types such as a mose move event and its harder to get the mouse position. 
Due to me having implemented a custom event system, I am able to hook the application up to a different api that can get certain events for me and have those be dispatched by the engine

This means that the game code does not need to be modifided other than having the option to hook the game up to new event types



