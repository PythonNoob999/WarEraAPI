'''this script is used to get the best production
bonus for each item to know which item is most profitable
to produce'''

from WarEraAPI import WarEraClient
from WarEraAPI.types import Region
from WarEraAPI.types import ITEM
from typing import get_args

import asyncio


async def get_item_bonuses(
    client: WarEraClient,
    target: ITEM | None = None
) -> dict[ITEM, tuple[str, float]]:
    
    _items = get_args(ITEM)
    bonuses: dict[ITEM, tuple[str, float]] = {}
    eligible_items: int = 18
    cursor: str = ""
    regions: dict[str, Region] = {
        r._id: r for r in await client.get_all_regions()
    }

    while (
        (cursor is not None)
        and
        (len(bonuses.keys()) != eligible_items)
    ):
        
        companies, cursor = await client.get_companies(
            cursor=cursor,
            limit=80,
            return_companies=True
        )

        for company in companies:

            if company.itemCode not in bonuses:

                recommended = await client.get_company_recommended_regions(
                    companyId=company._id
                )

                best_region: tuple[str, float] = ("null", float("-inf"))
                
                for region in recommended:

                    if region.bonus > best_region[1]:
                        best_region = (regions[region.regionId].name, region.bonus)
                
                bonuses[company.itemCode] = best_region

                if company.itemCode == target:
                    return {target: best_region}

                print(f"Found {company.itemCode} Best Bonus!, {len(bonuses.keys())}/{eligible_items}")
    
    return bonuses


async def main():

    print(
        "Which item do you want to fetch its bonus?\n"
        "1. iron                2. limestone\n"
        "3. petroleum           4. grain\n"
        "5. lead                6. mysterious plant\n"
        "7. livestock           8. fish\n"
        "9. cookedFish          10.bread\n"
        "11. concrete           12. steel\n"
        "13. oil                14. steak\n"
        "15. lightAmmo (green)  16. ammo (blue)\n"
        "17. heavyAmmo (purple) 18. cocaine (pill)\n"
        "19. ALL                20. exit"
    )
    ans = input("> ")
    choices: dict[str,ITEM | str] = {
        "1": "iron",
        "2": "limestone",
        "3": "petroleum",
        "4": "grain",
        "5": "lead",
        "6": "coca",
        "7": "livestock",
        "8": "fish",
        "9": "cookedFish",
        "10": "bread",
        "11": "concrete",
        "12": "steel",
        "13": "oil",
        "14": "steak",
        "15": "lightAmmo",
        "16": "ammo",
        "17": "heavyAmmo",
        "18": "cocain",
        "19": "ALL",
        "20": "exit"
    }

    choice = choices.get(ans.strip(), None)

    if choice is None:
        print("Unknown option, exiting...")
        exit(0)
    
    client = WarEraClient(rate_limit=100)
    
    print("Fetching Bonuses...")
    result = await get_item_bonuses(
        client=client,
        target=choice if choice != "ALL" else None
    )

    for item, bonus in result.items():

        print(f"[{item}] {bonus[1]:.1f}% Bonus in {bonus[0]}")
    
    print(">>>END<<<")


if __name__ == "__main__":

    asyncio.run(main())