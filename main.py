from src.api_client import AnalyticsClient
from src.transform import transform_for_eventhub
from src.send_event import EventHubSender
import requests, asyncio

async def main():
    client = AnalyticsClient()
    try:
        analytics_data = client.get_analytics(
            site_id="nerdidads.com",
            metrics=["visitors", "pageviews", "bounce_rate"],
            date_range="7d",
            dimensions=[
                "visit:country_name",
                "visit:city_name",
                "visit:source",
                "visit:device",
                "visit:browser",
                "visit:os"
            ]
        )
        # print(analytics_data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching analytics: {e}")

    try:
        events = transform_for_eventhub(analytics_data)
    except Exception as e:
        print(f"Error transforming analytics data: {e}")
    finally:
        print("event created and sent to eventhub successfully")

    async with EventHubSender() as sender:
        await sender.send_events(events)

if __name__ == "__main__":
    asyncio.run(main())