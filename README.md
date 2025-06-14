# stubhub_events
Crawl All the events of Syubhub
This project is a [Scrapy](https://scrapy.org/) spider that scrapes event listings from StubHub based on location (latitude/longitude). It uses StubHub's internal event API and supports pagination.

Events are stored in separate JSON files, with **5 records per file**:
- `events_1.json`
- `events_2.json`
- ...
- etc.

---

## 📦 Features

- ✅ Extracts event name, date, venue, city, image URL, and event URL
- ✅ Supports dynamic latitude/longitude from URL
- ✅ Saves results in chunks of 5 per JSON file

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/hk2807/stubhub_events.git
cd stubhub-scraper
