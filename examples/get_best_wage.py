from WarEraAPI import WarEraClient
from WarEraAPI import WorkOffer

import asyncio


async def main(
    energy: int | None = None,
    production: int | None = None
):

    client = WarEraClient(rate_limit=100)
    offers: list[WorkOffer] = []
    cursor = None

    # fetch all the job offers
    while True:

        work_offers = await client.get_work_offers(
            limit=100,
            cursor=cursor,
            energy=energy or 0,
            production=production or 0
        )
        cursor = work_offers[1]

        for work_offer in work_offers[0]:

            offers.append(work_offer)

        if cursor is None:
            break
        
    # sort them
    best_offers = sorted(
        offers,
        key=(lambda x: x.wageAfterTax),
        reverse=True
    )

    print("Here is the top 10 offers for your level!")
    for offer in best_offers[:10]:
        print(f"https://app.warera.io/company/{offer.company} ~ {offer.wageAfterTax:.3f}Coins")


if __name__ == "__main__":

    energy = input("what is your current energy ?: ")
    production = input("what is your current production ?: ")
    asyncio.run(main(
        energy=int(energy),
        production=int(production)
    ))