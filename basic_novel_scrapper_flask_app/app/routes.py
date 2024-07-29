from flask import Blueprint, render_template, request, jsonify, current_app
from app.models import NovelUrls, ChaptersList
from app.database import get_db_session
from app.utils import fetch_content, parse_chapter_links, create_browser_session, set_custom_cookies, simulate_human_behavior, parse_all_links
import logging



bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/fetch', methods=['POST'])
def fetch_novel():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    session = get_db_session()
    try:
        # Check if the URL has already been scraped
        novel_url = session.query(NovelUrls).filter_by(url=url).first()
        if novel_url:
            return jsonify({'message': 'URL already scraped', 'novel_id': novel_url.id})

        content = fetch_content(url)
        if not content:
            return jsonify({'error': 'Failed to fetch content'}), 500

        novel_url = NovelUrls(url=url, webpage_data=content)
        session.add(novel_url)
        session.commit()

        chapter_links = parse_chapter_links(content)
        for chapter_link in chapter_links:
            chapter = ChaptersList(novel_url_id=novel_url.id, chapter_url=chapter_link)
            session.add(chapter)
        session.commit()

        return jsonify({'message': 'Novel and chapters fetched successfully', 'novel_id': novel_url.id})
    except Exception as e:
        session.rollback()
        logging.error(f"Error saving novel data: {str(e)}")
        return jsonify({'error': 'Failed to save novel data'}), 500
    finally:
        session.close()


@bp.route('/novels', methods=['GET'])
def list_novels():
    session = get_db_session()
    try:
        novels = session.query(NovelUrls).all()
        return render_template('results.html', novels=novels)
    except Exception as e:
        logging.error(f"Error fetching novels: {str(e)}")
        return jsonify({'error': 'Failed to fetch novels'}), 500
    finally:
        session.close()

@bp.route('/view_chapters/<int:novel_id>', methods=['GET'])
def view_chapters(novel_id):
    session = get_db_session()
    try:
        novel = session.query(NovelUrls).filter_by(id=novel_id).first()
        if not novel:
            return jsonify({'error': 'Novel not found'}), 404
        
        links = parse_all_links(novel.webpage_data, novel.url)
        return jsonify(links)
    except Exception as e:
        logging.error(f"Error parsing chapters: {str(e)}")
        return jsonify({'error': 'Failed to parse chapters'}), 500
    finally:
        session.close()

@bp.route('/test_browser', methods=['POST'])
def test_browser():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        session = create_browser_session()
        
        # Uncomment and modify if you need to set custom cookies
        # custom_cookies = {'session_id': '1234567890'}
        # set_custom_cookies(session, custom_cookies)
        
        response = session.get(
            url, 
            timeout=current_app.config['REQUEST_TIMEOUT'],
            proxies={'http': current_app.config['PROXY_URL'], 'https': current_app.config['PROXY_URL']} if current_app.config['USE_PROXY'] else None
        )
        
        simulate_human_behavior(session)
        
        return jsonify({
            'status_code': response.status_code,
            'content_length': len(response.text),
            'cookies': dict(response.cookies)
        })
    except Exception as e:
        logging.error(f"Error testing browser: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
