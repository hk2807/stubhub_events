import scrapy
import json


class StubhubSpider(scrapy.Spider):
    name = "stubhub"
    allowed_domains = ["stubhub.com"]
    start_urls = ["https://www.stubhub.com/explore?lat=MjUuNDQ3ODg5OA%3D%3D&lon=LTgwLjQ3OTIyMzY5OTk5OTk5&to=253402300799999&tlcId=2"]

    # Initialize record_counter, file counter and buffer
    record_count = 0
    file_count = 1
    buffer = []
    
    def parse(self, response):

        """
        Builds API URL, and sends request to event API.
        """
        lat_long = self.start_urls[0].split('?')[-1]
        api_url = f'https://www.stubhub.com/explore?method=getExploreEvents&{lat_long}'
        print(api_url)
        headers = {
            'accept': '*/*',
            'accept-language': 'en-IN,en;q=0.9',
            'content-type': 'application/json',
            'priority': 'u=1, i',
            'referer': self.start_urls[0],
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        }

        yield scrapy.Request(url=api_url, headers=headers, callback=self.parse_events)
    
    def parse_events(self, response):
        """
        parse and writes 5 at a time to a new JSON file.
        """
        #print(response.body)
        data = json.loads(response.body)
        events = data.get('events', [])
        #print(data)
        
        for event in events:
            item = {
                "name": event.get("name"),
                "date": f'{event.get("dayOfWeek")}, {event.get("formattedDateWithoutYear")} • {event.get("formattedTime")}',
                "venue": event.get("venueName",'-'),
                "city": event.get("formattedVenueLocation",'-'),
                "Image_url":  event.get("imageUrl",'-')
            }

            # Add to buffer
            self.buffer.append(item)
            self.record_count += 1

            # Once we have 5 records, write to a new file
            if len(self.buffer) == 5:
                self._write_to_file()
        
        # Write remaining records if < 5 left at the end
        if self.buffer:
            self._write_to_file(final=True)

    def _write_to_file(self, final=False):
        """
        Writes events to a JSON file and clears the buffer.
        """
        filename = f"events_{self.file_count}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.buffer, f, ensure_ascii=False, indent=2)

        self.logger.info(f"Wrote {len(self.buffer)} records to {filename}")
        self.buffer = []
        self.file_count += 1