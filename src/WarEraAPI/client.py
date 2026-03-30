from aiohttp import ClientSession
from typing import Literal, Any

from WarEraAPI.types import *
from WarEraAPI.types.constants import ITEM
from WarEraAPI.types.constants import EVENT_TYPES
from WarEraAPI.types.constants import BattleHit
from WarEraAPI.utils import edit_types


class WarEraClient:


    def __init__(self, api_key: str | None = None):

        self.api_key = api_key
        self.uri = "https://api2.warera.io/trpc/"
    

    def sanitize_response(
        self,
        data: dict | list
    ) -> None:
        

        if isinstance(data, dict):
        
            ktr = []

            for k,v in data.items():

                if isinstance(k,str) and k.startswith("__"):
                    ktr.append(k)

                elif isinstance(v, dict):
                    self.sanitize_response(data=v)
                
                elif isinstance(v, list):

                    for item in v:

                        if not isinstance(item, dict):
                            continue

                        self.sanitize_response(data=item)
            
            for k in ktr:
                data.pop(k)
        
        elif isinstance(data, list):

            for item in data:
                self.sanitize_response(
                    data=item
                )
        

    async def request(
        self,
        method: Literal["GET", "POST"],
        endpoint: str,
        headers: dict | None = None,
        body: dict | None = None
    ) -> Any:
        
        if headers is None:
            headers = {}
        
        headers["Content-Type"] = "application/json"
        
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        
        async with ClientSession() as api:

            async with api.request(
                method,
                self.uri+"/"+endpoint,
                headers=headers,
                json=body
            ) as resp:
                try:
                    response = (await resp.json())["result"]["data"]
                except KeyError:
                    print(await resp.json())
                    exit(1)
                self.sanitize_response(response)
                return response

    # Company

    async def get_company(
        self,
        companyId: str = "String"
    ) -> Company:
        
        result = await self.request(
            method="POST",
            endpoint="company.getById",
            body={
                "companyId": companyId
            }
        )
        
        return Company(**result)
    

    async def get_companies(
        self,
        userId: str | None = None,
        cursor: str | None = None,
        perPage: int = 10,
        return_companies: bool = False
    ) -> tuple[list[str] | list[Company], str]:
        '''
        company.getCompanies endpoint
        
        :param userId: filter companies by user
        :type userId: str | None
        :param cursor: used for pagination
        :type cursor: str | None
        :param perPage: number of results per query
        :type perPage: int
        :param return_companies: whether to return the Companies as list[Company] instead of list[str] (the ids)
        :type return_companies: bool
        :return: tuple[0] = list[str] or list[Company], tuple[1] = next_cursor (use it for next page in the "cursor" argument) 
        :rtype: tuple[list[str] | list[Company], str]
        '''
        
        result = await self.request(
            method="POST",
            endpoint="company.getCompanies",
            body={
                "userId": userId or "",
                "perPage": perPage,
                "cursor": cursor or ""
            }
        )

        items = result["items"]

        if return_companies:

            items = [
                (await self.get_company(companyId=cid))
                for cid in items
            ]

        return (
            items,
            result["nextCursor"]
        )
    

    # Countries

    async def get_country(
        self,
        countryId: str
    ) -> Country:
        
        result = await self.request(
            method="POST",
            endpoint="country.getCountryById",
            body={
                "countryId": countryId
            }
        )

        return Country(**result)
    
    
    async def get_all_countries(
        self,
    ) -> list[Country]:
        
        result = await self.request(
            method="POST",
            endpoint="country.getAllCountries"
        )

        return [
            Country(**country) for country in result
        ]
    

    # Events

    async def get_events(
        self,
        limit: int = 10,
        cursor: str | None = None,
        countryId: str | None = None,
        eventTypes: list[EVENT_TYPES] | None = None
    ) -> list[Event]:
        
        result = await self.request(
            method="POST",
            endpoint="event.getEventsPaginated",
            body={
                "limit": limit,
                "countryId": countryId or "",
                "cursor": cursor or "",
                "eventTypes": eventTypes or []
            }
        )

        return [
            Event(**event) for event in result
        ]
    

    # Government

    async def get_government(
        self,
        countryId: str
    ) -> Government:
        
        result = await self.request(
            method="POST",
            endpoint="government.getByCountryId",
            body={
                "countryId": countryId
            }
        )

        return Government(**result)
    

    # Region

    async def get_region(
        self,
        regionId: str
    ) -> Region:
        
        result = await self.request(
            method="POST",
            endpoint="region.getById",
            body={
                "regionId": regionId
            }
        )

        return Region(
            **result
        )
    

    async def get_all_regions(
        self
    ) -> list[Region]:
        
        result = await self.request(
            method="POST",
            endpoint="region.getRegionsObject"
        )
        
        return [
            Region(**region) for region in result.values()
        ]
    

    # Battles

    async def get_battle(
        self,
        battleId: str
    ) -> Battle:
        
        result = await self.request(
            method="POST",
            endpoint="battle.getById",
            body={
                "battleId": battleId
            }
        )

        return Battle(**result)
    

    async def get_battles(
        self,
        isActive: bool = True,
        limit: int = 10,
        cursor: str | None = None,
        direction: str = "forward",
        filter: str = "all",
        defenderRegionId: str | None = None,
        warId: str | None = None,
        countryId: str | None = None
    ) -> list[Battle]:
        
        result = await self.request(
            method="POST",
            endpoint="battle.getBattles",
            body={
                "isActive": isActive,
                "limit": limit,
                "cursor": cursor or "",
                "direction": direction,
                "filter": filter,
                "defenderRegionId": defenderRegionId or "",
                "warId": warId or "",
                "countryId": countryId or ""
            }
        )

        return [
            Battle(**battle) for battle in result["items"]
        ]
    

    async def get_live_battle_data(
        self,
        battleId: str,
        roundNumber: int = 0
    ) -> BattleData:
        
        result = await self.request(
            method="POST",
            endpoint="battle.getLiveBattleData",
            body={
                "battleId": battleId,
                "roundNumber": roundNumber
            }
        )

        return BattleData(**result)
    

    # Round

    async def get_round(
        self,
        roundId: str
    ) -> Round:
        
        result = await self.request(
            method="POST",
            endpoint="round.getById",
            body={
                "roundId": roundId
            }
        )

        return Round(**result)
    

    async def get_round_last_hits(
        self,
        roundId: str
    ) -> tuple[list[BattleHit], list[BattleHit]]:
        
        result = await self.request(
            method="POST",
            endpoint="round.getLastHits",
            body={
                "roundId": roundId
            }
        )

        for item in (result["attacker"] + result["defender"]):
            edit_types(
                obj=item,
                class_overwrite=BattleHit
            )

        return (
            result["attacker"],
            result["defender"]
        )
    

    # BattleRankings
    # TBC


    # ItemTrading

    async def get_prices(
        self
    ) -> dict[ITEM, float]:
        
        result = await self.request(
            method="POST",
            endpoint="itemTrading.getPrices"
        )

        return result

    # Workers

    async def get_workers(
        self,
        companyId: str,
        userId: str | None = None
    ) -> list[Worker]:
        
        result = await self.request(
            method="POST",
            endpoint="worker.getWorkers",
            body={
                "companyId": companyId,
                "userId": userId or ""
            }
        )

        return [
            Worker(
                **worker
            )
            for worker in result["workers"]
        ]