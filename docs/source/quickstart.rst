Quickstart
============

here is a very simple quickstart script

.. code-block:: python

    from WarEraAPI import WarEraClient
    import asyncio

    async def main():
        # Initialize client with API key (optional)
        client = WarEraClient(api_key="your_api_key_here")

        # get user id
        userId = input("Type the id of the user you want to fetch: ")
        
        # Get user information
        user = await client.get_user(userId=userId)
        print(user)
        

    # Run the async function
    asyncio.run(main())