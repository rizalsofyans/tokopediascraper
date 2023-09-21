import scrapy
import json


class GqltokpedSpider(scrapy.Spider):
    name = "gqltokped"
    allowed_domains = ["gql.tokopedia.com"]
    max_products = 80

    def start_requests(self):
        url = "http://gql.tokopedia.com/graphql"
        headers = {
            "authority": "gql.tokopedia.com",
            "accept": "*/*",
            "accept-language": "id,en-US;q=0.9,en;q=0.8",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://www.tokopedia.com",
            "referer": "https://www.tokopedia.com/the-watch-co/product?sort=8",
            "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "x-device": "default_v3",
            "x-source": "tokopedia-lite",
            "x-tkpd-lite-service": "zeus",
            "x-version": "103c37c",
        }
        etalase_id = "etalase"

        page = 1
        while True:
            query = """
                query ShopProducts(
                $sid: String!
                $page: Int
                $perPage: Int
                $keyword: String
                $etalaseId: String
                $sort: Int
                $user_districtId: String
                $user_cityId: String
                $user_lat: String
                $user_long: String
                ) {
                GetShopProduct(
                    shopID: $sid
                    filter: {
                    page: $page
                    perPage: $perPage
                    fkeyword: $keyword
                    fmenu: $etalaseId
                    sort: $sort
                    user_districtId: $user_districtId
                    user_cityId: $user_cityId
                    user_lat: $user_lat
                    user_long: $user_long
                    }
                ) {
                    status
                    errors
                    links {
                    prev
                    next
                    }
                    data {
                    name
                    product_url
                    product_id
                    price {
                        text_idr
                    }
                    primary_image {
                        original
                        thumbnail
                        resize300
                    }
                    flags {
                        isSold
                        isPreorder
                        isWholesale
                        isWishlist
                    }
                    campaign {
                        discounted_percentage
                        original_price_fmt
                        start_date
                        end_date
                    }
                    label {
                        color_hex
                        content
                    }
                    label_groups {
                        position
                        title
                        type
                        url
                    }
                    badge {
                        title
                        image_url
                    }
                    stats {
                        reviewCount
                        rating
                    }
                    category {
                        id
                    }
                    }
                }
                }
            """

            variables = {
                "sid": "5511907",
                "page": page,
                "perPage": self.max_products,
                "etalaseId": etalase_id,
                "sort": 8,
                "user_districtId": "2289",
                "user_cityId": "178",
                "user_lat": "-6.211939889347085",
                "user_long": "106.94425471311837",
            }

            request_data = {"query": query, "variables": variables}

            yield scrapy.Request(
                url=url,
                method="POST",
                headers=headers,
                body=json.dumps(request_data),
                callback=self.parse_products,
            )

            page += 1
            if page > 100:  # Optional: Stop after reaching page 100
                break

    def parse_products(self, response):

        data = json.loads(response.body)
        items = data.get("data").get("GetShopProduct").get("data")

        for item in items:
            print(item)
            yield {
                "name": item.get("name"),
                "product_id": item.get("product_id"),
                "price": item.get("price").get("text_idr"),
            }
