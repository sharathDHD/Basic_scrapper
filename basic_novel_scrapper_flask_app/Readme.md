# 📚 Novel Scraper Flask App

Welcome to the **Novel Scraper Flask App**! This application is designed to scrape and store novel information from websites, focusing on handling novel chapter links and pagination. Built with Flask, SQLAlchemy, and Tailwind CSS, it ensures a seamless and efficient scraping experience. 🚀

![Flask Logo](https://flask.palletsprojects.com/en/2.0.x/_images/flask-logo.png)

## 🌟 Features

1. **Novel URL Submission**: Submit novel URLs through a form on the homepage.
2. **Chapter Link Extraction**: Extracts chapter links and pagination links from stored webpage content.
3. **Link Display**: View chapter and pagination links in separate tables.
4. **Browser Emulation**: Mimics a mobile device to avoid detection.
5. **Error Handling and Logging**: Implements robust error handling and logging.
6. **Database Triggers**: Logs database operations automatically.

## 🛠️ Key Components

### Backend (Flask)
- **Main Application**: Handles routing and core functionality.
- **Database Integration**: Uses SQLAlchemy with PostgreSQL.
- **Web Scraping**: Utilizes cloudscraper and BeautifulSoup.

### Frontend
- **HTML Templates**: Styled with Tailwind CSS.
- **JavaScript**: For dynamic content loading and interaction.

### Database Structure
- **NovelUrls Table**: Stores novel URLs and webpage content.
- **ChaptersList Table**: Stores individual chapter URLs.
- **Log Table**: Tracks database operations.

## 📂 File Structure

```
project_root/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── database.py
│   ├── utils.py
│   └── templates/
│       ├── index.html
│       └── results.html
│
├── config.py
├── run.py
└── requirements.txt
```

## 🚀 Workflow

1. **Submit a Novel URL**: User submits a URL on the homepage.
2. **Fetch Webpage Content**: Application fetches and stores the content.
3. **View Stored Novels**: User can view stored novels and click "View Chapters".
4. **Extract Links**: App parses content to extract links.
5. **Display Links**: Links are displayed in separate tables.

## 🔒 Security and Performance

- **Cloudscraper**: Bypasses Cloudflare protection.
- **Mobile Emulation**: Appears as a natural browser.
- **Database Management**: Efficient session management.
- **Logging**: Automatic logging of database operations.

## 🚀 Potential Improvements

1. Implement user authentication and authorization.
2. Add asynchronous processing for large webpages.
3. Implement a job queue for background scraping tasks.
4. Add sophisticated parsing logic for different websites.
5. Implement caching to reduce database load.
6. Add pagination for stored novels list.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please fork this repository and submit a pull request.

## 📧 Contact

For any inquiries, please contact [sharathkumardaroor@gmail.com](mailto:sharathkumardaroor@gmail.com).

