from aiohttp import ClientSession, ContentTypeError
from typing import Literal, Any

from WarEraAPI.types import *
from WarEraAPI.utils import edit_types
from WarEraAPI.utils import pretty_json
from WarEraAPI.errors import APIError
from WarEraAPI.errors import TransactionTypeNotSupported
from WarEraAPI.errors import NoAvailableServer

import asyncio


class WarEraClient:


    def __init__(
        self,
        api_key: str | None = None,
        rate_limit: int = 200
    ):
        '''
        WarEraClient.__init__
        
        :param api_key: Your API_KEY from the game (optional)
        :type api_key: str | None
        :param rate_limit: amount of requests sent per minute max
        :type rate_limit: int
        '''

        self.api_key: str | None = api_key

        if api_key is None:
            rate_limit = 100

        self.uri: str = "https://api2.warera.io/trpc"
        self.rate_limit: int = rate_limit
        self._semaphore = asyncio.Semaphore(rate_limit)
        self._refill_task = None


    async def _refill_loop(self):
        while True:
            await asyncio.sleep(60)

            to_add = self.rate_limit - self._semaphore._value
            for _ in range(to_add):
                self._semaphore.release()


    def _ensure_refill_running(self):
        if self._refill_task is None:
            self._refill_task = asyncio.create_task(self._refill_loop())


    def sanitize_response(
        self,
        data: dict | list[dict]
    ) -> None:
        '''
        WarEraClient.sanitize_response()
        
        :param data: the raw api response
        :type data: dict | list[dict]
        '''
        

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
    

    def sanitize_body(
        self,
        body: dict
    ) -> None:
        
        ktr = []

        for k,v in body.items():

            if v == "":
                ktr.append(k)
        
        for k in ktr:
            body.pop(k)
        

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
        
        if isinstance(body, dict):
            self.sanitize_body(body)

        self._ensure_refill_running()
        await self._semaphore.acquire()

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
                    raise APIError(pretty_json(await resp.json()))
                except ContentTypeError:
                    if resp.status == 503:
                        raise NoAvailableServer
                    raise APIError(await resp.text())
                self.sanitize_response(response)
                return response

    # Company

    async def get_company(
        self,
        companyId: str = "String"
    ) -> Company:
        '''
        company.get_company endpoint
        
        :param companyId: the company Id
        :type companyId: str
        :return: returns Company object on success
        :rtype: Company
        '''
        
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
        limit: int = 10,
        return_companies: bool = False
    ) -> tuple[list[str] | list[Company], str | None]:
        '''
        company.getCompanies endpoint
        
        :param userId: filter companies by user
        :type userId: str | None
        :param cursor: used for pagination
        :type cursor: str | None
        :param limit: number of results per query
        :type limit: int
        :param return_companies: whether to return the Companies as list[Company] instead of list[str] (the ids)
        :type return_companies: bool
        :return: tuple[0] = list[str] or list[Company], tuple[1] = next_cursor (use it for next page in the "cursor" argument) 
        :rtype: tuple[list[str] | list[Company], str | None]
        '''
        
        result = await self.request(
            method="POST",
            endpoint="company.getCompanies",
            body={
                "userId": userId or "",
                "perPage": limit,
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
            result.get("nextCursor")
        )
    

    async def get_company_recommended_regions(
        self,
        companyId: str
    ) -> list[RecommendedRegion]:
        '''
        company.get_company_recommended_regions
        
        :param companyId: the company Id
        :type companyId: str
        :return: a list of RecommendedRegion objects (not sorted)
        :rtype: list[RecommendedRegion]
        '''
        
        result = await self.request(
            method="POST",
            endpoint="company.getRecommendedRegionIds",
            body={
                "companyId": companyId
            }
        )

        return [
            RecommendedRegion(**region) for region in result
        ]


    async def get_company_production_bonus(
        self,
        companyId: str
    ) -> ProductionBonus:
        '''
        company.get_company_production_bonus
        
        :param companyId: the company Id
        :type companyId: str
        :return: returns ProductionBonus object for that company
        :rtype: ProductionBonus
        '''
        
        result = await self.request(
            method="POST",
            endpoint="company.getProductionBonus",
            body={
                "companyId": companyId
            }
        )

        return ProductionBonus(**result)

    # BattleRankings (not implemented currently)


    # tradingOrder

    async def get_top_orders(
        self,
        itemCode: ITEM,
        limit: int = 10
    ) -> tuple[list[TradingOrder], list[TradingOrder]]:
        '''
        tradingOrder.get_top_orders
        gets the top orders for an item
        
        :param itemCode: the item Code
        :type itemCode: ITEM
        :param limit: amount of orders returned
        :type limit: int
        :return: a tuple with the first index holding the buyOrders and the second holding the sellOrders
        :rtype: tuple[list[TradingOrder], list[TradingOrder]]
        '''
        
        result = await self.request(
            method="POST",
            endpoint="tradingOrder.getTopOrders",
            body={
                "itemCode": itemCode,
                "limit": limit
            }
        )

        return (
            [
                TradingOrder(**order) for order in result["buyOrders"]
            ],
            [
                TradingOrder(**order) for order in result["sellOrders"]
            ]
        )
    

    # itemOffer (not implemented currently)


    # workOffer

    async def get_work_offer(
        self,
        workOfferId: str
    ) -> WorkOffer:
        '''
        workOffer.get_work_offer
        get info about a work offer
        
        :param workOfferId: the work offer Id
        :type workOfferId: str
        :return: WorkOffer object
        :rtype: WorkOffer
        '''
        
        result = await self.request(
            method="POST",
            endpoint="workOffer.getById",
            body={
                "workOfferId": workOfferId
            }
        )

        return WorkOffer(**result)
    

    async def get_company_work_offer(
        self,
        companyId: str
    ) -> WorkOffer:
        '''
        workOffer.get_company_work_offer
        get work offer for a certain company
        
        :param companyId: the company Id
        :type companyId: str
        :return: a WorkOffer object
        :rtype: WorkOffer
        '''
        
        result = await self.request(
            method="POST",
            endpoint="workOffer.getWorkOfferByCompanyId",
            body={
                "companyId": companyId
            }
        )

        return WorkOffer(**result)
    

    async def get_work_offers(
        self,
        regionId: str | None = None,
        userId: str | None = None,
        cursor: str | None = None,
        limit: int = 10,
        energy: int = 0,
        production: int = 0,
        citizenship: str | None = None,
    ) -> tuple[list[WorkOffer], str | None]:
        '''
        workOffer.get_work_offers
        get many work offers and optionally filter them
        by region, user or citizenship
        
        :param regionId: the region Id
        :type regionId: str | None
        :param userId: the user Id
        :type userId: str | None
        :param cursor: the key for fetching the next page results
        :type cursor: str | None
        :param limit: the amount of WorkOffer's returned
        :type limit: int
        :param energy: the min energy requirement
        :type energy: int
        :param production: the min production requirement
        :type production: int
        :param citizenship: the country name
        :type citizenship: str | None
        :return: tuple with the first index holding the WorkOffer objects and the second having the next cursor (optional)
        :rtype: tuple[list[WorkOffer], str | None]
        '''
        
        result = await self.request(
            method="POST",
            endpoint="workOffer.getWorkOffersPaginated",
            body={
                "userId": userId or "",
                "regionId": regionId or "",
                "cursor": cursor or "",
                "limit": limit,
                "energy": energy,
                "production": production,
                "citizenship": citizenship or ""
            }
        )

        return (
            [
            WorkOffer(**work_offer) for work_offer in result["items"]
            ],
            result.get("nextCursor")
        )
    
    # ranking

    async def get_rankings(
        self,
        type: RANKING_TYPE
    ) -> Rankings:
        '''
        ranking.get_rankings
        get the current rankings of RANKING_TYPE
        
        :param type: the ranking type
        :type type: RANKING_TYPE
        :return: Rankings object
        :rtype: Rankings
        '''
        
        result = await self.request(
            method="POST",
            endpoint="ranking.getRanking",
            body={
                "rankingType": type
            }
        )

        return Rankings(**result)
    

    # search

    async def search(
        self,
        searchText: str
    ) -> SearchResult:
        '''
        search.searchAnything
        search for any user,region,country,party or Mu by text search
        
        :param searchText: the text to search with
        :type searchText: str
        :return: SearchResult object
        :rtype: SearchResult
        '''

        result = await self.request(
            method="POST",
            endpoint="search.searchAnything",
            body={
                "searchText": searchText
            }
        )

        return SearchResult(**result)
    

    # gameConfig

    async def get_game_dates(
        self,
    ) -> GameDates:
        '''
        gameConfig.get_game_dates
        
        :param self: Description
        :return: Description
        :rtype: GameDates
        '''

        result = await self.request(
            method="POST",
            endpoint="gameConfig.getDates"
        )

        return GameDates(**result)
    

    # user

    async def get_user_lite(
        self,
        userId: str
    ) -> User:
        '''
        user.get_user_lite
        get less info about user
        
        :param userId: the user Id
        :type userId: str
        :return: a User object with all of its optional fields set to None
        :rtype: User
        '''
        
        result = await self.request(
            method="POST",
            endpoint="user.getUserLite",
            body={
                "userId": userId
            }
        )

        return User(**result)


    async def get_user(
        self,
        userId: str
    ) -> User:
        '''
        user.get_user
        get info about a user
        
        :param userId: the user Id
        :type userId: str
        :return: a User object
        :rtype: User
        '''
        
        result = await self.request(
            method="POST",
            endpoint="user.getUserById",
            body={
                "userId": userId
            }
        )

        return User(**result)
    

    async def get_country_users(
        self,
        countryId: str,
        limit: int = 10,
        cursor: str | None = None,
        return_users: bool = False
    ) -> tuple[list[User] | dict[str, str], str | None]:
        '''
        user.get_country_users
        get users from a certain country
        
        :param countryId: the country Id
        :type countryId: str
        :param limit: the amount of users returned with each page
        :type limit: int
        :param cursor: the key for fetching the next page results
        :type cursor: str | None
        :param return_users: wether to return User objects or just user Ids
        :type return_users: bool
        :return: a tuple with the first index holding a list of User objects (or dict[str, str] in case of return_users=False) and the second index holding the next cursor (optional)
        :rtype: tuple[list[User] | dict[str, str], str | None]
        '''
        
        result = await self.request(
            method="POST",
            endpoint="user.getUsersByCountry",
            body={
                "countryId": countryId,
                "limit": limit,
                "cursor": cursor or ""
            }
        )
        items = result["items"]

        if return_users:

            new_items = []

            for item in items:

                user = await self.get_user(
                    userId=item["_id"]
                )
                new_items.append(user)
            
            items = new_items
        
        return (
            items,
            result.get("nextCursor")
        )
    

    # Article

    async def get_article(
        self,
        articleId: str
    ) -> Article:
        '''
        article.get_article
        get info about an article
        
        :param articleId: the article Id
        :type articleId: str
        :return: an Article object
        :rtype: Article
        '''
        
        result = await self.request(
            method="POST",
            endpoint="article.getArticleById",
            body={
                "articleId": articleId
            }
        )

        return Article(**result)


    async def get_article_lite(
        self,
        articleId: str
    ) -> Article:
        '''
        article.get_article_lite
        get less info about an Article
        
        :param articleId: the article Id
        :type articleId: str
        :return: an Article object with all of its optional fields set to None
        :rtype: Article
        '''
        
        result = await self.request(
            method="POST",
            endpoint="article.getArticleLiteById",
            body={
                "articleId": articleId
            }
        )

        return Article(**result)


    async def get_articles(
        self,
        type: ARTICLE_TYPE,
        limit: int = 10,
        cursor: str | None = None,
        userId: str | None = None,
        categories: list[ARTICLE_CATEGORY] | None = None,
        languages: list[str] | None = None,
        positiveScoreOnly: bool = False
    ) -> tuple[list[Article], str | None]:
        '''
        article.get_articles
        get many articles with optional filtering
        with article_type,categories an languages
        
        :param type: the type of returned articles
        :type type: ARTICLE_TYPE
        :param limit: the amount of Articles returned
        :type limit: int
        :param cursor: the key for fetching the next page results
        :type cursor: str | None
        :param userId: the user Id
        :type userId: str | None
        :param categories: a list of ARTICLE_CATEGORY to filter with
        :type categories: list[ARTICLE_CATEGORY] | None
        :param languages: a list of languages to filter with
        :type languages: list[str] | None
        :param positiveScoreOnly: wether to return only positive articles or not (positive = article with > 0 (likes-dislikes))
        :type positiveScoreOnly: bool
        :return: a tuple with the first index holding a list of Article objects and the second holding the next cursor (optional)
        :rtype: tuple[list[Article], str | None]
        '''
        
        result = await self.request(
            method="POST",
            endpoint="article.getArticlesPaginated",
            body={
                "type": type,
                "limit": limit,
                "cursor": cursor or "",
                "userId": userId or "",
                "categories": categories or "",
                "languages": languages or "",
                "positiveScoreOnly": positiveScoreOnly
            }
        )

        return (
            [
                Article(**article) for article in result["items"]
            ],
            result.get("nextCursor")
        )
    
    # Military Units

    async def get_mu(
        self,
        muId: str
    ) -> MilitaryUnit:
        '''
        mu.get_mu
        get info about a military unit
        
        :param muId: the military unit Id
        :type muId: str
        :return: a MilitaryUnit object
        :rtype: MilitaryUnit
        '''

        result = await self.request(
            method="POST",
            endpoint="mu.getById",
            body={
                "muId": muId
            }
        )

        return MilitaryUnit(**result)


    async def get_many_mu(
        self,
        limit: int = 10,
        cursor: str | None = None,
        memberId: str | None = None,
        userId: str | None = None,
        search: str | None = None
    ) -> tuple[list[MilitaryUnit], str | None]:
        '''
        mu.get_many_mu
        get many MilitaryUnits with optional filtering
        with member,user Id or search
        
        :param limit: the amount of returned MilitaryUnit objects
        :type limit: int
        :param cursor: the key for fetching the next page results
        :type cursor: str | None
        :param memberId: an optional member Id
        :type memberId: str | None
        :param userId: an optional user Id
        :type userId: str | None
        :param search: optional text to filter with
        :type search: str | None
        :return: a tuple with first index holding the list of MilitaryUnit objects and the second holding the next cursor (optional)
        :rtype: tuple[list[MilitaryUnit], str | None]
        '''

        result = await self.request(
            method="POST",
            endpoint="mu.getManyPaginated",
            body={
                "limit": limit,
                "cursor": cursor or "",
                "memberId": memberId or "",
                "userId": userId or "",
                "search": search or ""
            }
        )

        return (
            [
                MilitaryUnit(**mu) for mu in result["items"]
            ],
            result.get("nextCursor")
        )
    

    # Transactions

    async def get_transactions(
        self,
        transactionType: TRANSACTION_TYPE,
        limit: int = 10,
        cursor: str | None = None,
        userId: str | None = None,
        muId: str | None = None,
        countryId: str | None = None,
        partyId: str | None = None,
        itemCode: ITEM | ITEM_MARKET_CODE | None = None,
    ) -> tuple[list[Transaction], str | None]:
        '''
        transaction.get_transactions
        get many transactions with optional filtering
        with user,mu,country,party Id or itemCode depending on transactionType
        
        :param transactionType: the transaction type to filter
        :type transactionType: TRANSACTION_TYPE
        :param limit: the amount of transactions returned
        :type limit: int
        :param cursor: the key for fetching the next page results
        :type cursor: str | None
        :param userId: optional userId to filter with
        :type userId: str | None
        :param muId: optional military unit Id to filter with
        :type muId: str | None
        :param countryId: optional country Id to filter with
        :type countryId: str | None
        :param partyId: optional party Id to filter with
        :type partyId: str | None
        :param itemCode: the item code to filter with (ITEM for supplies and ITEM_MARKET_CODE for equipments)
        :type itemCode: ITEM | ITEM_MARKET_CODE | None
        :return: a tuple with its first index holding the list of Transaction Objects and the second optionally holding the next Cursor
        :rtype: tuple[list[Transaction], str | None]
        '''
        
        result = await self.request(
            method="POST",
            endpoint="transaction.getPaginatedTransactions",
            body={
                "transactionType": transactionType,
                "limit": limit,
                "cursor": cursor or "",
                "userId": userId or "",
                "muId": muId or "",
                "countryId": countryId or "",
                "partyId": partyId or "",
                "itemCode": itemCode or ""
            }
        )

        _type = None

        if transactionType in TransactionMapping:
            _type = TransactionMapping[transactionType]
        
        else:
            raise TransactionTypeNotSupported(tx_type=transactionType)

        return (
            [
                _type(**tx) for tx in result["items"]
            ],
            result.get("nextCursor", None)
        )
    
    
    # Upgrade

    async def get_entity_upgrade(
        self,
        upgradeType: UPGRADE_TYPE,
        regionId: str | None = None,
        muId: str | None = None,
        companyId: str | None = None
    ) -> EntityUpgrade:
        '''
        upgrade.get_entity_upgrade
        get the current upgrades this entity have
        entity is a region,mu or company
        
        :param upgradeType: the upgrade type to fetch
        :type upgradeType: UPGRADE_TYPE
        :param regionId: the region Id
        :type regionId: str | None
        :param muId: the military unit Id
        :type muId: str | None
        :param companyId: the company Id
        :type companyId: str | None
        :return: a EntityUpgrade object
        :rtype: EntityUpgrade
        '''
        
        result = await self.request(
            method="POST",
            endpoint="upgrade.getUpgradeByTypeAndEntity",
            body={
                "upgradeType": upgradeType,
                "regionId": regionId or "",
                "muId": muId or "",
                "companyId": companyId or ""
            }
        )

        return EntityUpgrade(
            **result
        )

    # Countries

    async def get_country(
        self,
        countryId: str
    ) -> Country:
        '''
        country.get_country
        get info about a country
        
        :param countryId: the country Id
        :type countryId: str
        :return: a Country object
        :rtype: Country
        '''
        
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
        '''
        country.get_all_countries
        get all the countries
        
        :return: a list of Country objects
        :rtype: list[Country]
        '''
        
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
    ) -> tuple[list[Event], str | None]:
        '''
        event.get_events
        get a list of events and optionally filter with Country Id
        
        :param limit: the amount of events returned
        :type limit: int
        :param cursor: the key for fetching the next page results
        :type cursor: str | None
        :param countryId: an optional Country Id to filter ITs events
        :type countryId: str | None
        :param eventTypes: specific event type to fetch (optional)
        :type eventTypes: list[EVENT_TYPES] | None
        :return: a tuple with the first index holding list of Event objects and the second optionally holding the next cursor
        :rtype: tuple[list[Event], str | None]
        '''
        
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

        return (
            [
            Event(**event) for event in result
            ],
            result.get("nextCursor")
        )
    

    # Government

    async def get_government(
        self,
        countryId: str
    ) -> Government:
        '''
        government.get_government
        get info about a country's government
        
        :param countryId: the country Id
        :type countryId: str
        :return: a Government object
        :rtype: Government
        '''
        
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
        '''
        region.get_region
        get region info
        
        :param regionId: the region Id
        :type regionId: str
        :return: a Region object
        :rtype: Region
        '''
        
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
        '''
        region.get_all_regions
        get all regions
        
        :return: list of Region objects
        :rtype: list[Region]
        '''
        
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
        '''
        battle.get_battle
        get info about a battle
        
        :param battleId: the battle Id
        :type battleId: str
        :return: a Battle object
        :rtype: Battle
        '''
        
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
        direction: Literal["forward", "backward"] = "forward",
        filter: BATTLE_FILTER = "all",
        defenderRegionId: str | None = None,
        warId: str | None = None,
        countryId: str | None = None
    ) -> tuple[list[Battle], str | None]:
        '''
        battle.get_battles
        get many battles with optional filtering
        with war or country Id
        
        :param isActive: wether to return only active battles or not
        :type isActive: bool
        :param limit: the amount of battles returned
        :type limit: int
        :param cursor: the key for fetching the next page results
        :type cursor: str | None
        :param direction: the direction
        :type direction: Literal["forward", "backward"]
        :param filter: filter which battle
        :type filter: BATTLE_FILTER
        :param defenderRegionId: the id of the defender Region (optional)
        :type defenderRegionId: str | None
        :param warId: the war Id (optional)
        :type warId: str | None
        :param countryId: the country Id (optional)
        :type countryId: str | None
        :return: a tuple with the first index holding list of Battle objects and the second holding an optional cursor
        :rtype: tuple[list[Battle], str | None]
        '''
        
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

        return (
            [
            Battle(**battle) for battle in result["items"]
            ],
            result.get("nextCursor")
        )
    

    async def get_live_battle_data(
        self,
        battleId: str,
        roundNumber: int = 0
    ) -> BattleData:
        '''
        battle.get_live_battle_data
        get live data from a battle
        
        :param battleId: the battle Id
        :type battleId: str
        :param roundNumber: the round number
        :type roundNumber: int
        :return: BattleData object
        :rtype: BattleData
        '''
        
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
        '''
        round.get_round
        get a battle Round info
        
        :param roundId: the round Id
        :type roundId: str
        :return: Round object
        :rtype: Round
        '''
        
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
        '''
        round.get_round_last_hits
        get last hits from a round
        
        :param roundId: the round Id
        :type roundId: str
        :return: a tuple with the first index holding a list of BattleHit for the attacker side and the second index holding a list of BattleHit for the defender side
        :rtype: tuple[list[BattleHit], list[BattleHit]]
        '''
        
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


    # ItemTrading

    async def get_prices(
        self
    ) -> dict[ITEM, float]:
        '''
        itemTrading.get_prices
        get current items market price
        
        :return: MAPPING[ItemCode: priceInCoins]
        :rtype: dict[ITEM, float]
        '''
        
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
        '''
        worker.get_workers
        get a list of workers for a company
        
        :param companyId: the company Id
        :type companyId: str
        :param userId: the employer Id to filter with
        :type userId: str | None
        :return: a list of Worker objects
        :rtype: list[Worker]
        '''
        
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
    

    async def get_total_workers_count(
        self,
        userId: str
    ) -> int:
        '''
        worker.get_total_workers_count
        get the total number of workers working for a specific user
        
        :param userId: the user Id
        :type userId: str
        :return: the amount of workers
        :rtype: int
        '''
        
        result = await self.request(
            method="POST",
            endpoint="worker.getTotalWorkersCount",
            body={
                "userId": userId
            }
        )

        return result
    

    # battle order

    async def get_battle_orders(
        self,
        battleId: str,
        side: Literal["attacker", "defender"]
    ) -> list[BattleOrder]:
        '''
        battleOrder.get_battle_orders
        get the orders for a specific battle
        
        :param battleId: the battle Id
        :type battleId: str
        :param side: the orders for the attacker or the defender side
        :type side: Literal["attacker", "defender"]
        :return: a list of BattleOrder objects
        :rtype: list[BattleOrder]
        '''

        result = await self.request(
            method="POST",
            endpoint="battleOrder.getByBattle",
            body={
                "battleId": battleId,
                "side": side
            }
        )

        return [
            BattleOrder(**bo) for bo in result
        ]
    

    # inventory

    async def get_user_inventory(
        self,
        userId: str
    ) -> UserEquipments:
        '''
        inventory.get_user_inventory
        get a user equipments
        
        :param userId: the user Id
        :type userId: str
        '''
        
        result = await self.request(
            method="POST",
            endpoint="inventory.fetchCurrentEquipment",
            body={
                "userId": userId
            }
        )

        return UserEquipments(**result)

    # gameStat

    async def get_avg_equipment_price(
        self,
        item: ITEM_MARKET_CODE
    ) -> float:
        '''
        gameStat.get_avg_equipment_price
        
        :param item: the equipment code
        :type item: ITEM_MARKET_CODE
        :return: the price
        :rtype: float
        '''
        
        result = await self.request(
            method="POST",
            endpoint="gameStat.getEquipmentAvgByCode",
            body={
                "itemCode": item
            }
        )

        return result
    

    # party


    async def get_party(
        self,
        partyId: str
    ) -> Party:
        '''
        party.get_party

        :param partyId: the party Id
        :type partyId: str
        :return: a Party object
        :rtype: Party
        '''

        result = await self.request(
            method="POST",
            endpoint="party.getById",
            body={
                "partyId": partyId
            }
        )

        return Party(**result)
